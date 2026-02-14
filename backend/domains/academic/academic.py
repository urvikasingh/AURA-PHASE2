from backend.core.llm_client import generate_response
from backend.db.academic_memory_repository import get_or_create_academic_memory
from backend.db.chat_repository import get_conversation_messages
from backend.core.chat_context_builder import build_chat_context


ACADEMIC_SYSTEM_PROMPT = """
You are an Academic Assistant.

You MUST follow this format strictly:
1. Definition (2–3 sentences)
2. Detailed explanation (step-by-step, numbered)
3. Example (with explanation)

Rules:
- Use formal academic language
- Avoid emojis, jokes, or casual tone
- Do not shorten answers
- Be explicit and structured
"""


def academic_handler(
    message: str,
    user_id: int,
    conversation_id: int | None = None,
) -> str:
    # 1️⃣ Load academic memory
    academic_memory = get_or_create_academic_memory(user_id)

    explanation_style = academic_memory.get("explanation_style", "step-by-step")
    difficulty_level = academic_memory.get("difficulty_level", "beginner")

    # 2️⃣ Load last N messages (if conversation exists)
    history_block = ""
    if conversation_id:
        messages = get_conversation_messages(
            conversation_id=conversation_id,
            limit=6,
        )
        history_block = build_chat_context(messages)

    # 3️⃣ Build final prompt
    prompt = f"""
{ACADEMIC_SYSTEM_PROMPT}

Academic preferences:
- Explanation style: {explanation_style}
- Difficulty level: {difficulty_level}

Conversation so far:
{history_block}

Question:
{message}

Answer:
"""

    academic_generation_config = {
        "temperature": 0.3,
        "max_output_tokens": 1024,
    }

    return generate_response(
        prompt,
        generation_config=academic_generation_config,
    )
