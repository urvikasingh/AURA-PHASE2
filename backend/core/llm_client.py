import os

# Optional config import (CI-safe)
try:
    from backend.config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_response(
    full_prompt: str,
    generation_config: dict | None = None
) -> str:
    """
    Shared LLM wrapper.
    - USP uses default config
    - Academic / other domains pass their own config
    - TEST_MODE returns deterministic outputs
    """

    # 🧪 TEST MODE
    if os.getenv("TEST_MODE") == "true":
        prompt_lower = full_prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello. How can I help you today?"

        if "ceo" in prompt_lower or "who is my" in prompt_lower:
            return "I don’t have enough information to answer that."

        if "medicine" in prompt_lower or "chest pain" in prompt_lower:
            return "I can’t provide medical advice. Please consult a doctor."

        if "gravity" in prompt_lower:
            return "Gravity is a force that attracts objects toward each other."

        return "I’m here to help."

    # 🚀 REAL MODE (Gemini)
    try:
        from google import genai

        if not GEMINI_API_KEY:
            return "LLM is not configured properly."

        client = genai.Client(api_key=GEMINI_API_KEY)

        # ✅ Default config (USP-friendly)
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

        # ✅ Collect ALL text safely (no truncation)
        full_text = ""

        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                if hasattr(candidate, "content"):
                    for part in candidate.content.parts:
                        if hasattr(part, "text"):
                            full_text += part.text

        if not full_text.strip():
            return "I’m having trouble generating a response right now."

        return full_text.strip()

    except Exception as e:
        print("Gemini error:", repr(e))
        return "LLM is temporarily unavailable."
