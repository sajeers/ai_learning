#!/bin/bash

# PDF RAG Chatbot Startup Script
# This script ensures proper setup and launches the application

echo "🚀 Starting PDF RAG Chatbot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama is running
echo "🤖 Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running. Please start Ollama with: ollama serve"
    echo "   And ensure you have a model installed: ollama pull llama3.2"
    read -p "Press Enter when Ollama is ready..."
fi

# Ensure data directory exists
mkdir -p data

# Navigate to src directory and run the application
echo "🌐 Launching Streamlit application..."
cd src && streamlit run pdf_streamlit_ui.py

echo "✅ Application started! Open your browser to http://localhost:8501"
