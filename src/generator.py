"""Prompt construction and LLM generation via Ollama's HTTP API.

Builds a prompt from retrieved context chunks and a user query, then sends it
to a locally running Ollama instance. The response is returned as a complete
string (non-streaming) — the user waits for the full answer before seeing anything.
"""

import httpx

from src.config import OLLAMA_MODEL, OLLAMA_URL

# The system prompt constrains the LLM to answer only from provided context,
# preventing hallucination and ensuring source attribution.
SYSTEM_PROMPT = (
    "You are an assistant for a Security Operations Center. "
    "Answer the question based ONLY on the provided context. "
    "If the context does not contain enough information to answer, say so clearly. "
    "Always cite which document(s) your answer comes from."
)


def build_prompt(query: str, context_chunks: list[dict]) -> str:
    """Assemble the full prompt string from context chunks and the user's query.

    Each chunk is prefixed with its source filename so the LLM can cite it.
    The system prompt, context block, and question are concatenated into a
    single prompt string (Ollama handles system/user separation internally
    when using the /api/generate endpoint).
    """
    context_parts = []
    for chunk in context_chunks:
        context_parts.append(f"[Source: {chunk['source']}]\n{chunk['text']}")

    context_block = "\n\n".join(context_parts)

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {query}"
    )


def generate(query: str, context_chunks: list[dict]) -> dict:
    """Send the query + context to Ollama and return the generated answer.

    Returns a dict with 'answer', 'sources' (deduplicated filenames), and 'query'.
    Raises RuntimeError if Ollama is not reachable.
    """
    prompt = build_prompt(query, context_chunks)

    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            # stream=False means we wait for the complete response. Simpler to handle
            # but the user sees nothing until generation finishes (up to 120s on CPU).
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120.0,
        )
        response.raise_for_status()
    except httpx.ConnectError:
        # Specific catch for connection failures — the most common error is
        # forgetting to start Ollama before querying
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. "
            "Make sure Ollama is running: ollama serve"
        )

    data = response.json()
    # Deduplicate source filenames using a set — multiple chunks may come from
    # the same document
    sources = list({chunk["source"] for chunk in context_chunks})

    return {
        "answer": data["response"],
        "sources": sources,
        "query": query,
    }
