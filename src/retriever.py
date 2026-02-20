"""Vector similarity search against the ChromaDB collection.

Provides two retrieval functions for different contexts:
- retrieve(): standalone version that opens its own ChromaDB client each call.
  Simple but slow — suitable for CLI scripts or one-off testing.
- retrieve_with_collection(): takes a pre-opened collection object, avoiding
  repeated client/model initialization. Used by the web app where the collection
  is initialized once at startup (singleton pattern).
"""

import chromadb

from src.config import CHROMA_DIR, COLLECTION_NAME, TOP_K
from src.embeddings import SentenceTransformerEmbedding


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """Retrieve similar chunks for a query, initializing a fresh client each call.

    This is the standalone version — it creates its own ChromaDB client and
    embedding model. Convenient for scripts but too slow for a web server
    (loading the embedding model takes seconds).

    Raises RuntimeError if the collection doesn't exist (ingestion not run yet).
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = SentenceTransformerEmbedding()

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embed_fn,
        )
    except (ValueError, chromadb.errors.InvalidCollectionException):
        raise RuntimeError(
            f"Collection '{COLLECTION_NAME}' not found. "
            "Run the ingestion pipeline first: python -m src.ingest"
        )

    results = collection.query(query_texts=[query], n_results=n_results)

    # ChromaDB returns nested lists because it supports batched queries.
    # We only send one query, so all our results are at index [0].
    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "title": results["metadatas"][0][i]["title"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
        })

    return chunks


def retrieve_with_collection(query: str, collection, n_results: int = TOP_K) -> list[dict]:
    """Retrieve similar chunks using a pre-initialized collection.

    This avoids reinitializing the embedding model and ChromaDB client on
    every request. The web app passes in a collection from app.state that
    was created once at startup.
    """
    results = collection.query(query_texts=[query], n_results=n_results)

    # Same nested-list unwrapping as retrieve() — index [0] for our single query
    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "title": results["metadatas"][0][i]["title"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
        })

    return chunks
