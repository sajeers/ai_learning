#!/bin/bash

# Streamlit PDF RAG Chatbot Startup Script

echo "🚀 Starting Streamlit PDF RAG Chatbot..."

# Check if root virtual environment exists
if [ ! -d "../venv" ]; then
    echo "📦 Creating virtual environment in root directory..."
    cd .. && python -m venv venv && cd 02_rag_chatbot__pdf
fi

# Activate root virtual environment
echo "🔧 Activating root virtual environment..."
source ../venv/bin/activate

# Install dependencies from streamlit app directory
echo "📥 Installing dependencies..."
pip install -r streamlit_app/requirements.txt

# Check if Ollama is running
echo "🔍 Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running. Please start it with: ollama serve"
    echo "   You can run this in another terminal window."
    read -p "Press Enter once Ollama is running to continue..."
fi

# Start Streamlit from root directory
echo "🌐 Starting Streamlit application..."
echo "   Access at: http://localhost:8501"
cd streamlit_app && streamlit run app.py
