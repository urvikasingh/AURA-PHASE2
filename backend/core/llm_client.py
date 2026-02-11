import os

# Optional config import (CI-safe)
try:
    from backend.config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_response(full_prompt: str) -> str:
    """
    LLM wrapper.
    - Real Gemini in prod/dev
    - Deterministic stub in TEST_MODE
    """

    # 🧪 TEST MODE: return deterministic responses
    if os.getenv("TEST_MODE") == "true":
        prompt_lower = full_prompt.lower()

        # Greeting
        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello. How can I help you today?"

        # Hallucination refusal
        if "ceo" in prompt_lower or "who is my" in prompt_lower:
            return "I don’t have enough information to answer that."

        # Medical refusal
        if "medicine" in prompt_lower or "chest pain" in prompt_lower:
            return "I can’t provide medical advice. Please consult a doctor."

        # General knowledge fallback
        if "gravity" in prompt_lower:
            return "Gravity is a force that attracts objects toward each other."

        return "I’m here to help."

    # 🚀 REAL MODE (Gemini)
    try:
        from google import genai

        if not GEMINI_API_KEY:
            return "LLM is not configured properly."

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=full_prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 300
            }
        )

        if not response or not response.text:
            return "I’m having trouble generating a response right now."

        return response.text.strip()

    except Exception as e:
        print("Gemini error:", repr(e))
        return "LLM is temporarily unavailable."
