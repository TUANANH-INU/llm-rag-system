#!/bin/bash

# Frontend setup script

echo "Setting up RAG Chatbot Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Please install Node.js 18 or higher."
    exit 1
fi

echo "Node.js version:"
node --version

# Install dependencies
echo "Installing npm packages..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env .env.local
    echo "Created .env file. Update it if needed."
fi

echo "Frontend setup complete!"
echo "Run 'npm run dev' to start the development server"
