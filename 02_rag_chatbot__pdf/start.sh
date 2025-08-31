#!/bin/bash

# PDF RAG Chatbot - Main Startup Script
# Choose between Streamlit and Chainlit interfaces

echo "📚 PDF RAG Chatbot - Choose Your Interface"
echo "=========================================="
echo ""
echo "Available interfaces:"
echo "1) 🌐 Streamlit Web App (http://localhost:8501)"
echo "2) 💬 Chainlit Chat Interface (http://localhost:8000)"
echo "3) ❌ Exit"
echo ""

# Check if root virtual environment exists
if [ ! -d "../venv" ]; then
    echo "📦 Creating virtual environment in root directory..."
    cd .. && python -m venv venv && cd 02_rag_chatbot__pdf
fi

while true; do
    read -p "Select interface (1-3): " choice
    case $choice in
        1)
            echo ""
            echo "🚀 Starting Streamlit Web App..."
            ./start_streamlit.sh
            break
            ;;
        2)
            echo ""
            echo "🚀 Starting Chainlit Chat Interface..."
            ./start_chainlit.sh
            break
            ;;
        3)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please select 1, 2, or 3."
            ;;
    esac
done
