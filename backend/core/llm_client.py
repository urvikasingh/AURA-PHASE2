import os

# =========================
# Environment flags
# =========================
TEST_MODE = os.getenv("TEST_MODE", "").lower() == "true"

# Optional config import (CI-safe)
try:
    from backend.config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_response(
    full_prompt: str,
    domain: str | None = None,
    generation_config: dict | None = None
) -> str:
    """
    Central LLM adapter.

    - Domain-aware
    - TEST_MODE-safe (no external API calls)
    - Production-safe (Gemini unchanged)
    """

    # =========================
    # 🧪 TEST MODE (NO GEMINI)
    # =========================
    if TEST_MODE:
        # 🔑 Academic domain stub
        if domain == "academic":
            return (
                "[ACADEMIC MODE]\n"
                "Explanation style: step-by-step\n"
                "Difficulty level: medium\n\n"
                "Answer:\n"
                "This is a test-safe academic explanation."
            )

        # 🔑 USP / general domain stub
        prompt_lower = full_prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello. How can I help you today?"

        if "gravity" in prompt_lower:
            return "Gravity is a force that attracts objects toward each other."

        return "I’m here to help."

    # =========================
    # 🚀 REAL MODE (Gemini)
    # =========================
    try:
        from google import genai

        if not GEMINI_API_KEY:
            return "LLM is not configured properly."

        client = genai.Client(api_key=GEMINI_API_KEY)

        if generation_config is None:
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 300,
            }

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=full_prompt,
            config=generation_config,
        )

        full_text = ""
        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                for part in getattr(candidate.content, "parts", []):
                    full_text += getattr(part, "text", "")

        if not full_text.strip():
            return "I’m having trouble generating a response right now."

        return full_text.strip()

    except Exception as e:
        print("Gemini error:", repr(e))
        return "LLM is temporarily unavailable."
