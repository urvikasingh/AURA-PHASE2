def build_chat_context(messages: list[dict]) -> str:
    """
    Convert chat history into a clean text block for the LLM.
    """
    context_lines = []

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            context_lines.append(f"User: {content}")
        elif role == "assistant":
            context_lines.append(f"Assistant: {content}")

    return "\n".join(context_lines)
