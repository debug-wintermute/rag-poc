# CLAUDE.md

## Project Overview

Local RAG proof of concept for a SOC (Security Operations Center) knowledge base. Ingests Markdown documents simulating Confluence pages, stores them as vector embeddings in ChromaDB, and answers natural language queries using Ollama/Mistral with retrieved context. Fully local — no external APIs.

## File Structure

| File | Purpose |
|------|---------|
| `src/config.py` | All configuration constants (paths, model names, chunking params) |
| `src/ingest.py` | Ingestion pipeline entry point: loads markdown files, chunks, embeds, stores in ChromaDB |
| `src/chunker.py` | `chunk_text()` — fixed-size character chunking with word-boundary protection and configurable overlap |
| `src/embeddings.py` | `SentenceTransformerEmbedding` — wraps sentence-transformers to implement ChromaDB's `EmbeddingFunction` protocol |
| `src/retriever.py` | `retrieve()` for standalone use, `retrieve_with_collection()` for the web app (takes pre-initialized collection) |
| `src/generator.py` | `build_prompt()` assembles context + system prompt; `generate()` calls Ollama HTTP API |
| `src/app.py` | FastAPI app — `GET /` serves UI, `POST /api/query` handles queries. Initializes embedding model + ChromaDB client once at startup |
| `src/templates/index.html` | Self-contained dark-themed single-page UI (vanilla JS, no framework) |
| `data/confluence/` | 10 mock SOC Markdown docs for a fictional bank (Meridian National Bank) |
| `data/chroma/` | ChromaDB persistent storage directory (gitignored) |
| `.devcontainer/` | VS Code Dev Container config. `post-create.sh` installs Ollama, Python deps, CLI tools |
| `requirements.txt` | Python dependencies (note: `httpx` and `python-multipart` are installed by post-create.sh but not listed here) |

## Key Architectural Decisions

- **No LangChain** — all orchestration is manual: loader, chunker, embedder, retriever, generator are plain Python modules wired together directly
- **Singleton initialization** — the embedding model (~90MB) and ChromaDB client are loaded once in `app.py` `@app.on_event("startup")` and stored in `app.state`, reused across all requests
- **Fixed-size chunking** — character-based with word-boundary safety (scans backward for nearest space). 500 chars per chunk, 100 char overlap. No semantic/sentence-aware splitting
- **Full rebuild on ingest** — `ingest.py` deletes and recreates the ChromaDB collection every run. No incremental updates
- **Two retriever functions** — `retrieve()` opens its own ChromaDB client (for CLI/scripts), `retrieve_with_collection()` accepts a pre-opened collection (for the web app singleton pattern)
- **Non-streaming generation** — Ollama is called with `stream: false` and a 120s timeout. Full answer returned at once
- **ChromaDB EmbeddingFunction protocol** — `SentenceTransformerEmbedding` implements `__call__` so ChromaDB handles embedding automatically during add/query

## How to Run

```bash
# Start Ollama (background) and pull model
ollama serve &
ollama pull mistral

# Ingest documents (run from repo root)
python -m src.ingest

# Start web UI
uvicorn src.app:app --host 0.0.0.0 --port 8501

# Test a query via curl
curl -X POST http://localhost:8501/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the phishing response procedure?"}'
```

All commands must be run from the repo root (`/workspaces/rag-poc/`) because config paths are relative.

## Configuration (src/config.py)

| Constant | Value | Controls |
|----------|-------|----------|
| `DATA_DIR` | `"data/confluence"` | Source directory for Markdown documents |
| `CHROMA_DIR` | `"data/chroma"` | ChromaDB persistent storage location |
| `CHUNK_SIZE` | `500` | Characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap characters between adjacent chunks |
| `EMBEDDING_MODEL` | `"all-MiniLM-L6-v2"` | sentence-transformers model (384-dim vectors) |
| `COLLECTION_NAME` | `"soc_docs"` | ChromaDB collection name |
| `OLLAMA_URL` | `"http://localhost:11434"` | Ollama API base URL |
| `OLLAMA_MODEL` | `"mistral"` | LLM model for generation |
| `TOP_K` | `5` | Number of chunks retrieved per query |

All values are plain module-level constants. No environment variable support.

## Known Constraints

- **CPU-only inference** — Mistral 7B runs on CPU; expect 30-60s per query
- **No streaming** — user sees nothing until full response completes
- **No authentication** — no auth, no HTTPS, local use only
- **Model must be pulled manually** — `ollama pull mistral` required after every container rebuild
- **Relative paths** — all file paths in config.py are relative; must run from repo root
- **Missing from requirements.txt** — `httpx` and `python-multipart` are installed by `post-create.sh` but not listed in `requirements.txt`
- **No incremental ingest** — every ingestion run is a full rebuild

## Current Phase

Phase 6 — evaluation and iteration.
