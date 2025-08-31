import chainlit as cl
import os
import sys
import asyncio
from datetime import datetime
import json
import pandas as pd

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from rag.pdf_chatbot import PDFRAGChatbot

# Global storage for chat history
CHAT_HISTORY_FILE = "pdf_chat_history.json"

def save_chat_history(history):
    """Save chat history to JSON file"""
    try:
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving chat history: {e}")

def load_chat_history():
    """Load chat history from JSON file"""
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading chat history: {e}")
    return []

def save_to_csv_file(chat_history):
    """Save chat history to CSV with timestamp"""
    if not chat_history:
        return None

    try:
        csv_data = []
        for entry in chat_history:
            csv_data.append({
                'timestamp': entry['timestamp'],
                'query': entry['query'],
                'response': entry['response'],
                'model': entry.get('model', 'N/A'),
                'temperature': entry.get('temperature', 'N/A'),
                'top_p': entry.get('top_p', 'N/A'),
                'top_k': entry.get('top_k', 'N/A')
            })

        df = pd.DataFrame(csv_data)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"pdf_chat_history_{timestamp}.csv"
        df.to_csv(filename, index=False)
        return filename
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

@cl.on_chat_start
async def start():
    """Initialize the PDF RAG chatbot session"""
    await cl.Message(
        content="📚 **Welcome to PDF RAG Chatbot!**\n\nI can help you chat with your PDF documents using AI. Please upload a PDF file to get started, or I'll try to use an existing test.pdf file.",
    ).send()

    # Set up configuration settings
    settings = await cl.ChatSettings([
        cl.input_widget.Select(
            id="model",
            label="Model",
            values=["llama3.2", "llama3.1", "mistral", "codellama"],
            initial_index=0,
        ),
        cl.input_widget.Slider(
            id="temperature",
            label="Temperature",
            initial=0.7,
            min=0.0,
            max=2.0,
            step=0.01,
        ),
        cl.input_widget.Slider(
            id="top_p",
            label="Top P",
            initial=0.9,
            min=0.0,
            max=1.0,
            step=0.01,
        ),
        cl.input_widget.Slider(
            id="top_k",
            label="Top K",
            initial=40,
            min=1,
            max=100,
            step=1,
        ),
        cl.input_widget.Slider(
            id="max_tokens",
            label="Max Tokens",
            initial=1000,
            min=100,
            max=4000,
            step=100,
        ),
        cl.input_widget.Slider(
            id="context_chunks",
            label="Context Chunks",
            initial=5,
            min=1,
            max=10,
            step=1,
        ),
        cl.input_widget.Switch(
            id="save_to_csv",
            label="Auto-save to CSV",
            initial=False,
        ),
    ]).send()

    # Initialize session variables
    cl.user_session.set("chatbot", None)
    cl.user_session.set("chat_history", load_chat_history())
    cl.user_session.set("pdf_loaded", False)

    # Try to initialize with existing test.pdf
    await initialize_default_pdf()

    # Add action buttons
    actions = [
        cl.Action(name="upload_pdf", value="upload", description="📁 Upload PDF", payload={"action": "upload_pdf"}),
        cl.Action(name="show_summary", value="summary", description="📋 Generate document summary", payload={"action": "show_summary"}),
        cl.Action(name="export_csv", value="export", description="💾 Export chat to CSV", payload={"action": "export_csv"}),
        cl.Action(name="clear_history", value="clear", description="🗑️ Clear chat history", payload={"action": "clear_history"}),
        cl.Action(name="reload_pdf", value="reload", description="🔄 Reload PDF", payload={"action": "reload_pdf"}),
    ]

    await cl.Message(
        content="🛠️ **Available Actions:** Use the buttons below to manage your PDF chat session.",
        actions=actions,
        author="System"
    ).send()

