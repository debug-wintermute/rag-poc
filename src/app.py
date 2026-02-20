"""FastAPI web application for the SOC Knowledge Base RAG interface.

Serves a single-page UI and exposes a POST endpoint for natural language queries.
On startup, initializes the embedding model and ChromaDB client once (singleton
pattern) to avoid reloading the ~90MB model on every HTTP request.
"""

import chromadb
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.config import CHROMA_DIR, COLLECTION_NAME
from src.embeddings import SentenceTransformerEmbedding
from src.generator import generate
from src.retriever import retrieve_with_collection

app = FastAPI(title="SOC Knowledge Base")
templates = Jinja2Templates(directory="src/templates")


class QueryRequest(BaseModel):
    """Request body for the /api/query endpoint."""
    query: str


@app.on_event("startup")
def startup():
    """Initialize shared resources once when the server starts.

    Loads the embedding model and opens the ChromaDB collection, storing both
    in app.state so every request handler can reuse them. Without this, each
    request would reload the model from disk (~seconds of latency per query).
    """
    embed_fn = SentenceTransformerEmbedding()
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn,
        )
    except (ValueError, chromadb.errors.InvalidCollectionException):
        # Collection doesn't exist — ingestion hasn't been run yet.
        # The app stays alive but will return 503 on queries.
        collection = None

    app.state.collection = collection


@app.get("/")
def index(request: Request):
    """Serve the single-page web UI."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/query")
def query(body: QueryRequest):
    """Accept a natural language query, retrieve context, and generate an answer.

    Pipeline: validate input → retrieve top-K chunks from ChromaDB → build
    prompt with context → call Ollama for generation → return answer + sources.
    """
    if not body.query.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Query cannot be empty."},
        )

    # If collection is None, ingestion was never run — tell the user how to fix it
    if app.state.collection is None:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Document collection not found. "
                "Run the ingestion pipeline first: python -m src.ingest"
            },
        )

    try:
        chunks = retrieve_with_collection(body.query, app.state.collection)
        result = generate(body.query, chunks)
    except RuntimeError as e:
        # RuntimeError is raised by the retriever/generator for known failures
        # (e.g., Ollama not running). Surface the message to the user.
        return JSONResponse(
            status_code=503,
            content={"error": str(e)},
        )

    return result
