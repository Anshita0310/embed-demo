from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import QDRANT_PATH, COLLECTION_NAME, VECTOR_SIZE
import os

def get_qdrant_client():
    os.makedirs(QDRANT_PATH, exist_ok=True)
    return QdrantClient(path=QDRANT_PATH)

def create_collection(client):
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )