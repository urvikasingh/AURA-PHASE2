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
    - TEST_MODE-safe
    - Gemini-compatible (NO system_instruction)
    """

    # =========================
    # 🧪 TEST MODE
    # =========================
    if TEST_MODE:
        return (
            "[TEST MODE]\n\n"
            "This is a safe, complete response.\n"
            "No external API call was made."
        )

    # =========================
    # 🚀 REAL MODE (Gemini)
    # =========================
    try:
        from google import genai

        if not GEMINI_API_KEY:
            return "LLM is not configured properly."

        client = genai.Client(api_key=GEMINI_API_KEY)

        # 🔒 Hard safety defaults
        final_config = {
            "temperature": 0.4,
            "max_output_tokens": 1200,
        }

        if generation_config:
            final_config.update(generation_config)

        # ❗ IMPORTANT:
        # Gemini expects ONE merged prompt
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=full_prompt,
            config=final_config,
        )

        # =========================
        # 🛡️ Safe parsing
        # =========================
        full_text = ""

        candidates = getattr(response, "candidates", None)
        if candidates:
            for candidate in candidates:
                content = getattr(candidate, "content", None)
                parts = getattr(content, "parts", []) if content else []
                for part in parts:
                    text = getattr(part, "text", "")
                    if text:
                        full_text += text

        if not full_text.strip():
            return "I’m having trouble generating a response right now."

        return full_text.strip()

    except Exception as e:
        print("Gemini error:", repr(e))
        return "LLM is temporarily unavailable."