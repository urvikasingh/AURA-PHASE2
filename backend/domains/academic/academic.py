from backend.core.llm_client import generate_response
from backend.db.academic_memory_repository import get_or_create_academic_memory


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


def academic_handler(message: str, user_id: int) -> str:
    # 🔹 Load academic memory
    academic_memory = get_or_create_academic_memory(user_id)

    explanation_style = academic_memory.get("explanation_style", "default")
    difficulty_level = academic_memory.get("difficulty_level", "medium")

    prompt = f"""
{ACADEMIC_SYSTEM_PROMPT}

Academic preferences:
- Explanation style: {explanation_style}
- Difficulty level: {difficulty_level}

Question:
{message}

Answer:
"""

    academic_generation_config = {
        "temperature": 0.3,
        "max_output_tokens": 1024,
        "top_p": 0.9,
    }

    # 🔑 DOMAIN IS PASSED HERE (CRITICAL)
    return generate_response(
        prompt,
        domain="academic",
        generation_config=academic_generation_config,
    )
