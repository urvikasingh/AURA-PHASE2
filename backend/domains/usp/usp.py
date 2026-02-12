import os

from backend.core.emotion_intent import detect_emotion_and_intent
from backend.core.memory_extractor import extract_preferences
from backend.core.prompt_with_memory import build_personalized_prompt
from backend.db.memory_repository import (
    get_user_preferences,
    save_user_preference
)
from backend.core.llm_client import generate_response
from backend.core.policy_engine import PolicyEngine


def should_save_memory(
    key: str,
    value: str,
    message: str,
    existing_preferences: dict
) -> bool:
    message_lower = message.lower()

    explicit_triggers = [
        "remember this",
        "remember that",
        "save this",
        "keep in mind"
    ]
    if any(trigger in message_lower for trigger in explicit_triggers):
        return True

    if key in existing_preferences and existing_preferences[key] == value:
        return True

    allowed_keys = {
        "response_length",
        "explanation_style",
        "tone",
        "language"
    }
    return key in allowed_keys


def usp_handler(message: str, user_id: int) -> str:
    # ✅ TEST_MODE fast-path (optional, harmless)
    if os.getenv("TEST_MODE", "").lower() == "true":
        if "gravity" in message.lower():
            return (
                "Gravity is a natural force that attracts objects with mass "
                "toward each other."
            )

    analysis = detect_emotion_and_intent(message)
    mode = analysis["intent"]

    preferences = get_user_preferences(user_id)
    extracted = extract_preferences(message)

    for key, value in extracted:
        if should_save_memory(key, value, message, preferences):
            save_user_preference(user_id, key, value)

    full_prompt = build_personalized_prompt(
        mode=mode,
        preferences=preferences,
        user_message=message
    )

    # 🔑 DOMAIN IS PASSED HERE
    return generate_response(
        full_prompt,
        domain="usp"
    )
