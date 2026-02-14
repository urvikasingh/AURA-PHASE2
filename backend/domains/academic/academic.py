from backend.core.llm_client import generate_response
from backend.db.academic_memory_repository import get_or_create_academic_memory
from backend.db.chat_repository import get_conversation_messages
from backend.core.chat_context_builder import build_chat_context


ACADEMIC_SYSTEM_PROMPT = """
You are an excellent teacher who explains complex topics clearly and kindly.

Your goal is to help the student understand without overwhelming them
and without making them feel inadequate.

STRICT OUTPUT RULES (must follow exactly):

- NEVER write a long paragraph.
- Each paragraph must be at most 2 sentences.
- Leave a blank line between every section.
- Use simple language first, technical terms later.
- Stop once the core idea is understood.

REQUIRED STRUCTURE:

Intuition:
(2 short sentences explaining the idea simply)

Step-by-step:
1. One short step.
2. One short step.
3. One short step.

Example:
A simple, everyday example in 2 sentences.

Gentle follow-up:
One optional line inviting the student to continue.

Tone rules:
- Calm, respectful, and patient.
- Never condescending.
- Never say “this is simple” or “obviously”.

Naming:
- If addressed as “sir”, respond politely.
- Do not introduce yourself or insist on a name.
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

    # 2️⃣ Load academic preferences (defaults for now)
    academic_memory = get_or_create_academic_memory(user_id)

    explanation_style = academic_memory.get("explanation_style", "default")
    difficulty_level = academic_memory.get("difficulty_level", "intermediate")

    # 3️⃣ Load minimal conversation context (avoid token waste)
    history_block = ""
    if conversation_id:
        messages = get_conversation_messages(
            conversation_id=conversation_id,
            limit=2,  # IMPORTANT: keep academic context short
        )
        if messages:
            history_block = build_chat_context(messages)

    # 4️⃣ Build final prompt
    prompt = f"""
{ACADEMIC_SYSTEM_PROMPT}

Academic preferences:
- Explanation style: {explanation_style}
- Difficulty level: {difficulty_level}

Conversation context:
{history_block}

Question:
{message}

Provide a clear academic explanation suitable for a learner.
"""

    academic_generation_config = {
        "temperature": 0.3,
        "max_output_tokens": 700,
    }

    return generate_response(
        prompt,
        generation_config=academic_generation_config,
    )
