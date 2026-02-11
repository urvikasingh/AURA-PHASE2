from backend.config import GEMINI_API_KEY

def generate_response(full_prompt: str) -> str:
    """
    Safe Gemini wrapper using NEW SDK.
    Never crashes backend.
    """
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
