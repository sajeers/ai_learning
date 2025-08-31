# PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that enables intelligent conversations with PDF documents using Ollama language models and vector embeddings. This project provides **two independent interfaces**: a **Streamlit web app** and a **Chainlit conversational interface**.

## 🌟 Features

- **PDF Document Processing**: Upload and analyze any PDF document
- **Intelligent Q&A**: Ask questions and get contextually accurate answers from your PDFs
- **Comprehensive Summarization**: Generate detailed summaries of entire documents
- **Advanced RAG Pipeline**: Uses sentence transformers for embeddings and ChromaDB for vector storage
- **Multiple Model Support**: Compatible with llama3.2, llama3.1, mistral, codellama, and other Ollama models
- **Customizable Parameters**: Fine-tune responses with temperature, top-p, top-k controls
- **Persistent Chat History**: Conversations are automatically saved and restored
- **CSV Export**: Export chat history with timestamps for analysis
- **Two UI Options**: Choose between Streamlit (web app) or Chainlit (chat interface)
- **GPU/CPU Flexibility**: Automatically handles CUDA compatibility issues

## 🏗️ Project Structure

```
pdf-rag-chatbot/
├── streamlit_app/              # Streamlit web interface
│   ├── app.py                 # Main Streamlit application
│   ├── requirements.txt       # Streamlit dependencies
│   └── README.md             # Streamlit-specific documentation
├── chainlit_app/              # Chainlit chat interface
│   ├── app.py                # Main Chainlit application
│   ├── requirements.txt      # Chainlit dependencies
│   ├── README.md            # Chainlit-specific documentation
│   └── .chainlit/           # Chainlit configuration
│       └── config.toml      # UI and feature settings
├── shared/                   # Shared components
│   └── rag/                 # RAG implementation
│       └── pdf_chatbot.py   # Core RAG logic
├── data/                    # Data storage
│   ├── chroma_db_pdf/      # Vector database storage
│   ├── pdf_chat_history.json # Chat history
│   ├── test.pdf           # Sample PDF
│   └── temp_pdf.pdf       # Uploaded file storage
├── docs/                   # Documentation
│   ├── README.md          # This file
│   └── CHANGELOG.md       # Version history
├── requirements.txt       # Main project dependencies
└── .gitignore            # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Virtual environment (managed centrally from workspace root)

### Installation

1. **Navigate to the workspace root and set up environment**
   ```bash
   cd ../../  # Go to ai_learning_01 root
   ./setup.sh  # One-click setup for entire workspace
   ```

2. **Manual setup (alternative)**
   ```bash
   cd ../../  # Go to ai_learning_01 root
   python -m venv venv
   source venv/bin/activate  # Linux/Mac: venv\Scripts\activate (Windows)
   pip install -r requirements.txt
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

### Choose Your Interface

#### Option A: Streamlit Web App

1. **Run the Streamlit application**
   ```bash
   cd 02_rag_chatbot__pdf
   ./start_streamlit.sh
   ```

2. **Access the interface**
   Open `http://localhost:8501` in your browser

#### Option B: Chainlit Chat Interface

1. **Run the Chainlit application**
   ```bash
   cd 02_rag_chatbot__pdf
   ./start_chainlit.sh
   ```

2. **Access the interface**
   Open `http://localhost:8000` in your browser

#### Option C: Interactive Launcher

1. **Use the main launcher**
   ```bash
   cd 02_rag_chatbot__pdf
   ./start.sh  # Choose interface interactively
   ```

> **Note:** This project uses the **centralized virtual environment** located at `../../venv` (workspace root) for efficient dependency management across all projects.

## 📖 Usage

### Streamlit Interface Features
- **Sidebar Configuration**: Upload PDFs, select models, adjust parameters
- **Real-time Chat**: Interactive question-answering with your documents
- **Chat History**: Expandable conversation history with metadata
- **Export Options**: Save conversations to CSV format
- **Parameter Control**: Fine-tune AI responses with sliders

### Chainlit Interface Features
- **Conversational UI**: Modern chat interface with streaming responses
- **Action Buttons**: Quick access to upload, summary, export functions
- **Live Settings**: Adjust parameters without page refresh
- **Auto-save**: Optional automatic CSV export
- **File Upload**: Drag-and-drop PDF upload experience

### Common Operations
- **Document Summarization**: Ask "Summarize the PDF" or "What is this document about?"
- **Specific Questions**: Query specific information within the document
- **Concept Exploration**: Ask about particular concepts, terms, or sections
- **Content Analysis**: Request analysis of themes, arguments, or data

## ⚙️ Configuration

### Model Parameters
- **Temperature (0.0-2.0)**: Controls response creativity and randomness
- **Top-P (0.0-1.0)**: Nucleus sampling for response diversity
- **Top-K (1-100)**: Limits token selection for coherence
- **Max Tokens**: Maximum response length
- **Context Chunks (1-10)**: Number of document sections to consider

### Supported Models
- llama3.2 (recommended)
- llama3.1
- mistral
- codellama
- Any other Ollama-compatible model

## 🔧 Technical Details

### RAG Pipeline
1. **Document Processing**: PDFs are split into chunks using pdfplumber
2. **Embedding Generation**: Text chunks are encoded using sentence-transformers
3. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
4. **Query Processing**: User questions are embedded and matched against document chunks
5. **Response Generation**: Relevant chunks are provided as context to Ollama models

### Shared Components
- `shared/rag/pdf_chatbot.py`: Core RAG implementation used by both interfaces
- Common vector database and chat history storage
- Consistent model and parameter handling across interfaces

## 📁 Data Management

- **PDF Storage**: Uploaded files are stored in `data/` directory
- **Vector Database**: ChromaDB stores document embeddings in `data/chroma_db_pdf/`
- **Chat History**: Conversations saved in `data/pdf_chat_history.json`
- **CSV Exports**: Generated in respective app directories with timestamps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the appropriate app directory or shared components
4. Test with both interfaces if modifying shared components
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues
- **Ollama not running**: Ensure `ollama serve` is running before starting the app
- **CUDA issues**: The app automatically falls back to CPU if CUDA is unavailable
- **PDF processing errors**: Ensure PDF files are not password-protected or corrupted
- **Port conflicts**: Streamlit uses 8501, Chainlit uses 8000 by default

### Performance Tips
- Use smaller context chunks for faster responses
- Lower temperature for more focused answers
- Increase context chunks for more comprehensive responses
- Use GPU-enabled setup for better performance with large documents
