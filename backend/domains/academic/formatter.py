import re

def enforce_academic_format(text: str) -> str:
    if not text:
        return text

    text = text.strip()

    headers = [
        "Intuition:",
        "Step-by-step:",
        "Example:",
        "Gentle follow-up:",
    ]

    for h in headers:
        text = re.sub(rf"\s*{h}", f"\n\n{h}", text)

    text = re.sub(r"\s*(\d+\.)", r"\n\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()