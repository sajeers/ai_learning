import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import sys

# Add the shared directory to the path
shared_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared'))
if shared_path not in sys.path:
    sys.path.insert(0, shared_path)

try:
    from rag.pdf_chatbot import PDFRAGChatbot
except ImportError as e:
    st.error(f"Could not import PDFRAGChatbot: {e}")
    st.error("Please ensure the shared/rag directory exists and contains pdf_chatbot.py")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'cancel_generation' not in st.session_state:
    st.session_state.cancel_generation = False

def initialize_chatbot(pdf_file, model_name):
    """Initialize the PDF chatbot with the uploaded file."""
    try:
        if pdf_file is not None:
            # Save uploaded file temporarily - updated path for new structure
            temp_path = "../data/temp_pdf.pdf"
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(pdf_file.getvalue())

            # Initialize chatbot with the uploaded file and force reload
            chatbot = PDFRAGChatbot(pdf_file_path=temp_path, model_name=model_name)
            # Force reload to ensure we're using the new file
            reload_message = chatbot.force_reload_pdf(temp_path)
            return chatbot, f"PDF uploaded and loaded successfully! {reload_message}"
        else:
            # Try to use existing test.pdf - updated path
            test_pdf_path = "../data/test.pdf"
            if os.path.exists(test_pdf_path):
                chatbot = PDFRAGChatbot(pdf_file_path=test_pdf_path, model_name=model_name)
                return chatbot, "Using existing test.pdf file"
            else:
                return None, "Please upload a PDF file"
    except Exception as e:
        return None, f"Error initializing chatbot: {str(e)}"

def save_to_csv(chat_history):
    """Save chat history to CSV with timestamp."""
    if not chat_history:
        return "No chat history to save"

    try:
        # Prepare data for CSV
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
        filename = f"chat_history_{timestamp}.csv"
        df.to_csv(filename, index=False)
        return f"Chat history saved to {filename}"
    except Exception as e:
        return f"Error saving to CSV: {str(e)}"

def load_chat_history():
    """Load chat history from JSON file."""
    try:
        if os.path.exists("pdf_chat_history.json"):
            with open("pdf_chat_history.json", "r") as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading chat history: {e}")
    return []

def save_chat_history(chat_history):
    """Save chat history to JSON file."""
    try:
        with open("pdf_chat_history.json", "w") as f:
            json.dump(chat_history, f, indent=2)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

# Load existing chat history
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history()

# Main UI
st.title("📚 PDF RAG Chatbot")
st.markdown("Chat with your PDF documents using AI")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    # PDF file upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

    # Model selection
    model_name = st.selectbox(
        "Select Model",
        ["llama3.2", "llama3.1", "mistral", "codellama"],
        index=0
    )

    # Parameters
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    top_k = st.slider("Top K", 1, 100, 40, 1)

    # Additional parameters you might want
    max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
    context_chunks = st.slider("Context Chunks", 1, 10, 5, 1)  # Increased default

    # Summary mode toggle
    summary_mode = st.checkbox("📋 Full Document Summary Mode",
                              help="Get comprehensive summary of entire document")

    st.divider()

    # Initialize chatbot button
    if st.button("🔄 Initialize/Reload Chatbot", type="primary"):
        with st.spinner("Initializing chatbot..."):
            chatbot, message = initialize_chatbot(uploaded_file, model_name)
            if chatbot:
                st.session_state.chatbot = chatbot
                st.success(message)
                # Show document info
                if hasattr(chatbot, 'collection') and chatbot.collection.count() > 0:
                    st.info(f"📄 Document loaded with {chatbot.collection.count()} text chunks")
            else:
                st.error(message)

    st.divider()

    # Export options
    st.subheader("Export Options")
    if st.button("💾 Save to CSV"):
        if st.session_state.chat_history:
            message = save_to_csv(st.session_state.chat_history)
            st.success(message)
        else:
            st.warning("No chat history to save")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        save_chat_history([])
        st.success("Chat history cleared")
        st.rerun()

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    # Query input
    query = st.text_area(
        "Enter your question about the PDF:",
        height=100,
        disabled=st.session_state.processing
    )

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer

    # Send button
    send_button = st.button(
        "🚀 Ask AI",
        type="primary",
        disabled=st.session_state.processing or not query.strip(),
        use_container_width=True
    )

    # Cancel button (only show when processing)
    if st.session_state.processing:
        if st.button("❌ Cancel", type="secondary", use_container_width=True):
            st.session_state.cancel_generation = True
            st.session_state.processing = False

# Process query
if send_button and query.strip() and st.session_state.chatbot:
    st.session_state.processing = True
    st.session_state.cancel_generation = False

    # Show processing indicator
    with st.spinner("Generating response..."):
        try:
            # Generate response
            result = st.session_state.chatbot.generate_response(
                query,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k
            )

            # Check if generation was cancelled
            if not st.session_state.cancel_generation:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if isinstance(result, dict):
                    response_text = result['response']
                    model_used = result.get('model', model_name)
                else:
                    response_text = str(result)
                    model_used = model_name

                # Add to chat history (new responses at top)
                chat_entry = {
                    'timestamp': timestamp,
                    'query': query,
                    'response': response_text,
                    'model': model_used,
                    'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k
                }

                st.session_state.chat_history.insert(0, chat_entry)
                save_chat_history(st.session_state.chat_history)

                st.success("Response generated successfully!")
            else:
                st.warning("Generation cancelled by user")

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

    st.session_state.processing = False
    st.rerun()

elif send_button and not st.session_state.chatbot:
    st.error("Please initialize the chatbot first by uploading a PDF or using the existing test.pdf file")

# Display chat history
st.header("💬 Chat History")

if st.session_state.chat_history:
    for i, entry in enumerate(st.session_state.chat_history):
        # Create expandable container for each chat entry
        with st.expander(
            f"🕒 {entry['timestamp']} - {entry['query'][:50]}{'...' if len(entry['query']) > 50 else ''}",
            expanded=(i == 0)  # Expand the most recent entry
        ):
            # Display query
            st.markdown("**📝 Query:**")
            st.write(entry['query'])

            # Display response
            st.markdown("**🤖 Response:**")
            st.write(entry['response'])

            # Display metadata
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.caption(f"Model: {entry.get('model', 'N/A')}")
            with col2:
                st.caption(f"Temp: {entry.get('temperature', 'N/A')}")
            with col3:
                st.caption(f"Top-P: {entry.get('top_p', 'N/A')}")
            with col4:
                st.caption(f"Top-K: {entry.get('top_k', 'N/A')}")

        # Add separator between entries
        if i < len(st.session_state.chat_history) - 1:
            st.divider()
else:
    st.info("No chat history yet. Start by asking a question about your PDF!")

# Footer
st.markdown("---")
st.markdown("💡 **Tips:**")
st.markdown("- Upload a PDF file or ensure 'test.pdf' exists in the current directory")
st.markdown("- Adjust temperature for creativity (higher = more creative)")
st.markdown("- Use Top-P and Top-K to control response diversity")
st.markdown("- Chat history is automatically saved and persists between sessions")
