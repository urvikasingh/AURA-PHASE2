import os
import re
from backend.db.connection import get_connection


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
    Memory Gate v1.2
    - USP only
    - Silent name memory
    - Sticky identity (no auto-overwrite)
    """

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

        # If name exists and is different → ignore (no overwrite)

    finally:
        conn.close()
