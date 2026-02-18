def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        if end < text_len:
            # Don't split mid-word: scan backward for nearest space
            space_pos = text.rfind(" ", start, end)
            if space_pos > start:
                end = space_pos
        else:
            end = text_len

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break

        start = end - overlap

    return chunks
