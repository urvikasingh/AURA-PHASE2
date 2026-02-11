from backend.db.connection import get_connection


def create_user(email: str, password_hash: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (email, password_hash) OUTPUT INSERTED.id VALUES (?, ?)",
        email, password_hash
    )

    user_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return user_id


def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        email
    )

    row = cursor.fetchone()
    conn.close()

    return row
