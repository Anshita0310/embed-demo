from app.embeddings import EmbeddingModel
from app.qdrant_client import get_qdrant_client
from app.config import COLLECTION_NAME, TOP_K

embedder = EmbeddingModel()
client = get_qdrant_client()

def semantic_search(query: str, top_k: int = TOP_K):
    query_vector = embedder.encode([query])[0]

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=top_k,
        with_payload=True
    )

    return response.points