#!/bin/bash

# Backend setup script

echo "Setting up RAG Chatbot Backend..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data/uploads
mkdir -p data/vector_store

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp backend/.env.example backend/.env
    echo "Created .env file. Please update it with your settings."
fi

echo "Backend setup complete!"
echo "Run 'source venv/bin/activate' to activate the virtual environment"
echo "Run 'python backend/main.py' to start the server"
