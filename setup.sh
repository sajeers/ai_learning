#!/bin/bash

# AI Learning Projects - Workspace Setup Script

echo "🚀 AI Learning Projects - Workspace Setup"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created at ./venv"
else
    echo "✅ Virtual environment already exists at ./venv"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install all dependencies
echo "📥 Installing all project dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Workspace setup complete!"
echo ""
echo "🎯 Available Projects:"
echo "1. Simple Chatbot: cd 01_simple_chatbot && ./run.sh"
echo "2. RAG PDF Chatbot: cd 02_rag_chatbot__pdf && ./start.sh"
echo ""
echo "📖 For more information, see README.md"
