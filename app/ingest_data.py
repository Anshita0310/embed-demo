from datasets import load_dataset
from app.embeddings import EmbeddingModel
from app.qdrant_client import get_qdrant_client, create_collection
from app.config import COLLECTION_NAME

def ingest():
    print("Loading Banking77 dataset...")
    dataset = load_dataset("polyai/banking77")
    train_data = dataset["train"]

    embedder = EmbeddingModel()
    client = get_qdrant_client()

    create_collection(client)

    print("Generating embeddings...")
    embeddings = embedder.encode(train_data["text"])

    points = []
    for idx, vector in enumerate(embeddings):
        points.append({
            "id": idx,
            "vector": vector.tolist(),
            "payload": {
                "text": train_data[idx]["text"],
                "label": int(train_data[idx]["label"])
            }
        })

    print("Storing vectors locally in Qdrant...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ Ingestion completed!")

if __name__ == "__main__":
    ingest()
