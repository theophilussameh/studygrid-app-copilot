import os
from datetime import datetime

import psycopg

DB_TIMEZONE = datetime.now().astimezone().tzinfo
print(f"Using timezone: {DB_TIMEZONE}")


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "gridmind"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
    )


def init_db(drop=False):
    """
    Creates the `conversations` table — one row per user question
    (per `agent.chat()` call), matching monitoring/metrics.py's
    LLMCallRecord. Differences from the course's version:
      - `question` instead of `prompt`, since the agent builds a
        multi-turn messages list, not a single prompt string.
      - `app` instead of `course`, defaulting to 'studygrid' — kept
        for when/if GridMind serves more than one app.
      - `llm_calls`: how many times the agent hit the model for this
        one question (the agentic loop can call it more than once).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if drop:
                cur.execute("DROP TABLE IF EXISTS conversations")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    app TEXT NOT NULL DEFAULT 'studygrid',
                    model TEXT NOT NULL,
                    instructions TEXT NOT NULL,
                    llm_calls INTEGER NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    response_time FLOAT NOT NULL,
                    cost FLOAT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")