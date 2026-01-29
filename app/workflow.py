def decide_workflow(confidence: float):
    if confidence >= 0.75:
        return "AUTO_EXECUTE_INTENT"
    elif confidence >= 0.50:
        return "ASK_CLARIFICATION"
    else:
        return "FALLBACK_TO_HUMAN"
