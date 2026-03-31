#!/bin/bash

# Start everything with Docker Compose

echo "Starting RAG Chatbot System..."

cd docker

# Build images
echo "Building Docker images..."
docker-compose build

# Pull models for Ollama (optional, can be done manually)
# docker-compose run --rm ollama ollama pull llama2
# docker-compose run --rm ollama ollama pull nomic-embed-text

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check status
echo "Service status:"
docker-compose ps

echo ""
echo "✓ RAG Chatbot System started!"
echo ""
echo "Services:"
echo "  - Ollama:   http://localhost:11434"
echo "  - Backend:  http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Frontend: http://localhost:3000"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
