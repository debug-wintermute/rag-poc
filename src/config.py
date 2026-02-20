"""Central configuration for the RAG pipeline.

All constants are plain module-level values — no environment variable loading.
Paths are relative to the repo root, so all commands must be run from there.
"""

# Where the source Markdown documents live
DATA_DIR = "data/confluence"

# Where ChromaDB persists its vector index and metadata to disk
CHROMA_DIR = "data/chroma"

# Chunking parameters: each document is split into overlapping text windows.
# 500 chars per chunk keeps context focused; 100 char overlap ensures
# sentences near chunk boundaries aren't lost.
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# The sentence-transformers model used to convert text into 384-dimensional vectors.
# "all-MiniLM-L6-v2" is small (~90MB) and fast on CPU while still accurate for
# semantic similarity tasks.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ChromaDB collection name — acts like a table name for our stored vectors
COLLECTION_NAME = "soc_docs"

# Ollama runs a local HTTP API for LLM inference
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"

# Number of most-similar chunks to retrieve per query.
# Higher values give more context but risk diluting relevance and slowing generation.
TOP_K = 5
