# 🤖 RAG Chatbot - AI Q&A System

A complete Retrieval Augmented Generation (RAG) chatbot system that allows users to upload PDFs, load website content, and ask questions with source citations.

## 🎯 Features

- ✅ **PDF Upload** - Upload and process PDF documents
- ✅ **Web Content Loading** - Fetch and process content from websites
- ✅ **Intelligent Retrieval** - Find relevant documents using embeddings and FAISS
- ✅ **Citation Support** - Answers include source references
- ✅ **Local LLM** - Run LLaMA3 or other models locally with Ollama
- ✅ **Docker Support** - Easy deployment with Docker & Docker Compose
- ✅ **Modern UI** - React-based frontend with real-time chat

## 🏗️ System Architecture

```
User Interface (React)
        ↓
FastAPI Backend (8000)
        ↓
┌─────────────────────────────┐
│   RAG Pipeline              │
├─────────────────────────────┤
│ ├─ Document Loader (PDF/Web)│
│ ├─ Text Chunker             │
│ ├─ Embedder (Ollama)        │
│ ├─ Vector Store (FAISS)     │
│ ├─ Retriever                │
│ └─ LLM (Ollama)             │
└─────────────────────────────┘
        ↓
Ollama Service (11434)
└─ LLaMA2 / LLaMA3
└─ Nomic-Embed-Text
```

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)
- Or Ollama installed locally (for local deployment)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd scripts
bash start_docker.sh
```

The system will start with:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Ollama Service: http://localhost:11434

### Option 2: Local Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Run setup script (Linux/Mac)
bash ../scripts/setup_backend.sh

# Activate virtual environment
source venv/bin/activate

# Create .env file
cp .env.example .env

# Start backend server
python main.py
```

#### Ollama Setup

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama2
ollama pull nomic-embed-text

# Start Ollama service (in separate terminal)
ollama serve
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📁 Project Structure

```
llm-rag-system/
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── loader.py         # PDF & Web document loading
│   │   │   ├── chunker.py        # Text chunking
│   │   │   ├── embeddings.py     # Embedding generation
│   │   │   ├── vector_store.py   # FAISS vector database
│   │   │   ├── retriever.py      # Document retrieval
│   │   │   ├── llm.py            # LLM integration
│   │   │   └── pipeline.py       # Main RAG pipeline
│   │   └── api/
│   │       ├── documents.py      # Document endpoints
│   │       └── rag.py            # RAG query endpoints
│   ├── main.py                   # FastAPI application
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API services
│   │   └── App.jsx               # Main app component
│   ├── package.json              # NPM dependencies
│   └── Dockerfile                # Frontend container
├── docker/
│   ├── Dockerfile.backend        # Backend container
│   ├── Dockerfile.ollama         # Ollama container
│   └── docker-compose.yml        # Compose configuration
└── scripts/
    ├── setup_backend.sh          # Backend setup script
    ├── setup_frontend.sh         # Frontend setup script
    ├── setup_ollama.sh           # Ollama setup script
    └── start_docker.sh           # Docker startup script
```

## 🔧 Configuration

### Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
# LLM Configuration
LLM_MODEL=llama2              # or mistral, neural-chat
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
RELOAD=false

# Data Configuration
DATA_DIR=data
VECTOR_STORE_PATH=data/vector_store
UPLOAD_DIR=data/uploads
```

### Frontend Environment Variables

Create `.env` file in `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=RAG Chatbot
```

## 📚 API Endpoints

### Documents

- `POST /api/documents/upload-pdf/` - Upload PDF file
- `POST /api/documents/load-url/` - Load content from URL
- `GET /api/documents/list/` - List uploaded documents
- `DELETE /api/documents/delete/{document_id}` - Delete document

### RAG

- `POST /api/rag/query` - Query the system
  ```json
  {
    "question": "What is...?",
    "k": 5
  }
  ```
- `POST /api/rag/add-pdf` - Add PDF to RAG system
- `POST /api/rag/add-url` - Add URL content to RAG system
- `GET /api/rag/status` - Get system status
- `POST /api/rag/save` - Save vector store
- `POST /api/rag/load` - Load vector store

## 🎮 Usage

1. **Upload Documents**
   - Go to "Documents" tab
   - Upload PDF files or provide website URLs
   - Documents are automatically processed and indexed

2. **Ask Questions**
   - Go to "Chat" tab
   - Type your question
   - System retrieves relevant documents and generates answers
   - Answers include source citations

3. **Adjust Settings**
   - Change "Retrieval Count" for more/fewer source documents
   - Select different LLM models via configuration

## 🔍 How RAG Works

1. **Document Loading**: PDF or web content is loaded and extracted
2. **Chunking**: Documents are split into manageable chunks with overlap
3. **Embedding**: Chunks are converted to embeddings using Ollama embeddings model
4. **Indexing**: Embeddings are stored in FAISS vector database
5. **Retrieval**: Query is embedded and similar chunks are retrieved
6. **Generation**: LLM generates answer based on query and retrieved context
7. **Citations**: Source documents are included in the response

## 🐳 Docker Commands

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove all data
docker-compose down -v
```

## 🔧 Troubleshooting

### Ollama connection issues
- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Check `OLLAMA_BASE_URL` in backend `.env`
- Ensure Ollama models are pulled: `ollama list`

### Models not available
```bash
# Pull required models
ollama pull llama2
ollama pull nomic-embed-text
ollama pull mistral  # Optional alternative
```

### Backend connection issues
- Check backend logs: `docker-compose logs backend`
- Verify API port 8000 is accessible
- Check CORS settings if frontend can't reach backend

### PDF upload issues
- Ensure PDF files are valid
- Check file size limits
- Verify write permissions in `data/uploads/`

## 📝 Available Models

### LLM Models
- `llama2` - Default, good balance of speed and quality
- `mistral` - Smaller, faster inference
- `neural-chat` - Optimized for chat
- `llama3` - Latest LLaMA version (if available)

### Embedding Models
- `nomic-embed-text` - Default, good general-purpose embeddings

Pull additional models:
```bash
ollama pull mistral
ollama pull neural-chat
```

## 📊 Performance Tuning

### Chunk Size
- Smaller chunks (256-512): Better precision, more retrieval
- Larger chunks (1024+): Better context, fewer retrievals

### Retrieval Count (k)
- Lower k (3-5): Faster, focused results
- Higher k (10-20): More comprehensive, slower

### Batch Size
- Adjust in `backend/app/rag/embeddings.py`
- Larger batch = faster processing but more memory

## 🔒 Security Considerations

- Run Ollama on localhost in production
- Use authentication for API endpoints
- Validate and sanitize user inputs
- Limit file upload sizes
- Implement rate limiting on API endpoints

## 📦 Dependencies

### Backend
- FastAPI - Web framework
- Ollama - Local LLM integration
- FAISS - Vector similarity search
- LangChain - LLM utilities
- PyPDF - PDF processing
- BeautifulSoup4 - Web scraping

### Frontend
- React 18 - UI framework
- Vite - Build tool
- Axios - HTTP client

## 📄 License

See LICENSE file

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs
3. Check API docs: http://localhost:8000/docs

---

**Made with ❤️ for the RAG community**