async def initialize_default_pdf():
    """Try to initialize with existing test.pdf"""
    try:
        test_pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "test.pdf")
        if os.path.exists(test_pdf_path):
            settings = cl.user_session.get("settings", {})
            model_name = settings.get("model", "llama3.2")

            chatbot = PDFRAGChatbot(pdf_file_path=test_pdf_path, model_name=model_name)
            cl.user_session.set("chatbot", chatbot)
            cl.user_session.set("pdf_loaded", True)

            chunk_count = chatbot.collection.count() if hasattr(chatbot, 'collection') else 0
            await cl.Message(
                content=f"✅ **Automatically loaded existing PDF:** `test.pdf`\n📄 Document contains {chunk_count} text chunks",
                author="System"
            ).send()
        else:
            await cl.Message(
                content="ℹ️ No existing PDF found. Please upload a PDF file using the 'Upload PDF' action button.",
                author="System"
            ).send()
    except Exception as e:
        await cl.Message(
            content=f"⚠️ Error loading existing PDF: {str(e)}",
            author="System"
        ).send()

@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates"""
    cl.user_session.set("settings", settings)

    # If model changed and chatbot exists, update it
    chatbot = cl.user_session.get("chatbot")
    if chatbot:
        chatbot.model_name = settings.get("model", "llama3.2")

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    chatbot = cl.user_session.get("chatbot")

    if not chatbot:
        await cl.Message(
            content="❌ No PDF loaded. Please upload a PDF file first using the 'Upload PDF' action button.",
            author="System"
        ).send()
        return

    settings = cl.user_session.get("settings", {})

    # Extract parameters
    temperature = settings.get("temperature", 0.7)
    top_p = settings.get("top_p", 0.9)
    top_k = settings.get("top_k", 40)
    save_to_csv = settings.get("save_to_csv", False)

    user_content = message.content

    # Create response message
    response_msg = cl.Message(content="")
    await response_msg.send()

    try:
        # Show thinking indicator
        await response_msg.stream_token("🤔 Searching PDF and generating response...")

        # Generate response
        result = chatbot.generate_response(
            user_content,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k
        )

        # Clear the thinking message and show actual response
        response_msg.content = ""

        if isinstance(result, dict):
            response_text = result['response']
            model_used = result.get('model', settings.get('model', 'llama3.2'))

            # Stream the response
            for char in response_text:
                await response_msg.stream_token(char)
                await asyncio.sleep(0.01)  # Small delay for streaming effect

            # Show context information if available
            if 'context_used' in result:
                context_info = f"\n\n📖 **Context:** Used {len(result['context_used'])} relevant chunks"
                for i, ctx in enumerate(result['context_used'][:3]):  # Show first 3 contexts
                    page = ctx['metadata']['page']
                    relevance = ctx['relevance_score']
                    context_info += f"\n- Page {page} (relevance: {relevance:.2f})"

                await response_msg.stream_token(context_info)

        else:
            response_text = str(result)
            model_used = settings.get('model', 'llama3.2')
            await response_msg.stream_token(response_text)

        await response_msg.update()

        # Save to chat history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_entry = {
            'timestamp': timestamp,
            'query': user_content,
            'response': response_text,
            'model': model_used,
            'temperature': temperature,
            'top_p': top_p,
            'top_k': top_k
        }

        chat_history = cl.user_session.get("chat_history", [])
        chat_history.insert(0, chat_entry)
        cl.user_session.set("chat_history", chat_history)
        save_chat_history(chat_history)

        # Auto-save to CSV if enabled
        if save_to_csv:
            filename = save_to_csv_file(chat_history)
            if filename:
                await cl.Message(
                    content=f"💾 Chat history auto-saved to `{filename}`",
                    author="System"
                ).send()

        # Show parameters used
        param_info = f"🔧 **Model:** {model_used} | **Temp:** {temperature} | **Top-P:** {top_p} | **Top-K:** {top_k}"
        await cl.Message(
            content=param_info,
            author="System"
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ Error generating response: {str(e)}",
            author="System"
        ).send()

@cl.action_callback("upload_pdf")
async def handle_file_upload(action):
    """Handle PDF file upload"""
    files = await cl.AskFileMessage(
        content="Please upload a PDF file:",
        accept=["application/pdf"],
        max_size_mb=10
    ).send()

    if not files:
        return

    file = files[0]

    try:
        # Save uploaded file
        temp_path = os.path.join(os.path.dirname(__file__), "..", "data", "temp_uploaded.pdf")
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        with open(temp_path, "wb") as f:
            f.write(file.content)

        # Initialize chatbot with uploaded file
        settings = cl.user_session.get("settings", {})
        model_name = settings.get("model", "llama3.2")

        await cl.Message(
            content=f"📁 Processing uploaded PDF: `{file.name}`...",
            author="System"
        ).send()

        chatbot = PDFRAGChatbot(pdf_file_path=temp_path, model_name=model_name)
        reload_message = chatbot.force_reload_pdf(temp_path)

        cl.user_session.set("chatbot", chatbot)
        cl.user_session.set("pdf_loaded", True)

        chunk_count = chatbot.collection.count() if hasattr(chatbot, 'collection') else 0

        await cl.Message(
            content=f"✅ **PDF uploaded successfully!**\n📄 `{file.name}` loaded with {chunk_count} text chunks\n\nYou can now ask questions about the document!",
            author="System"
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ Error processing PDF: {str(e)}",
            author="System"
        ).send()

@cl.action_callback("export_csv")
async def on_export_csv(action):
    """Export chat history to CSV"""
    chat_history = cl.user_session.get("chat_history", [])

    if not chat_history:
        await cl.Message(
            content="📝 No chat history to export.",
            author="System"
        ).send()
        return

    filename = save_to_csv_file(chat_history)
    if filename:
        await cl.Message(
            content=f"✅ Chat history exported to `{filename}`",
            author="System"
        ).send()
    else:
        await cl.Message(
            content="❌ Error exporting chat history.",
            author="System"
        ).send()

@cl.action_callback("clear_history")
async def on_clear_history(action):
    """Clear chat history"""
    cl.user_session.set("chat_history", [])
    save_chat_history([])
    await cl.Message(
        content="✅ Chat history cleared!",
        author="System"
    ).send()

@cl.action_callback("show_summary")
async def on_show_summary(action):
    """Generate document summary"""
    chatbot = cl.user_session.get("chatbot")

    if not chatbot:
        await cl.Message(
            content="❌ No PDF loaded. Please upload a PDF first.",
            author="System"
        ).send()
        return

    settings = cl.user_session.get("settings", {})

    await cl.Message(
        content="📋 Generating comprehensive document summary...",
        author="System"
    ).send()

    try:
        result = chatbot.generate_summary(
            temperature=settings.get("temperature", 0.2),
            top_p=settings.get("top_p", 0.9),
            top_k=settings.get("top_k", 40)
        )

        if isinstance(result, dict):
            summary_content = f"## 📋 Document Summary\n\n{result['response']}\n\n"
            summary_content += f"📊 **Analysis Stats:**\n"
            summary_content += f"- Content chunks analyzed: {result.get('content_analyzed', 'N/A')}\n"
            summary_content += f"- Pages covered: {result.get('pages_covered', 'N/A')}\n"
            summary_content += f"- Model used: {result.get('model', 'N/A')}"
        else:
            summary_content = f"## 📋 Document Summary\n\n{result}"

        await cl.Message(
            content=summary_content,
            author="System"
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ Error generating summary: {str(e)}",
            author="System"
        ).send()

@cl.action_callback("reload_pdf")
async def on_reload_pdf(action):
    """Reload current PDF"""
    chatbot = cl.user_session.get("chatbot")

    if not chatbot:
        await cl.Message(
            content="❌ No PDF loaded to reload.",
            author="System"
        ).send()
        return

    try:
        reload_message = chatbot.force_reload_pdf()
        chunk_count = chatbot.collection.count() if hasattr(chatbot, 'collection') else 0

        await cl.Message(
            content=f"🔄 **PDF reloaded successfully!**\n{reload_message}\n📄 Document contains {chunk_count} text chunks",
            author="System"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Error reloading PDF: {str(e)}",
            author="System"
        ).send()
