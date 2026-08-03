from dataclasses import dataclass

from monitoring.db_init import get_db_connection
from monitoring.metrics import LLMCallRecord


def row_to_record(row):
    return LLMCallRecord(
        model=row[4],
        question=row[1],
        instructions=row[5],
        answer=row[2],
        llm_calls=row[6],
        prompt_tokens=row[7],
        completion_tokens=row[8],
        total_tokens=row[9],
        response_time=row[10],
        cost=row[11],
        timestamp=row[12],
    )


def get_conversations(limit=10):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, question, answer, app, model,
                       instructions, llm_calls,
                       prompt_tokens, completion_tokens, total_tokens,
                       response_time, cost, timestamp
                FROM conversations
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [row_to_record(row) for row in rows]


def get_relevance_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT relevance, COUNT(*)
                FROM feedback
                WHERE source = 'judge'
                GROUP BY relevance
            """)
            rows = cur.fetchall()
    finally:
        conn.close()
    return dict(rows)


def get_user_feedback_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    SUM(CASE WHEN score > 0 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN score < 0 THEN 1 ELSE 0 END)
                FROM feedback
                WHERE source = 'user'
            """)
            row = cur.fetchone()
    finally:
        conn.close()
    return row[0] or 0, row[1] or 0


def get_judge_cost():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT SUM(cost) FROM feedback WHERE source = 'judge'
            """)
            row = cur.fetchone()
    finally:
        conn.close()
    return row[0] or 0


@dataclass
class Stats:
    total: int
    avg_response_time: float
    total_cost: float
    avg_tokens: float
    avg_llm_calls: float


def get_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*),
                    AVG(response_time),
                    SUM(cost),
                    AVG(total_tokens),
                    AVG(llm_calls)
                FROM conversations
            """)
            row = cur.fetchone()
    finally:
        conn.close()

    return Stats(
        total=row[0] or 0,
        avg_response_time=row[1] or 0,
        total_cost=row[2] or 0,
        avg_tokens=row[3] or 0,
        avg_llm_calls=row[4] or 0,
    )