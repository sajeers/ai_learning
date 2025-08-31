# Streamlit PDF RAG Chatbot

A web-based interface for chatting with PDF documents using Streamlit and AI models.

## Features

- **Interactive Web UI**: Clean, responsive Streamlit interface
- **PDF Upload**: Upload and process PDF documents
- **Real-time Chat**: Ask questions and get AI-powered responses
- **Configurable Parameters**: Adjust temperature, top-p, top-k settings
- **Chat History**: Persistent conversation history with export options
- **Multiple Models**: Support for various Ollama models

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama service**
   ```bash
   ollama serve
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the interface**
   Open your browser to `http://localhost:8501`

## Usage

1. Upload a PDF file using the sidebar
2. Click "Initialize/Reload Chatbot" to process the document
3. Adjust generation parameters as needed
4. Start asking questions about your PDF content
5. Export chat history to CSV when needed

## Configuration

- **Temperature**: Controls response creativity (0.0-2.0)
- **Top P**: Nucleus sampling parameter (0.0-1.0)
- **Top K**: Token selection limit (1-100)
- **Max Tokens**: Maximum response length
- **Context Chunks**: Number of document sections to consider

## Tips

- Higher temperature values produce more creative responses
- Lower temperature values produce more focused responses
- Adjust context chunks based on document complexity
- Use the export feature to save important conversations
