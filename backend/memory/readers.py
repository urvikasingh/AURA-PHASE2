from backend.db.connection import get_connection


def get_display_name(user_id: int) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()

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
    conn.close()

    return row[0] if row else None
