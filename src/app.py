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
    query: str


@app.on_event("startup")
def startup():
    embed_fn = SentenceTransformerEmbedding()
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn,
        )
    except (ValueError, chromadb.errors.InvalidCollectionException):
        collection = None

    app.state.collection = collection


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/query")
def query(body: QueryRequest):
    if not body.query.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Query cannot be empty."},
        )

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
        return JSONResponse(
            status_code=503,
            content={"error": str(e)},
        )

    return result
