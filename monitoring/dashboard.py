import sys
from pathlib import Path

# Same reason as monitoring/app.py: this file lives in monitoring/, but
# imports the monitoring package itself, so the project root needs to
# be on sys.path regardless of where you run the command from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import asdict

import pandas as pd
import streamlit as st

from monitoring.db_query import (
    get_conversations,
    get_stats,
    get_relevance_stats,
    get_user_feedback_stats,
    get_judge_cost,
)

st.set_page_config(page_title="GridMind Dashboard", page_icon="📊")
st.title("GridMind Dashboard")

stats = get_stats()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total conversations", stats.total)
col2.metric("Avg response time", f"{stats.avg_response_time:.2f}s")
col3.metric("Total cost", f"${stats.total_cost:.4f}")
col4.metric("Avg tokens", f"{stats.avg_tokens:.0f}")
col5.metric("Avg LLM calls/question", f"{stats.avg_llm_calls:.1f}")

records = get_conversations(limit=100)

if records:
    df = pd.DataFrame([asdict(r) for r in records])

    st.subheader("Cost over time")
    st.line_chart(df, x="timestamp", y="cost")

    st.subheader("Response time over time")
    st.line_chart(df, x="timestamp", y="response_time")

    st.subheader("LLM calls per question")
    st.bar_chart(df, x="timestamp", y="llm_calls")
else:
    st.info("لسه مفيش بيانات كفاية — اسأل شوية أسئلة في الشات الأول.")

st.subheader("Recent conversations")
recent = get_conversations(limit=20)

for record in recent:
    st.write(f"**{record.question[:80]}**")
    st.write(f"{record.answer[:200]}...")
    st.write(
        f"⏱ {record.response_time:.2f}s | "
        f"🔁 {record.llm_calls} LLM call(s) | "
        f"💰 ${record.cost:.4f}"
    )
    st.divider()

st.subheader("Judge relevance")
relevance = get_relevance_stats()
if relevance:
    st.bar_chart(relevance)
else:
    st.info("لسه مفيش أحكام من الـ judge.")
st.caption(f"Total judge cost so far: ${get_judge_cost():.4f}")

st.subheader("User feedback")
thumbs_up, thumbs_down = get_user_feedback_stats()
col1, col2 = st.columns(2)
col1.metric("👍 Thumbs up", thumbs_up)
col2.metric("👎 Thumbs down", thumbs_down)