import httpx

from src.config import OLLAMA_MODEL, OLLAMA_URL

SYSTEM_PROMPT = (
    "You are an assistant for a Security Operations Center. "
    "Answer the question based ONLY on the provided context. "
    "If the context does not contain enough information to answer, say so clearly. "
    "Always cite which document(s) your answer comes from."
)


def build_prompt(query: str, context_chunks: list[dict]) -> str:
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
    prompt = build_prompt(query, context_chunks)

    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120.0,
        )
        response.raise_for_status()
    except httpx.ConnectError:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. "
            "Make sure Ollama is running: ollama serve"
        )

    data = response.json()
    sources = list({chunk["source"] for chunk in context_chunks})

    return {
        "answer": data["response"],
        "sources": sources,
        "query": query,
    }
