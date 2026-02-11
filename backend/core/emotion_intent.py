def detect_emotion_and_intent(message: str) -> dict:
    msg = message.lower()

    # Emotion detection (simple & reliable)
    if any(word in msg for word in ["sad", "demotivated", "tired", "low", "anxious"]):
        emotion = "low"
    elif any(word in msg for word in ["angry", "frustrated", "irritated"]):
        emotion = "frustrated"
    else:
        emotion = "neutral"

    # Intent detection
    if any(word in msg for word in ["remind", "schedule", "plan", "todo"]):
        intent = "assistant"
    elif any(word in msg for word in ["how", "explain", "what is", "why"]):
        intent = "thinker"
    elif emotion == "low":
        intent = "friend"
    else:
        intent = "motivator"

    return {
        "emotion": emotion,
        "intent": intent
    }
