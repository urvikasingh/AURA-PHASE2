def extract_preferences(message: str) -> list:
    msg = message.lower()
    memories = []

    if "i like " in msg:
        value = msg.split("i like ")[1].strip()
        memories.append(("likes", value))

    if "i prefer " in msg:
        value = msg.split("i prefer ")[1].strip()
        memories.append(("preference", value))

    if "i hate " in msg:
        value = msg.split("i hate ")[1].strip()
        memories.append(("dislikes", value))

    return memories
