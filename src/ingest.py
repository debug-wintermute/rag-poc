import glob
import os
import re

import chromadb

from src.chunker import chunk_text
from src.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    DATA_DIR,
)
from src.embeddings import SentenceTransformerEmbedding


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"


def load_documents(data_dir: str) -> list[dict]:
    docs = []
    for filepath in sorted(glob.glob(os.path.join(data_dir, "*.md"))):
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        filename = os.path.basename(filepath)
        docs.append({
            "filename": filename,
            "title": extract_title(content),
            "path": filepath,
            "content": content,
        })
    return docs


def main():
    print("Loading documents...")
    docs = load_documents(DATA_DIR)
    print(f"Found {len(docs)} documents")

    print("Initializing embedding model...")
    embed_fn = SentenceTransformerEmbedding()

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Reset collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except (ValueError, chromadb.errors.NotFoundError):
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
    )

    all_ids = []
    all_documents = []
    all_metadatas = []

    for doc in docs:
        chunks = chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            all_ids.append(f"{doc['filename']}_{i}")
            all_documents.append(chunk)
            all_metadatas.append({
                "source": doc["filename"],
                "title": doc["title"],
                "chunk_index": i,
            })

    print(f"Adding {len(all_ids)} chunks to ChromaDB...")
    collection.add(ids=all_ids, documents=all_documents, metadatas=all_metadatas)

    print(f"\nDone! Processed {len(docs)} documents, created {len(all_ids)} chunks.")


if __name__ == "__main__":
    main()
