# Changelog

All notable changes to the PDF RAG Chatbot project will be documented in this file.

## [2.0.0] - 2025-08-31

### 🎉 Major Restructure - Separate Streamlit and Chainlit Apps

#### Added
- **Independent Application Structure**: Separated Streamlit and Chainlit into independent folders
- **Streamlit App** (`streamlit_app/`):
  - Dedicated `app.py` with web-based interface
  - Independent `requirements.txt` for Streamlit dependencies
  - Comprehensive README with Streamlit-specific instructions
- **Chainlit App** (`chainlit_app/`):
  - Dedicated `app.py` with conversational interface
  - Independent `requirements.txt` for Chainlit dependencies
  - Chainlit configuration in `.chainlit/config.toml`
  - Comprehensive README with Chainlit-specific instructions
- **Shared Components** (`shared/`):
  - Common RAG implementation in `shared/rag/pdf_chatbot.py`
  - Reusable across both applications
- **Startup Scripts**:
  - `start_streamlit.sh` - One-click Streamlit app launcher
  - `start_chainlit.sh` - One-click Chainlit app launcher
- **Enhanced Documentation**:
  - Updated main README with dual-app architecture
  - App-specific README files with focused instructions
  - Comprehensive .gitignore for both applications

#### Changed
- **Project Structure**: Completely reorganized from single-app to dual-app architecture
- **Import Paths**: Updated both apps to use shared RAG module from `shared/` directory
- **Requirements Management**: Split dependencies into app-specific files plus shared core dependencies
- **File Paths**: Updated PDF storage paths to work with new directory structure

#### Technical Improvements
- **Independence**: Both apps can be developed and deployed independently
- **Code Reuse**: Shared RAG logic eliminates duplication
- **Maintainability**: Clear separation of concerns between UI frameworks
- **Flexibility**: Users can choose their preferred interface (web app vs chat)

#### Migration Notes
- **From v1.x**: 
  - Old `src/pdf_streamlit_ui.py` → `streamlit_app/app.py`
  - Old `src/pdf_chainlit_ui.py` → `chainlit_app/app.py`
  - RAG logic moved to `shared/rag/pdf_chatbot.py`
- **Data Compatibility**: Existing `data/` directory structure maintained
- **Chat History**: Previous chat histories remain compatible

### 🚀 Quick Start Options
- **Streamlit**: `./start_streamlit.sh` or `cd streamlit_app && streamlit run app.py`
- **Chainlit**: `./start_chainlit.sh` or `cd chainlit_app && chainlit run app.py`

### 📁 New Directory Structure
```
02_rag_chatbot__pdf/
├── streamlit_app/          # Streamlit web interface
├── chainlit_app/           # Chainlit chat interface  
├── shared/                 # Shared RAG components
├── data/                   # Common data storage
├── docs/                   # Documentation
├── start_streamlit.sh      # Streamlit launcher
├── start_chainlit.sh       # Chainlit launcher
└── requirements.txt        # Core shared dependencies
```

## [1.x] - Previous Versions

### Features (Legacy Structure)
- Single Streamlit application
- Basic PDF RAG functionality
- Manual setup and configuration
- Combined source directory structure
