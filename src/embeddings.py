"""Embedding function that integrates sentence-transformers with ChromaDB.

ChromaDB requires an object implementing its EmbeddingFunction protocol (a callable
that takes a list of strings and returns a list of float vectors). This module wraps
sentence-transformers to satisfy that interface, so ChromaDB can automatically embed
documents during both storage (add) and retrieval (query).
"""

from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL


class SentenceTransformerEmbedding(EmbeddingFunction[Documents]):
    """Wraps a sentence-transformers model to serve as a ChromaDB embedding function.

    Instantiating this class loads the model into memory (~90MB for MiniLM).
    The same instance should be reused across calls to avoid reloading the model.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: Documents) -> Embeddings:
        """Called automatically by ChromaDB when adding or querying documents."""
        return self.encode(input)

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Convert a list of text strings into embedding vectors.

        Returns a plain list of lists (not numpy arrays) because ChromaDB
        expects JSON-serializable types.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
