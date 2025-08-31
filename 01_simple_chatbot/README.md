# Simple AI Chatbot

A streamlined Streamlit-based chatbot application for basic AI conversations using Ollama language models.

## 🌟 Features

- **Simple Interface**: Clean, user-friendly Streamlit web interface
- **Multiple Models**: Support for various Ollama models (llama3.2, llama3.1, mistral, etc.)
- **Persistent Chat**: Conversation history saved and restored automatically
- **Configurable Parameters**: Adjustable temperature, top-p, top-k settings
- **Real-time Responses**: Streaming responses for better user experience
- **Export Options**: Save chat history to JSON or CSV formats

## 🏗️ Project Structure

```
01_simple_chatbot/
├── src/
│   └── app.py              # Main Streamlit application
├── data/
│   └── chat_history.json   # Persistent chat history
├── config/
│   └── settings.py         # Configuration settings
├── docs/
│   └── README.md          # This documentation
├── requirements.txt       # Python dependencies
└── run.sh                # Launch script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Virtual environment (managed centrally from root directory)

### Installation

1. **Navigate to the workspace root and set up environment**
   ```bash
   cd ../  # Go to ai_learning_01 root
   ./setup.sh  # One-click setup for entire workspace
   ```

2. **Manual setup (alternative)**
   ```bash
   cd ../  # Go to ai_learning_01 root
   python -m venv venv
   source venv/bin/activate  # Linux/Mac: venv\Scripts\activate (Windows)
   pip install -r requirements.txt
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

4. **Run the application**
   ```bash
   cd 01_simple_chatbot
   ./run.sh
   # or manually: streamlit run src/app.py
   ```

5. **Access the interface**
   Open your browser to `http://localhost:8501`

> **Note:** This project uses the **centralized virtual environment** located at `../venv` (workspace root) for efficient dependency management across all projects.

## 📖 Usage

### Basic Operations

1. **Start Conversation**: Type your message in the input field
2. **Send Message**: Click "Send" or press Enter
3. **View History**: Scroll through previous conversations
4. **Clear Chat**: Use the "Clear Chat" button to start fresh
5. **Export Data**: Save conversations using export buttons

### Configuration

Use the sidebar to adjust:
- **Model Selection**: Choose from available Ollama models
- **Temperature**: Control response creativity (0.0-2.0)
- **Top P**: Nucleus sampling parameter (0.0-1.0)
- **Top K**: Token selection limit (1-100)
- **Max Tokens**: Maximum response length

## ⚙️ Configuration

### Model Parameters

- **Temperature**: Higher values (1.0-2.0) make responses more creative and random
- **Top P**: Lower values (0.1-0.5) make responses more focused
- **Top K**: Lower values make responses more predictable
- **Max Tokens**: Limits the length of AI responses

### Supported Models

- llama3.2 (recommended for general use)
- llama3.1 (good balance of speed and quality)
- mistral (fast and efficient)
- codellama (optimized for code-related conversations)
- Any other Ollama-compatible model

## 📁 Data Management

- **Chat History**: Automatically saved to `data/chat_history.json`
- **Exports**: Generated files saved in the project directory
- **Persistence**: Conversations restored when app restarts

## 🔧 Development

### File Structure

- `src/app.py`: Main application logic and UI
- `config/settings.py`: Configuration constants and defaults
- `data/`: Storage for chat history and exports
- `docs/`: Documentation and guides

### Customization

1. **Modify UI**: Edit `src/app.py` for interface changes
2. **Change Defaults**: Update `config/settings.py` for default settings
3. **Add Features**: Extend functionality in the main application file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is part of the AI Learning repository. See the main LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

- **Ollama not running**: Ensure `ollama serve` is active
- **Model not found**: Install the model with `ollama pull model_name`
- **Port conflicts**: Streamlit uses port 8501 by default
- **Permission errors**: Ensure write access to the data directory

### Performance Tips

- Use lower temperature for more focused responses
- Reduce max tokens for faster responses
- Choose appropriate models based on your hardware capabilities

## 🔗 Related Projects

- **02_rag_chatbot__pdf**: Advanced RAG chatbot with PDF document processing
- **Main Repository**: Comprehensive AI learning projects collection

---

Built with ❤️ using Streamlit and Ollama
