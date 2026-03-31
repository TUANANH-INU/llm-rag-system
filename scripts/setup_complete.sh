#!/bin/bash

# Complete system setup script

echo "=========================================="
echo "   RAG Chatbot System Setup"
echo "=========================================="
echo ""

# Function to print section header
print_header() {
    echo ""
    echo ">> $1"
    echo "--------------------------------------"
}

# Check prerequisites
print_header "Checking prerequisites"
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "  Found Python $PYTHON_VERSION"

echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 18+"
    exit 1
fi
NODE_VERSION=$(node --version | sed 's/v//')
echo "  Found Node.js $NODE_VERSION"

echo "✓ Checking Git..."
if ! command -v git &> /dev/null; then
    echo "⚠ Git not found (optional)"
else
    echo "  Found Git $(git --version | awk '{print $3}')"
fi

# Setup backend
print_header "Setting up Backend"
cd backend
source ../scripts/setup_backend.sh
cd ..

# Setup frontend
print_header "Setting up Frontend"
cd frontend
bash ../scripts/setup_frontend.sh
cd ..

# Setup Ollama instructions
print_header "Ollama Setup"
echo "To use Ollama locally:"
echo "1. Install Ollama: https://ollama.ai"
echo "2. Pull models:"
echo "   ollama pull llama2"
echo "   ollama pull nomic-embed-text"
echo "3. Start Ollama in another terminal: ollama serve"
echo ""
echo "Or use Docker Compose (includes Ollama):"
echo "   cd docker && docker-compose up -d"

# Summary
print_header "Setup Complete!"
echo ""
echo "Next steps:"
echo ""
echo "1. Local Development:"
echo "   Terminal 1 - Ollama: ollama serve"
echo "   Terminal 2 - Backend: cd backend && source venv/bin/activate && python main.py"
echo "   Terminal 3 - Frontend: cd frontend && npm run dev"
echo ""
echo "2. Docker (Recommended):"
echo "   cd scripts && bash start_docker.sh"
echo ""
echo "3. Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "=========================================="
