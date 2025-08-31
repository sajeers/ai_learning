#!/bin/bash

# Simple AI Chatbot Launch Script

echo "🤖 Starting Simple AI Chatbot..."

# Check if root virtual environment exists
if [ ! -d "../venv" ]; then
    echo "📦 Creating virtual environment in root directory..."
    cd .. && python -m venv venv && cd 01_simple_chatbot
fi

# Activate root virtual environment
echo "🔧 Activating root virtual environment..."
source ../venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama is running
echo "🔍 Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running. Please start it with: ollama serve"
    echo "   You can run this in another terminal window."
    read -p "Press Enter once Ollama is running to continue..."
fi

# Start Streamlit application
echo "🌐 Starting Streamlit application..."
echo "   Access at: http://localhost:8501"
streamlit run src/app.py
