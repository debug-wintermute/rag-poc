import chromadb

from src.config import CHROMA_DIR, COLLECTION_NAME
from src.embeddings import SentenceTransformerEmbedding


def retrieve(query: str, n_results: int = 5) -> list[dict]:
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

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "title": results["metadatas"][0][i]["title"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
        })

    return chunks
