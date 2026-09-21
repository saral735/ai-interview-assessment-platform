
import uuid

from qdrant_client.models import PointStruct

from app.core.config import settings
from app.services.qdrant import qdrant_client


def store_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    candidate_id: int,
    document_type: str = "resume"
) -> int:
    """
    Store resume chunks and embeddings in Qdrant.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count must be equal"
        )

    if not chunks:
        return 0

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        point_id = str(uuid.uuid4())

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "candidate_id": candidate_id,
                    "document_type": document_type,
                    "text": chunk
                }
            )
        )

    qdrant_client.upsert(
        collection_name=settings.qdrant_collection_name,
        points=points
    )

    return len(points)


def store_job_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    job_id: int
) -> int:
    """
    Store Job Description chunks and embeddings in Qdrant.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count must be equal"
        )

    if not chunks:
        return 0

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        point_id = str(uuid.uuid4())

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "job_id": job_id,
                    "document_type": "job_description",
                    "text": chunk
                }
            )
        )

    qdrant_client.upsert(
        collection_name=settings.qdrant_collection_name,
        points=points
    )

    return len(points)


def search_similar_chunks(
    query_embedding: list[float],
    candidate_id: int,
    limit: int = 3
) -> list[dict]:
    """
    Search relevant resume chunks for a candidate.
    """

    if not query_embedding:
        return []

    results = qdrant_client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_embedding,
        query_filter={
            "must": [
                {
                    "key": "candidate_id",
                    "match": {
                        "value": candidate_id
                    }
                }
            ]
        },
        limit=limit,
        with_payload=True
    ).points

    return [
        {
            "text": result.payload.get("text", ""),
            "score": result.score
        }
        for result in results
    ]


def search_job_chunks(
    query_embedding: list[float],
    job_id: int,
    limit: int = 3
) -> list[dict]:
    """
    Search relevant Job Description chunks for a job.
    """

    if not query_embedding:
        return []

    results = qdrant_client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_embedding,
        query_filter={
            "must": [
                {
                    "key": "job_id",
                    "match": {
                        "value": job_id
                    }
                }
            ]
        },
        limit=limit,
        with_payload=True
    ).points

    return [
        {
            "text": result.payload.get("text", ""),
            "score": result.score
        }
        for result in results
    ]
def build_interview_context(
    query_embedding: list[float],
    candidate_id: int,
    job_id: int,
    limit: int = 3
) -> dict:
    """
    Retrieve relevant resume and job description
    chunks for interview context.
    """

    resume_chunks = search_similar_chunks(
        query_embedding=query_embedding,
        candidate_id=candidate_id,
        limit=limit
    )

    job_chunks = search_job_chunks(
        query_embedding=query_embedding,
        job_id=job_id,
        limit=limit
    )

    return {
        "resume_context": resume_chunks,
        "job_context": job_chunks
    }
