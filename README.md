# RAG PoC

Local RAG (Retrieval-Augmented Generation) proof of concept for a SOC knowledge base. Queries Confluence-style security documentation using a fully local pipeline — no external API calls, no cloud dependencies.

## Architecture

```
                         INGESTION
  data/confluence/*.md ──→ Loader ──→ Chunker ──→ Embeddings ──→ ChromaDB
                                      (500 char,   (all-MiniLM   (HNSW index,
                                      100 overlap)  -L6-v2)       data/chroma/)

                         RETRIEVAL + GENERATION
  User query ──→ Embed query ──→ ChromaDB top-K ──→ Build prompt ──→ Ollama/Mistral ──→ Answer
                  (same model)    similarity search   (context +       (local, CPU)
                                  (k=5)               system prompt)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Ollama + Mistral 7B |
| Vector store | ChromaDB (persistent, local) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Web framework | FastAPI + Jinja2 |
| HTTP client | httpx (Ollama API calls) |
| Runtime | Python 3.12, VS Code Dev Container |

## Setup

Requires VS Code with the Dev Containers extension.

```bash
# 1. Open in devcontainer
#    Open this folder in VS Code → "Reopen in Container"

# 2. Start Ollama and pull the model
ollama serve &
ollama pull mistral

# 3. Run ingestion (loads, chunks, embeds, stores)
python -m src.ingest

# 4. Start the web UI
uvicorn src.app:app --host 0.0.0.0 --port 8501
```

Open `http://localhost:8501` in your browser. First query takes ~30-60s on CPU.

## Project Structure

```
├── .devcontainer/
│   ├── devcontainer.json        # Container config, port forwarding, resource limits
│   └── post-create.sh           # Installs Ollama, Python deps, CLI tools
├── data/
│   ├── confluence/              # 10 mock SOC Markdown docs (Meridian National Bank)
│   └── chroma/                  # ChromaDB persistent storage (gitignored)
├── src/
│   ├── config.py                # All configuration constants (paths, models, params)
│   ├── ingest.py                # Ingestion pipeline: load → chunk → embed → store
│   ├── chunker.py               # Fixed-size character chunking with word-boundary safety
│   ├── embeddings.py            # SentenceTransformer wrapper for ChromaDB EmbeddingFunction
│   ├── retriever.py             # Vector similarity search (standalone + singleton variants)
│   ├── generator.py             # Prompt construction + Ollama HTTP call
│   ├── app.py                   # FastAPI app with singleton model/DB initialization
│   └── templates/
│       └── index.html           # Single-page dark-themed SOC UI
├── requirements.txt             # Python dependencies
└── CLAUDE.md                    # Claude Code project context
```
