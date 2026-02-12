from backend.db.connection import get_connection
import os


def get_academic_memory(user_id: int):
    """
    Fetch academic memory for a user.
    Returns a dict or None.
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT explanation_style, difficulty_level
        FROM academic_memory
        WHERE user_id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "explanation_style": row.explanation_style,
        "difficulty_level": row.difficulty_level,
    }


def create_default_academic_memory(user_id: int):
    """
    Create default academic memory for a user.
    Defaults are handled by the DB.
    """
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO academic_memory (user_id)
        VALUES (?)
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()


def get_or_create_academic_memory(user_id: int):
    """
    Get academic memory or create defaults if missing.
    In TEST_MODE, returns in-memory defaults (no DB access).
    """
    if os.getenv("TEST_MODE") == "true":
        return {
            "explanation_style": "default",
            "difficulty_level": "medium",
        }

    memory = get_academic_memory(user_id)
    if memory:
        return memory

    create_default_academic_memory(user_id)
    return get_academic_memory(user_id)


def update_academic_memory(
    user_id: int,
    explanation_style: str | None = None,
    difficulty_level: str | None = None,
):
    """
    Update academic memory fields if provided.
    """
    if not explanation_style and not difficulty_level:
        return

    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    if explanation_style:
        cursor.execute(
            """
            UPDATE academic_memory
            SET explanation_style = ?
            WHERE user_id = ?
            """,
            (explanation_style, user_id),
        )

    if difficulty_level:
        cursor.execute(
            """
            UPDATE academic_memory
            SET difficulty_level = ?
            WHERE user_id = ?
            """,
            (difficulty_level, user_id),
        )

    conn.commit()
    conn.close()
