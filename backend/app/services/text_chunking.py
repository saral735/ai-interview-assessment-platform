def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[str]:
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum approximate number of characters
        in each chunk.

    chunk_overlap:
        Number of characters shared between
        consecutive chunks.
    """

    if not text or not text.strip():
        return []

    text = text.strip()

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks