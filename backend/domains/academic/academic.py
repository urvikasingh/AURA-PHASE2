from backend.core.llm_client import generate_response
from backend.db.academic_memory_repository import get_or_create_academic_memory
from backend.db.chat_repository import get_conversation_messages
from backend.core.chat_context_builder import build_chat_context


ACADEMIC_SYSTEM_PROMPT = """
You are an excellent teacher who explains concepts clearly and patiently.

You MUST follow the output format EXACTLY.
If the format is violated, the answer is incorrect.

ABSOLUTE FORMATTING RULES (NON-NEGOTIABLE):

- Each section MUST start on a new line.
- There MUST be a blank line between sections.
- NEVER merge sections into one paragraph.
- NEVER stop mid-list.
- COMPLETE all sections fully.

REQUIRED STRUCTURE (USE THIS EXACTLY):

Intuition:
(Exactly 2 short sentences.)

(blank line)

Step-by-step:
1. One complete short sentence.
2. One complete short sentence.
3. One complete short sentence.

(blank line)

Example:
Exactly 2 sentences using a simple, real-life example.

(blank line)

Gentle follow-up:
One short inviting sentence.

LANGUAGE RULES:
- Simple words first, technical words later.
- Calm and respectful tone.
- Never say “obviously” or “this is simple”.
- Do not introduce yourself.
"""


def academic_handler(
    message: str,
    user_id: int,
    conversation_id: int | None = None,
) -> str:
    """
    Academic domain handler.
    Polite, professional tutor-style responses.
    """

    normalized = message.strip().lower()

    # 1️⃣ Polite handling of greetings (NOT USP-style)
    if normalized in {"hi", "hello", "hey", "hii"}:
        return "Hello. What academic topic or question would you like help with?"

    # 2️⃣ Load academic preferences
    academic_memory = get_or_create_academic_memory(user_id)

    explanation_style = academic_memory.get("explanation_style", "step_by_step")
    difficulty_level = academic_memory.get("difficulty_level", "beginner")

    # 3️⃣ Load minimal conversation context
    history_block = ""
    if conversation_id:
        messages = get_conversation_messages(
            conversation_id=conversation_id,
            limit=2,
        )
        if messages:
            history_block = build_chat_context(messages)

    # 4️⃣ BUILD PROMPT (RULES AT THE END — CRITICAL)
    prompt = f"""
You are answering an academic question.

Academic preferences:
- Explanation style: {explanation_style}
- Difficulty level: {difficulty_level}

Conversation context:
{history_block}

Question:
{message}

IMPORTANT — YOU MUST FOLLOW THESE OUTPUT RULES EXACTLY:
{ACADEMIC_SYSTEM_PROMPT}
"""

    academic_generation_config = {
        "temperature": 0.3,
        "max_output_tokens": 1200,
    }

    raw_response = generate_response(
        prompt,
        generation_config=academic_generation_config,
    )

    from backend.domains.academic.formatter import enforce_academic_format
    return enforce_academic_format(raw_response)