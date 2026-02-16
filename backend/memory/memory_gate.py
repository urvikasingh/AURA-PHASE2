import os
import re
from backend.db.connection import get_connection

# =========================
# 🧪 RESEARCH FLAG (NEW)
# =========================
_memory_triggered = False


NAME_PATTERNS = [
    r"\bmy name is ([A-Za-z]{2,})",
    r"\bi am called ([A-Za-z]{2,})",
    r"\bi'm called ([A-Za-z]{2,})",
]


def extract_name(message: str) -> str | None:
    for pattern in NAME_PATTERNS:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
    return None


def run_memory_gate(*, user_id: int, message: str, domain: str):
    """
    Memory Gate v1.2 + Research Instrumentation

    - USP only
    - Silent name memory
    - Sticky identity (no auto-overwrite)
    - Research-safe memory trigger flag
    """

    global _memory_triggered

    # 🔄 Reset flag at start of each call
    _memory_triggered = False

    # 🧪 Test safety
    if os.getenv("TEST_MODE") == "true":
        return

    # 🎯 Domain scope
    if domain != "usp":
        return

    # 🔍 Extract name
    name = extract_name(message)
    if not name:
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔎 Check if name already exists
        cursor.execute(
            """
            SELECT preference_value
            FROM user_preferences
            WHERE user_id = ?
              AND preference_key = 'display_name'
            """,
            (user_id,),
        )
        row = cursor.fetchone()

        # 🧠 Save ONLY if name does not exist yet
        if not row:
            cursor.execute(
                """
                INSERT INTO user_preferences (user_id, preference_key, preference_value)
                VALUES (?, 'display_name', ?)
                """,
                (user_id, name),
            )
            conn.commit()

            # ✅ MEMORY WAS TRIGGERED (RESEARCH)
            _memory_triggered = True

        # If name exists → ignore (no overwrite, no trigger)

    finally:
        conn.close()


# =========================
# 🧪 RESEARCH HELPER (NEW)
# =========================
def was_memory_triggered() -> bool:
    """
    Used ONLY for experiment logging.
    Returns whether memory was written in this turn.
    Resets flag after read.
    """
    global _memory_triggered
    value = _memory_triggered
    _memory_triggered = False
    return value
