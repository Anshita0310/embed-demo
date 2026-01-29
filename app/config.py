import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QDRANT_PATH = os.path.join(BASE_DIR, "qdrant_data")

COLLECTION_NAME = "banking77"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_SIZE = 384

TOP_K = 3