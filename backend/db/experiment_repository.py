from backend.db.connection import get_connection


def log_experiment(
    user_id: int,
    conversation_id: int,
    domain: str,
    memory_triggered: bool,
    latency_ms: float,
    input_length: int,
    output_length: int,
):
    """
    Research-only logging.
    Does NOT affect application behavior.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO experiment_logs
        (
            user_id,
            conversation_id,
            domain,
            memory_triggered,
            latency_ms,
            input_length,
            output_length
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            conversation_id,
            domain,
            int(memory_triggered),
            latency_ms,
            input_length,
            output_length,
        )
    )

    conn.commit()
    conn.close()
