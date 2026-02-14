import pyodbc
from backend.db.connection import get_connection


def create_user(email: str, password_hash: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (email, password_hash),
        )
        conn.commit()

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        )
        user_id = cursor.fetchone()[0]
        return user_id

    except pyodbc.IntegrityError:
        return None

    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        (email,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email FROM users WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()
    conn.close()
    return user
