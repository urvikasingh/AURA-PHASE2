from backend.db.connection import get_connection

print("LOADED chat_repository FROM:", __file__)

# =========================
# Conversations
# =========================

def create_conversation(user_id: int, domain: str) -> int:
    """
    Create a new conversation and return its ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (user_id, domain, has_greeted)
        OUTPUT INSERTED.id
        VALUES (?, ?, 0)
        """,
        (user_id, domain)
    )

    conversation_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return conversation_id


def get_user_conversations(user_id: int):
    """
    Fetch all conversations for a user (for sidebar).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, domain, created_at, updated_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "conversation_id": row.id,
            "domain": row.domain,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
        for row in rows
    ]


def update_conversation_timestamp(conversation_id: int):
    """
    Update updated_at when a new message arrives.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET updated_at = GETDATE()
        WHERE id = ?
        """,
        (conversation_id,)
    )

    conn.commit()
    conn.close()


def conversation_belongs_to_user(conversation_id: int, user_id: int) -> bool:
    """
    Check if a conversation belongs to a user.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM conversations
        WHERE id = ? AND user_id = ?
        """,
        (conversation_id, user_id)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def has_conversation_greeted(conversation_id: int) -> bool:
    """
    Check whether greeting was already used for this conversation.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT has_greeted
        FROM conversations
        WHERE id = ?
        """,
        (conversation_id,)
    )

    result = cursor.fetchone()
    conn.close()

    return bool(result[0]) if result else False


def mark_conversation_greeted(conversation_id: int):
    """
    Mark conversation as greeted.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET has_greeted = 1
        WHERE id = ?
        """,
        (conversation_id,)
    )

    conn.commit()
    conn.close()


# =========================
# Chat Messages
# =========================

def save_message(
    conversation_id: int,
    user_id: int,
    role: str,
    content: str,
):
    """
    Save a single chat message.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages
        (conversation_id, user_id, role, content)
        VALUES (?, ?, ?, ?)
        """,
        (conversation_id, user_id, role, content)
    )

    conn.commit()
    conn.close()


def get_conversation_messages(
    conversation_id: int,
    limit: int | None = None,
):
    """
    Fetch messages for a conversation.
    Used for LLM context and UI reload.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if limit:
        cursor.execute(
            """
            SELECT role, content, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY created_at DESC
            OFFSET 0 ROWS
            FETCH NEXT ? ROWS ONLY
            """,
            (conversation_id, limit)
        )
        rows = reversed(cursor.fetchall())
    else:
        cursor.execute(
            """
            SELECT role, content, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY created_at
            """,
            (conversation_id,)
        )
        rows = cursor.fetchall()

    conn.close()

    return [
        {
            "role": row.role,
            "content": row.content,
            "created_at": row.created_at,
        }
        for row in rows
    ]

def delete_conversation(conversation_id: int, user_id: int):
    """
    Delete a conversation and all its messages.
    Ensures the conversation belongs to the user.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Safety check: ownership
    cursor.execute(
        """
        SELECT 1
        FROM conversations
        WHERE id = ? AND user_id = ?
        """,
        (conversation_id, user_id)
    )

    if cursor.fetchone() is None:
        conn.close()
        raise PermissionError("Conversation does not belong to user")

    # Delete messages first (FK-safe)
    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE conversation_id = ?
        """,
        (conversation_id,)
    )

    # Delete conversation
    cursor.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        """,
        (conversation_id,)
    )

    conn.commit()
    conn.close()
