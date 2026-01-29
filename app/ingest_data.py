import pandas as pd
from qdrant_client.models import PointStruct
from app.embeddings import EmbeddingModel
from app.qdrant_client import get_qdrant_client, create_collection
from app.config import COLLECTION_NAME

def ingest():
    print("Loading Banking77 dataset from Parquet...")
    
    # Download the Parquet file directly from Hugging Face
    train_url = "https://huggingface.co/datasets/PolyAI/banking77/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet"
    
    # Read the Parquet file
    df = pd.read_parquet(train_url)
    
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    print(f"Loaded {len(texts)} examples")
    
    embedder = EmbeddingModel()
    client = get_qdrant_client()
    
    create_collection(client)
    
    print("Generating embeddings...")
    embeddings = embedder.encode(texts)
    
    points = []
    for idx, vector in enumerate(embeddings):
        points.append(
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload={
                    "text": texts[idx],
                    "label": int(labels[idx])
                }
            )
        )
    
    print("Storing vectors locally in Qdrant...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    
    print("✅ Ingestion completed!")

if __name__ == "__main__":
    ingest()