# PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that enables intelligent conversations with PDF documents using Ollama language models and vector embeddings.

## 🌟 Features

- **PDF Document Processing**: Upload and analyze any PDF document
- **Intelligent Q&A**: Ask questions and get contextually accurate answers from your PDFs
- **Comprehensive Summarization**: Generate detailed summaries of entire documents
- **Advanced RAG Pipeline**: Uses sentence transformers for embeddings and ChromaDB for vector storage
- **Multiple Model Support**: Compatible with llama3.2, llama3.1, mistral, codellama, and other Ollama models
- **Customizable Parameters**: Fine-tune responses with temperature, top-p, top-k controls
- **Persistent Chat History**: Conversations are automatically saved and restored
- **CSV Export**: Export chat history with timestamps for analysis
- **Modern Web Interface**: Clean, responsive Streamlit-based UI
- **GPU/CPU Flexibility**: Automatically handles CUDA compatibility issues

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pdf-rag-chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama service**
   ```bash
   ollama serve
   ```

5. **Run the application**
   ```bash
   streamlit run pdf_streamlit_ui.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501` to access the chatbot interface.

## 📖 Usage

### Basic Workflow

1. **Upload PDF**: Use the file uploader in the sidebar to select your PDF document
2. **Initialize Chatbot**: Click "Initialize/Reload Chatbot" to process the document
3. **Configure Parameters**: Adjust temperature, top-p, top-k in the sidebar
4. **Ask Questions**: Type your questions in the chat interface
5. **Get Answers**: Receive contextually relevant responses based on your PDF content

### Supported Operations

- **Document Summarization**: Ask "Summarize the PDF" or "What is this document about?"
- **Specific Questions**: Query specific information within the document
- **Concept Exploration**: Ask about particular concepts, terms, or sections
- **Content Analysis**: Request analysis of themes, arguments, or data

### Parameter Tuning

- **Temperature (0.0-2.0)**: Controls response creativity and randomness
- **Top-P (0.0-1.0)**: Nucleus sampling for response diversity
- **Top-K (1-100)**: Limits token selection for coherence
- **Context Chunks (1-10)**: Number of document sections to consider

## 🏗️ Architecture

```
pdf-rag-chatbot/
├── src/
│   ├── pdf_streamlit_ui.py     # Main Streamlit interface
│   └── rag/
│       └── pdf_chatbot.py      # Core RAG logic
├── data/
│   ├── chroma_db_pdf/          # Vector database storage
│   ├── pdf_chat_history.json  # Chat history
│   ├── test.pdf               # Sample PDF
│   └── temp_pdf.pdf           # Uploaded file storage
├── docs/
│   └── README.md              # This file
├── requirements.txt           # Python dependencies
└── .gitignore                # Git ignore rules
```

### Technical Stack

- **Frontend**: Streamlit for web interface
- **Backend**: Python with Ollama integration
- **Document Processing**: PDFplumber for text extraction
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB for similarity search
- **Language Models**: Ollama (llama3.2, mistral, etc.)

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional) for custom configurations:

```env
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=llama3.2
DEFAULT_TEMPERATURE=0.7
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

### Model Selection

The application supports any Ollama model. Popular choices:

- **llama3.2**: Best overall performance and accuracy
- **mistral**: Fast responses with good quality
- **codellama**: Optimized for technical documents

## 📊 Data Management

### Chat History

- Automatically saved to `pdf_chat_history.json`
- Persistent across sessions
- Includes timestamps, queries, responses, and parameters

### Vector Database

- Stored in `chroma_db_pdf/` directory
- Automatically manages embeddings
- Supports multiple documents
- Handles file changes and updates

### Export Options

- **CSV Export**: Save conversations with timestamps
- **JSON Backup**: Complete chat history with metadata
- **PDF Annotations**: Future feature for document markup

## 🛠️ Development

### Project Structure

```python
# Core components
pdf_chatbot.py          # RAG pipeline implementation
pdf_streamlit_ui.py     # Web interface
requirements.txt        # Dependencies

# Key functions
- load_and_embed_pdf()     # Document processing
- search_context()         # Similarity search
- generate_response()      # LLM integration
- generate_summary()       # Document summarization
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Testing

```bash
# Run basic functionality test
python -c "from rag.pdf_chatbot import PDFRAGChatbot; bot = PDFRAGChatbot(); print('Setup successful')"

# Test with sample PDF
streamlit run pdf_streamlit_ui.py
```

## 🐛 Troubleshooting

### Common Issues

**CUDA Compatibility**
- The application automatically falls back to CPU processing
- No manual configuration required

**PDF Processing Errors**
- Ensure PDF is not password-protected
- Check file size (recommended < 50MB)
- Verify PDF contains extractable text (not just images)

**Model Not Found**
- Ensure Ollama is running: `ollama serve`
- Install required model: `ollama pull llama3.2`
- Check model name spelling in interface

**Slow Performance**
- Reduce context chunks in sidebar
- Use smaller models (mistral vs llama3.2)
- Consider GPU setup for better performance

### Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Ollama documentation
3. Open an issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM serving
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Streamlit](https://streamlit.io/) for web interface
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [PDFplumber](https://github.com/jsvine/pdfplumber) for PDF processing

---

**Built with ❤️ for intelligent document interaction**
