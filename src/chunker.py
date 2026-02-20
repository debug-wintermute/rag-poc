"""Text chunking for the ingestion pipeline.

Splits long documents into fixed-size overlapping chunks suitable for embedding.
The overlap ensures that sentences near chunk boundaries appear in at least two
chunks, reducing the chance of losing context at the edges.
"""


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks with word-boundary safety.

    Args:
        text: The full document text to chunk.
        chunk_size: Target number of characters per chunk.
        overlap: Number of characters to repeat between consecutive chunks.

    Returns:
        A list of text chunks. Empty/whitespace-only chunks are excluded.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        if end < text_len:
            # Avoid splitting in the middle of a word by scanning backward from
            # the cut point to find the nearest space. rfind returns the highest
            # index of " " in text[start:end], so we break at a word boundary.
            space_pos = text.rfind(" ", start, end)
            if space_pos > start:
                end = space_pos
        else:
            # Last chunk: just take everything remaining
            end = text_len

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        # Move the window forward, but step back by `overlap` characters so
        # the next chunk repeats the tail of this one
        start = end - overlap

    return chunks
