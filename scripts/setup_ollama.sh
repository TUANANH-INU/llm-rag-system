#!/bin/bash

# Script to setup and run Ollama with LLaMA3

set -e

echo "Setting up Ollama with LLaMA3..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Create ollama data directory
mkdir -p ~/.ollama/models

echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
sleep 5

echo "Pulling LLaMA2 model..."
ollama pull llama2

echo "Pulling nomic-embed-text for embeddings..."
ollama pull nomic-embed-text

echo "Pulling mistral as alternative LLM..."
ollama pull mistral

echo "Setup complete!"
echo "Ollama is running. Models available:"
ollama list

wait $OLLAMA_PID
