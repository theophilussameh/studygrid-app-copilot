from datetime import datetime

from monitoring.db_init import get_db_connection, DB_TIMEZONE


def save_feedback(conversation_id, source, relevance=None,
                   explanation=None, score=None, cost=None):
    timestamp = datetime.now(DB_TIMEZONE)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO feedback (
                    conversation_id, source, relevance,
                    explanation, score, cost, timestamp
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (conversation_id, source, relevance,
                 explanation, score, cost, timestamp),
            )
        conn.commit()
    finally:
        conn.close()