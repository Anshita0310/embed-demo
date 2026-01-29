from fastapi import FastAPI
from app.search import semantic_search
from app.confidence import calculate_confidence
from app.workflow import decide_workflow

app = FastAPI(title="Local Semantic Intent Search")

@app.get("/predict")
def predict_intent(query: str):
    results = semantic_search(query)

    confidence = calculate_confidence(results)
    workflow = decide_workflow(confidence)

    return {
        "query": query,
        "predicted_label": results[0].payload["label"],
        "confidence": confidence,
        "workflow": workflow,
        "top_matches": [
            {
                "text": r.payload["text"],
                "label": r.payload["label"],
                "score": round(r.score, 3)
            }
            for r in results
        ]
    }
