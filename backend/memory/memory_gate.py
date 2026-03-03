import os
import re
from backend.db.connection import get_connection

# =========================
# 🧪 RESEARCH FLAGS (CAL v1.3)
# =========================
_memory_written = False
_memory_accessed = False


# =========================
# 🎯 NAME EXTRACTION RULES
# =========================
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


# =========================
# 🧠 MEMORY GATE (WRITE PATH)
# =========================
def run_memory_gate(*, user_id: int, message: str, domain: str):
    """
    Contextual Authorisation Layer (CAL) v1.3

    Behavior:
    - USP domain only
    - Explicit identity memory only (display_name)
    - Silent memory (no confirmation)
    - Sticky identity (no overwrite)
    - Research-safe instrumentation
    """

    global _memory_written, _memory_accessed

    # 🔄 Reset flags at start of each call
    _memory_written = False
    _memory_accessed = False

    # 🧪 Test safety
    if os.getenv("TEST_MODE") == "true":
        return

    # 🎯 Domain scope
    if domain != "usp":
        return

    # 🔍 Extract explicit name signal
    name = extract_name(message)
    if not name:
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔎 Check if identity already exists
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

        # 🧠 Write memory ONLY if not present
        if not row:
            cursor.execute(
                """
                INSERT INTO user_preferences (user_id, preference_key, preference_value)
                VALUES (?, 'display_name', ?)
                """,
                (user_id, name),
            )
            conn.commit()

            # ✅ MEMORY WRITE TRIGGERED
            _memory_written = True

        # If already exists → do nothing (no overwrite, no trigger)

    finally:
        conn.close()


# =========================
# 🧠 MEMORY ACCESS MARKER (READ PATH)
# =========================
def mark_memory_accessed():
    """
    Called ONLY when stored memory is actually used
    (e.g., name injected into USP response).
    """
    global _memory_accessed
    _memory_accessed = True


# =========================
# 🧪 RESEARCH HELPER
# =========================
def was_memory_triggered() -> bool:
    """
    Used ONLY for experiment logging.

    Returns True if memory was:
    - written OR
    - accessed (read)

    Resets flags after read.
    """
    global _memory_written, _memory_accessed

    value = _memory_written or _memory_accessed

    _memory_written = False
    _memory_accessed = False

    return value
