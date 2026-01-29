# def calculate_confidence(results):
#     scores = [r.score for r in results]
#
#     if len(scores) == 1:
#         return round(scores[0], 3)
#
#     top = scores[0]
#     second = scores[1]
#
#     relative_gap = top - second
#     normalized = top / sum(scores)
#
#     confidence = (0.7 * normalized) + (0.3 * relative_gap)
#
#     return round(confidence, 3)
def calculate_confidence(results):
    scores = [r.score for r in results]
    labels = [r.payload["label"] for r in results]

    top = scores[0]

    # 🔥 NEW: if all top-K belong to same intent
    if len(set(labels)) == 1:
        return round(min(0.95, top), 3)

    # fallback to old logic
    second = scores[1]
    normalized = top / sum(scores)
    relative_gap = top - second

    confidence = (0.7 * normalized) + (0.3 * relative_gap)
    return round(confidence, 3)
