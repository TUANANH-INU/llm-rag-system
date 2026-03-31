#!/bin/bash
# Initialize Ollama with required models

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Try to pull models with exponential backoff
pull_model() {
    local model=$1
    local max_attempts=5
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Pulling model: $model (attempt $attempt/$max_attempts)"
        if ollama pull $model; then
            echo "Successfully pulled $model"
            return 0
        fi
        
        sleep $((2 ** attempt))
        attempt=$((attempt + 1))
    done
    
    echo "Failed to pull $model after $max_attempts attempts"
    return 1
}

# Pull required models
pull_model "llama2"
pull_model "nomic-embed-text"

# Keep Ollama running in foreground
wait $OLLAMA_PID
