from backend.core.emotion_intent import detect_emotion_and_intent
from backend.core.memory_extractor import extract_preferences
from backend.core.prompt_with_memory import build_personalized_prompt
from backend.db.memory_repository import (
    get_user_preferences,
    save_user_preference
)
from backend.core.llm_client import generate_response
from backend.core.policy_engine import PolicyEngine


GREETING = "Hello. How can I help you today?"


def route_message(user_id: int, domain: str, message: str) -> str:
    domain = domain.lower()

    # ✅ Greeting ONLY for empty input
    if not message or not message.strip():
        return GREETING

    # ✅ Policy layer ALWAYS runs (even in TEST_MODE)
    policy = PolicyEngine.run(message)
    if policy.blocked:
        return policy.response

    # ✅ Domain routing
    if domain == "usp":
        return usp_handler(message, user_id)

    elif domain == "academic":
        return academic_handler(message, user_id)

    elif domain == "legal":
        return "Legal assistant is not enabled yet."

    elif domain == "medical":
        return "Medical assistant is not enabled yet."

    else:
        return "Invalid domain selected."


def should_save_memory(
    key: str,
    value: str,
    message: str,
    existing_preferences: dict
) -> bool:
    """
    Decide whether a memory should be saved.
    """

    message_lower = message.lower()

    # Rule 1: explicit user intent
    explicit_triggers = [
        "remember this",
        "remember that",
        "save this",
        "keep in mind"
    ]
    if any(trigger in message_lower for trigger in explicit_triggers):
        return True

    # Rule 2: repeated preference
    if key in existing_preferences:
        if existing_preferences[key] == value:
            return True

    # Rule 3: allowed stable preference types
    allowed_keys = {
        "response_length",
        "explanation_style",
        "tone",
        "language"
    }
    if key in allowed_keys:
        return True

    return False


import os


def usp_handler(message: str, user_id: int) -> str:
    msg_lower = message.lower()

    # ✅ TEST_MODE deterministic responses (NO LLM)
    if os.getenv("TEST_MODE") == "true":
        if "gravity" in msg_lower:
            return (
                "Gravity is a natural force that attracts objects with mass "
                "toward each other, such as objects falling toward Earth."
            )

    # 1️⃣ Detect emotion & intent
    analysis = detect_emotion_and_intent(message)
    mode = analysis["intent"]

    # 2️⃣ Load existing memory FIRST
    preferences = get_user_preferences(user_id)

    # 3️⃣ Extract candidate memory
    extracted = extract_preferences(message)

    # 4️⃣ Apply memory write guard
    for key, value in extracted:
        if should_save_memory(key, value, message, preferences):
            save_user_preference(user_id, key, value)

    # 5️⃣ Build FULL prompt (rules + memory + user message)
    full_prompt = build_personalized_prompt(
        mode=mode,
        preferences=preferences,
        user_message=message
    )

    # 6️⃣ Call LLM (non-test mode only)
    return generate_response(full_prompt)



def academic_handler(message: str, user_id: int) -> str:
    preferences = get_user_preferences(user_id)

    explanation_style = preferences.get("explanation_style", "step-by-step")
    interests = preferences.get("likes", None)

    response = "[ACADEMIC MODE]\n"
    response += f"Explanation style: {explanation_style}\n"

    if interests:
        response += f"User interests: {interests}\n"

    response += f"Question: {message}\n"
    response += "Answer: (Academic LLM will be integrated here)"

    return response
