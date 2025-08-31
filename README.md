# AI Learning Projects

A comprehensive collection of AI and machine learning projects, created for my learning purpose, focused on chatbot development, RAG \(Retrieval-Augmented Generation\) systems, and language model integration.


## 🎯 Overview

This repository contains progressive AI learning projects, from simple chatbots to advanced document processing systems. Each project is designed to build upon previous concepts while introducing new techniques and technologies.

## 📁 Project Structure

```
ai_learning_01/
├── 01_simple_chatbot/         # Basic Streamlit chatbot with Ollama
├── 02_rag_chatbot__pdf/       # Advanced RAG system with PDF processing
├── venv/                      # Centralized virtual environment
├── data/                      # Shared data storage (if needed)
├── docs/                      # Additional documentation
├── requirements.txt           # Consolidated dependencies for all projects
├── setup.sh                   # One-click workspace setup script
├── LICENSE                    # License information
└── README.md                  # This file
```

## 🚀 Projects

### 1. Simple AI Chatbot (`01_simple_chatbot/`)

**Technology Stack:** Streamlit, Ollama
**Complexity:** Beginner

A clean, user-friendly chatbot interface for basic AI conversations.

**Features:**
- Multiple Ollama model support
- Configurable AI parameters
- Persistent chat history
- CSV export functionality
- Professional project structure

**Quick Start:**
```bash
cd 01_simple_chatbot
./run.sh
```

### 2. RAG PDF Chatbot (`02_rag_chatbot__pdf/`)

**Technology Stack:** Streamlit/Chainlit, Ollama, ChromaDB, Sentence Transformers
**Complexity:** Advanced

A sophisticated document processing system with dual interface options.

**Features:**
- PDF document ingestion and processing
- Vector embeddings with ChromaDB
- Dual UI: Streamlit web app & Chainlit chat interface
- Document summarization
- Advanced RAG pipeline
- Shared component architecture

**Quick Start:**
```bash
cd 02_rag_chatbot__pdf
./start.sh  # Choose interface
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Web interface framework
- **Chainlit**: Conversational UI framework
- **Ollama**: Local language model integration

### AI/ML Libraries
- **sentence-transformers**: Text embeddings
- **ChromaDB**: Vector database
- **pdfplumber**: PDF text extraction
- **torch**: Deep learning framework

### Data & Storage
- **pandas**: Data manipulation
- **JSON**: Configuration and data storage
- **CSV**: Export functionality

## 🔧 Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB+ RAM (8GB+ recommended)
- Storage: 2GB+ for models and data

### Required Software
1. **Python**: [Download Python](https://python.org/downloads/)
2. **Ollama**: [Install Ollama](https://ollama.ai/)
3. **Git**: For cloning the repository

### Recommended Models
```bash
# Install recommended Ollama models
ollama pull llama3.2      # General purpose (recommended)
ollama pull llama3.1      # Alternative general model  
ollama pull mistral       # Fast and efficient
ollama pull codellama     # Code-focused conversations
```

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai_learning_01
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Start Ollama Service
```bash
ollama serve
```

### 4. Choose Your Project
- **Beginners**: Start with `01_simple_chatbot/`
- **Advanced Users**: Explore `02_rag_chatbot__pdf/`

## 📚 Learning Path

### Phase 1: Fundamentals
1. **Simple Chatbot**: Learn basic Streamlit and Ollama integration
2. **Configuration Management**: Understand professional project structure
3. **UI/UX Principles**: Design clean, user-friendly interfaces

### Phase 2: Advanced Concepts
1. **RAG Systems**: Implement document retrieval and augmentation
2. **Vector Databases**: Work with embeddings and similarity search
3. **Multi-Interface Design**: Build both web and chat interfaces

### Phase 3: Production Readiness
1. **Error Handling**: Robust exception management
2. **Performance Optimization**: Efficient processing and caching
3. **Deployment Strategies**: Prepare for production environments

## 🤝 Contributing

### Guidelines
1. **Fork** the repository
2. **Create** a feature branch for your project
3. **Follow** existing project structure patterns
4. **Document** your code and features thoroughly
5. **Test** all functionality before submitting
6. **Submit** a pull request with clear description

### Project Standards
- **Code Quality**: Follow PEP 8 style guidelines
- **Documentation**: Include comprehensive README files
- **Structure**: Use organized folder hierarchies
- **Dependencies**: Pin version numbers in requirements.txt
- **Configuration**: Separate settings from code logic

## 📖 Documentation

### Project-Specific Docs
- [Simple Chatbot Guide](01_simple_chatbot/README.md)
- [RAG PDF Chatbot Guide](02_rag_chatbot__pdf/docs/README.md)

### Additional Resources
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Chainlit Documentation](https://docs.chainlit.io)

## 🆘 Troubleshooting

### Common Issues

**Ollama Connection Errors:**
```bash
# Ensure Ollama is running
ollama serve

# Check available models
ollama list

# Pull missing models
ollama pull llama3.2
```

**Python Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Port Conflicts:**
- Streamlit default: `http://localhost:8501`
- Chainlit default: `http://localhost:8000`
- Ollama default: `http://localhost:11434`

### Performance Tips
1. **Hardware**: Use GPU if available for faster processing
2. **Models**: Choose appropriate model size for your hardware
3. **Parameters**: Tune temperature and token limits for optimal responses
4. **Caching**: Leverage built-in caching mechanisms

## 📈 Future Projects

### Planned Additions
- **03_multimodal_chatbot**: Image and text processing
- **04_agent_framework**: Multi-agent conversation systems
- **05_deployment_ready**: Production deployment examples

### Enhancement Ideas
- **Database Integration**: PostgreSQL/MongoDB support
- **Authentication**: User management systems
- **API Development**: REST API interfaces
- **Cloud Deployment**: AWS/GCP deployment guides

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team**: For providing excellent local LLM integration
- **Streamlit Team**: For the intuitive web framework
- **Chainlit Team**: For the modern chat interface
- **Open Source Community**: For the amazing AI/ML libraries

---

**Happy Learning! 🚀**

Built with ❤️ for the AI learning community
