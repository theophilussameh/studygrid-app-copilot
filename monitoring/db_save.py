from datetime import datetime

from monitoring.db_init import get_db_connection, DB_TIMEZONE


def save_conversation(record, app="studygrid"):
    """
    Inserts an LLMCallRecord (from monitoring/metrics.py) as one row.
    Returns the new row's id — needed later to attach feedback to the
    right conversation.
    """
    timestamp = datetime.now(DB_TIMEZONE)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations (
                    question, answer, app, model, instructions,
                    llm_calls, prompt_tokens, completion_tokens, total_tokens,
                    response_time, cost, timestamp
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
                """,
                (
                    record.question,
                    record.answer,
                    app,
                    record.model,
                    record.instructions,
                    record.llm_calls,
                    record.prompt_tokens,
                    record.completion_tokens,
                    record.total_tokens,
                    record.response_time,
                    record.cost,
                    timestamp,
                ),
            )
            conversation_id = cur.fetchone()[0]
        conn.commit()
    finally:
        conn.close()
    return conversation_id