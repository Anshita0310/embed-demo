def calculate_confidence(results):
    scores = [r.score for r in results]

    if len(scores) == 0:
        return 0.0
    
    if len(scores) == 1:
        return round(scores[0], 3)

    top = scores[0]
    second = scores[1]

    relative_gap = top - second
    normalized = top / sum(scores)

    confidence = (0.7 * normalized) + (0.3 * relative_gap)

    return round(confidence, 3)