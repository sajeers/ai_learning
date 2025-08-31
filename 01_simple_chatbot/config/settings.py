# Simple AI Chatbot - Configuration Settings

# Default model settings
DEFAULT_MODEL = "llama3.2"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_TOP_K = 40
DEFAULT_MAX_TOKENS = 1000

# Available models
AVAILABLE_MODELS = [
    "llama3.2",
    "llama3.1",
    "mistral",
    "codellama"
]

# UI Configuration
PAGE_TITLE = "Simple AI Chatbot"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# File paths
CHAT_HISTORY_FILE = "data/chat_history.json"

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"

# Streamlit settings
DEFAULT_PORT = 8501
