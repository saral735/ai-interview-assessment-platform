from fastembed import TextEmbedding


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


embedding_model = TextEmbedding(
    MODEL_NAME
)


def generate_embeddings(
    texts: list[str]
) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks.
    """

    if not texts:
        return []

    embeddings = embedding_model.embed(
        texts
    )

    return [
        embedding.tolist()
        for embedding in embeddings
    ]