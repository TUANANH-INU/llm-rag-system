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

- Docker & Docker Compose
- 4GB+ RAM (for Ollama models)
- Port 3000 (Frontend), 8000 (Backend), 11434 (Ollama) available

## 🚀 Quick Start

```bash
# Start entire system with Docker Compose
docker compose -f docker/docker-compose.yml up -d

# Wait 30-60 seconds for services to initialize, then access:
```

**Access the application:**
- 🎨 **Frontend:** http://localhost:3000
- 📡 **Backend API:** http://localhost:8000
- 📖 **API Documentation:** http://localhost:8000/docs
- 🤖 **Ollama Service:** http://localhost:11434

**Stop the system:**
```bash
docker compose -f docker/docker-compose.yml down
```

**View logs:**
```bash
docker compose -f docker/docker-compose.yml logs -f backend
docker compose -f docker/docker-compose.yml logs -f ollama
docker compose -f docker/docker-compose.yml logs -f frontend
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
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API services
│   │   ├── App.jsx               # Main app component
│   │   └── index.css             # Styles
│   ├── package.json              # NPM dependencies
│   ├── Dockerfile                # Frontend container
│   └── .env                      # Environment variables
├── docker/
│   ├── Dockerfile.backend        # Backend container
│   ├── Dockerfile.ollama         # Ollama container
│   └── docker-compose.yml        # Compose orchestration
└── data/                         # Uploaded documents & vector store
    ├── uploads/                  # PDF uploads
    └── vector_store/             # FAISS indices
```

## 🔧 Configuration

All configuration is done through environment variables in Docker containers:

**Backend** - Automatically loaded from `backend/.env.example`:
```env
LLM_MODEL=llama2
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://ollama:11434
API_HOST=0.0.0.0
API_PORT=8000
```

**Frontend** - Configured in `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=RAG Chatbot
```

To customize settings, update the `docker-compose.yml` environment variables or the `.env` files before running the containers.

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
# Start all services
docker compose -f docker/docker-compose.yml up -d

# Stop all services
docker compose -f docker/docker-compose.yml down

# View logs (all services)
docker compose -f docker/docker-compose.yml logs -f

# View specific service logs
docker compose -f docker/docker-compose.yml logs -f backend
docker compose -f docker/docker-compose.yml logs -f ollama
docker compose -f docker/docker-compose.yml logs -f frontend

# Restart specific service
docker compose -f docker/docker-compose.yml restart backend

# Rebuild images (after code changes)
docker compose -f docker/docker-compose.yml build

# Remove all containers and volumes
docker compose -f docker/docker-compose.yml down -v

# Check service status
docker compose -f docker/docker-compose.yml ps
```

## 🔧 Troubleshooting

**Services won't start?**
```bash
# Check logs
docker compose -f docker/docker-compose.yml logs

# Verify port availability
lsof -i :3000 :8000 :11434

# Clean up and restart
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml up -d
```

**Slow performance?**
```bash
# Check container resource usage
docker stats
```

**Need to access container shell?**
```bash
# Access backend container
docker compose -f docker/docker-compose.yml exec backend bash

# Access frontend container
docker compose -f docker/docker-compose.yml exec frontend sh

# Access ollama container
docker compose -f docker/docker-compose.yml exec ollama bash
```

**Ollama models not loading?**
- Wait 1-2 minutes after startup for models to pull
- Check ollama logs: `docker compose -f docker/docker-compose.yml logs ollama`
- Verify internet connection during container startup

## 📝 Available Models

To use different LLM models, update `docker-compose.yml`:

**LLM Models:**
- `llama2` - Default, balanced speed & quality ⭐
- `mistral` - Smaller, faster
- `neural-chat` - Optimized for conversation

Change in `docker-compose.yml`:
```yaml
environment:
  - LLM_MODEL=mistral  # or neural-chat, llama2
```

Then rebuild: `docker compose -f docker/docker-compose.yml build && docker compose -f docker/docker-compose.yml up -d`

## 📊 System Configuration

**Adjust RAG parameters in `backend/main.py` before building:**

```python
# Chunk size (default: 512)
RAGSystem(chunk_size=1024)

# Retrieval count (default: 5)
rag_system.query(question, k=10)

# Embedding batch size (larger = faster but more memory)
embed_chunks(chunks, batch_size=20)
```

## 🔒 Security Considerations

- Run Ollama on localhost only in production
- Use authentication for exposed API endpoints
- Validate and sanitize user inputs
- Limit file upload sizes
- Implement rate limiting on endpoints

## 📦 Stack Overview

**Backend:**
- FastAPI - Web framework
- Ollama - Local LLM
- FAISS - Vector search
- PyPDF + BeautifulSoup4 - Document processing

**Frontend:**
- React 18 - UI framework
- Vite - Build tool
- Axios - HTTP client

**Infrastructure:**
- Docker & Docker Compose - Containerization
- Python 3.10 - Backend runtime
- Node.js 18 - Frontend runtime

---

## 📝 License

See [LICENSE](LICENSE) file

