# Chainlit PDF RAG Chatbot

A conversational AI interface for chatting with PDF documents using Chainlit and AI models.

## Features

- **Conversational UI**: Modern chat interface with streaming responses
- **PDF Upload**: Drag-and-drop PDF file upload
- **Action Buttons**: Quick access to common functions
- **Real-time Settings**: Adjust parameters on-the-fly
- **Auto-save Options**: Automatic CSV export of conversations
- **Document Summary**: Generate comprehensive document overviews
- **Session Management**: Persistent chat history and settings

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
   chainlit run app.py
   ```

4. **Access the interface**
   Open your browser to `http://localhost:8000`

## Usage

1. Upload a PDF file using the "📁 Upload PDF" action button
2. Adjust settings using the gear icon (⚙️) in the interface
3. Use action buttons for quick operations:
   - **📁 Upload PDF**: Upload new documents
   - **📋 Generate Summary**: Get document overview
   - **💾 Export to CSV**: Save chat history
   - **🗑️ Clear History**: Reset conversation
   - **🔄 Reload PDF**: Refresh document processing

## Settings

- **Model**: Choose from available Ollama models
- **Temperature**: Response creativity control
- **Top P/K**: Token selection parameters
- **Max Tokens**: Response length limit
- **Context Chunks**: Document sections to analyze
- **Auto-save CSV**: Automatic conversation export

## Action Buttons

The interface provides convenient action buttons for:
- Document management (upload, reload)
- Content analysis (summary generation)
- Data export (CSV export)
- Session management (clear history)

## Tips

- Use the settings panel to fine-tune AI responses
- Enable auto-save CSV for automatic conversation backups
- The summary feature provides quick document overviews
- Action buttons provide quick access to common operations
