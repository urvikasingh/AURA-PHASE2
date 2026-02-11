from backend.db.connection import get_connection


def get_user_preferences(user_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT preference_key, preference_value FROM user_preferences WHERE user_id = ?",
        user_id
    )

    rows = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in rows}


def save_user_preference(user_id: int, key: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        MERGE user_preferences AS target
        USING (SELECT ? AS user_id, ? AS preference_key) AS source
        ON target.user_id = source.user_id
           AND target.preference_key = source.preference_key
        WHEN MATCHED THEN
            UPDATE SET preference_value = ?, updated_at = GETDATE()
        WHEN NOT MATCHED THEN
            INSERT (user_id, preference_key, preference_value)
            VALUES (?, ?, ?);
    """,
        user_id,          # source.user_id
        key,              # source.preference_key
        value,            # UPDATE preference_value
        user_id,          # INSERT user_id
        key,              # INSERT preference_key
        value             # INSERT preference_value
    )

    conn.commit()
    conn.close()
