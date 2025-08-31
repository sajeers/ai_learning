import streamlit as st
import ollama
import csv
import json
from datetime import datetime
import os
import sys

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from settings import *

# Configure Streamlit page
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

st.title(f"{PAGE_ICON} {PAGE_TITLE}")
st.write("Send prompts to LLM models with custom parameters.")

# Chat history file with proper path
CHAT_HISTORY_PATH = os.path.join(os.path.dirname(__file__), '..', CHAT_HISTORY_FILE)

# Functions to handle persistent chat history
def save_chat_history(history):
    """Save chat history to JSON file"""
    try:
        with open(CHAT_HISTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

def load_chat_history():
    """Load chat history from JSON file"""
    try:
        if os.path.exists(CHAT_HISTORY_PATH):
            with open(CHAT_HISTORY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading chat history: {e}")
    return []

def truncate_timestamp(timestamp_str):
    """Truncate timestamp to YYYY-MM-DDTHH:mm:ss format"""
    try:
        if len(timestamp_str) > 19:
            return timestamp_str[:19]
        return timestamp_str
    except:
        return timestamp_str

def save_to_csv_file(content, model, temperature, top_p, top_k, max_tokens, response, system_prompt="", seed=None, stop_sequences="", stream=False):
    """Save chat interaction to CSV file with datetime appended"""
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"ollama_output_{now}.csv"
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow([
                    'datetime', 'model', 'prompt', 'temperature', 'top_p', 'top_k',
                    'max_tokens', 'seed', 'stop_sequences', 'system_prompt', 'stream', 'response'
                ])
            writer.writerow([
                datetime.now().isoformat(),
                model,
                content,
                temperature,
                top_p,
                top_k,
                max_tokens,
                seed or '',
                stop_sequences,
                system_prompt,
                stream,
                response
            ])
        return filename
    except Exception as e:
        st.error(f"Error saving to CSV: {e}")
        return None

# Initialize session state variables
if 'is_waiting' not in st.session_state:
    st.session_state['is_waiting'] = False
if 'cancel_requested' not in st.session_state:
    st.session_state['cancel_requested'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = load_chat_history()

# Disable input widgets when waiting for response
input_disabled = st.session_state['is_waiting']

# Create main input form
with st.form(key="chat_form", clear_on_submit=False):
    st.subheader("📝 Chat Input")

    # Main content input
    content = st.text_area(
        "Prompt Content",
        value="" if not hasattr(st.session_state, 'last_content') else st.session_state.get('last_content', ''),
        height=100,
        disabled=input_disabled,
        help="Enter your prompt here"
    )

    # Model selection
    col1, col2 = st.columns([2, 1])
    with col1:
        model_options = ["llama3.2", "mistral", "codellama", "custom"]
        model_choice = st.selectbox("Model", model_options, disabled=input_disabled)
        if model_choice == "custom":
            model = st.text_input("Enter custom model name", "", disabled=input_disabled)
        else:
            model = model_choice


    # Advanced parameters in expandable section
    with st.expander("🔧 Advanced Parameters", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.01, disabled=input_disabled,
                                  help="Controls randomness. Lower = more focused, Higher = more creative")
            top_p = st.slider("Top P (nucleus sampling)", min_value=0.0, max_value=1.0, value=0.9, step=0.01, disabled=input_disabled,
                            help="Cumulative probability cutoff for token selection")
            top_k = st.number_input("Top K", min_value=1, max_value=100, value=40, disabled=input_disabled,
                                  help="Limits token selection to top K most likely tokens")

        with col2:
            max_tokens = st.number_input("Max tokens", min_value=1, max_value=4000, value=1000, disabled=input_disabled,
                                       help="Maximum number of tokens to generate")
            seed = st.number_input("Seed (optional)", min_value=0, value=None, disabled=input_disabled,
                                 help="Random seed for reproducible outputs")
            system_prompt = st.text_area("System Prompt (optional)", value="", disabled=input_disabled,
                                       help="System message to set AI behavior")

    # Options
    col1, col2 = st.columns(2)
    with col1:
        save_to_csv = st.checkbox("💾 Save output to CSV file", disabled=input_disabled,
                                help="Saves conversation to CSV with timestamp")

    with col2:
        stream = st.checkbox("Stream response", value=True, disabled=input_disabled)
    # Form submission buttons
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        send_clicked = st.form_submit_button("🚀 Ask AI", disabled=input_disabled, use_container_width=True)
    with col2:
        clear_clicked = st.form_submit_button("🗑️ Clear History", disabled=input_disabled)

# Cancel button (outside form to work immediately)
if st.session_state['is_waiting']:
    if st.button("❌ Cancel Request", use_container_width=True, type="secondary"):
        st.session_state['cancel_requested'] = True
        st.session_state['is_waiting'] = False
        st.rerun()

# Handle clear history
if clear_clicked:
    st.session_state['chat_history'] = []
    save_chat_history([])
    st.success("✅ Chat history cleared!")
    st.rerun()

# Handle send request
if send_clicked and not st.session_state['is_waiting']:
    if not model or (model_choice == "custom" and not model.strip()):
        st.error("❌ Please select or enter a model name.")
    elif not content.strip():
        st.error("❌ Prompt content cannot be empty.")
    else:
        st.session_state['is_waiting'] = True
        st.session_state['cancel_requested'] = False
        st.session_state['last_content'] = content  # Store for form persistence
        st.rerun()

# Process request when waiting
if st.session_state['is_waiting'] and not st.session_state['cancel_requested']:
    with st.spinner("🤖 Generating response... Click 'Cancel Request' to stop."):
        try:
            # Prepare messages
            messages = []
            if system_prompt.strip():
                messages.append({
                    'role': 'system',
                    'content': system_prompt.strip()
                })

            # Build options dict
            options = {
                'temperature': temperature,
                'top_p': top_p,
                'top_k': top_k,
                'num_predict': max_tokens,  # Ollama uses num_predict instead of max_tokens
            }
            if seed is not None:
                options['seed'] = seed

            messages.append({
                'role': 'user',
                'content': content
            })

            # Make API call
            response = ollama.chat(
                model=model,
                messages=messages,
                stream=stream,
                options=options
            )

            # Handle response
            if stream:
                response_container = st.container()
                with response_container:
                    st.markdown("**🤖 AI Response:**")
                    response_box = st.empty()
                    full_response = ""

                for chunk in response:
                    if st.session_state['cancel_requested']:
                        break
                    if 'message' in chunk and 'content' in chunk['message']:
                        full_response += chunk['message']['content']
                        response_box.markdown(full_response)

                final_response = full_response
            else:
                if not st.session_state['cancel_requested']:
                    final_response = response['message']['content']
                    st.markdown("**🤖 AI Response:**")
                    st.markdown(final_response)
                else:
                    final_response = ""

            # Save to history and CSV if not cancelled
            if not st.session_state['cancel_requested'] and final_response:
                timestamp = datetime.now().isoformat()

                # Add to chat history (newest first)
                assistant_msg = {
                    'role': 'assistant',
                    'content': final_response,
                    'timestamp': timestamp,
                    'model': model
                }

                user_msg = {
                    'role': 'user',
                    'content': content,
                    'timestamp': timestamp,
                    'parameters': {
                        'temperature': temperature,
                        'top_p': top_p,
                        'top_k': top_k,
                        'max_tokens': max_tokens,
                        'seed': seed,
                        'system_prompt': system_prompt,
                        'stream': stream
                    }
                }

                # Insert at beginning (newest first)
                st.session_state['chat_history'].insert(0, assistant_msg)
                st.session_state['chat_history'].insert(0, user_msg)

                # Save to persistent storage
                save_chat_history(st.session_state['chat_history'])

                # Save to CSV if requested
                if save_to_csv:
                    filename = save_to_csv_file(
                        content, model, temperature, top_p, top_k, max_tokens,
                        final_response, system_prompt, seed, "", stream
                    )
                    if filename:
                        st.success(f"💾 Output saved to {filename}")

            # Reset waiting state
            st.session_state['is_waiting'] = False
            if 'last_content' in st.session_state:
                del st.session_state['last_content']  # Clear form after successful send
            st.rerun()

        except Exception as e:
            st.session_state['is_waiting'] = False
            st.error(f"❌ Error: {str(e)}")
            st.rerun()

# Display chat history section
st.markdown("---")
st.subheader("💬 Chat History")

if st.session_state['chat_history']:
    # Display newest conversations first
    current_conversation = []

    for idx, msg in enumerate(st.session_state['chat_history']):
        current_conversation.append(msg)

        # When we hit an assistant message or it's the last message, display the conversation
        if msg['role'] == 'assistant' or idx == len(st.session_state['chat_history']) - 1:
            # Find the user message for this conversation
            user_msg = None
            assistant_msg = None

            for conv_msg in reversed(current_conversation):
                if conv_msg['role'] == 'user' and user_msg is None:
                    user_msg = conv_msg
                elif conv_msg['role'] == 'assistant' and assistant_msg is None:
                    assistant_msg = conv_msg

            # Display the conversation in a container
            with st.container():
                if user_msg:
                    timestamp = user_msg.get('timestamp', 'Unknown time')
                    params = user_msg.get('parameters', {})

                    st.markdown(f"**👤 You** ({truncate_timestamp(timestamp)}):")
                    st.markdown(f"> {user_msg['content']}")

                    if params:
                        param_str = f"🔧 **Parameters:** temp={params.get('temperature', 'N/A')}, top_p={params.get('top_p', 'N/A')}, top_k={params.get('top_k', 'N/A')}, max_tokens={params.get('max_tokens', 'N/A')}"
                        if params.get('seed'):
                            param_str += f", seed={params.get('seed')}"
                        if params.get('system_prompt'):
                            param_str += f", system_prompt=✓"
                        st.caption(param_str)

                if assistant_msg:
                    timestamp = assistant_msg.get('timestamp', 'Unknown time')
                    model_used = assistant_msg.get('model', 'Unknown model')

                    st.markdown(f"**🤖 {model_used}** ({truncate_timestamp(timestamp)}):")
                    st.markdown(assistant_msg['content'])

                # Add visual separation between conversations
                st.markdown("---")

            current_conversation = []
else:
    st.info("📝 No chat history yet. Start a conversation above!")

# Footer
st.markdown("---")
st.caption("💡 **Tips:** Use advanced parameters to fine-tune responses. Enable streaming for real-time output. Save important conversations to CSV for later reference.")