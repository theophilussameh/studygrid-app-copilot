import sys
from pathlib import Path

# app.py lives in monitoring/, but config.py (and everything it wires
# together) lives at the project root. Streamlit only puts this file's
# own directory on sys.path, so we add the parent (project root)
# ourselves — otherwise `from config import agent` fails no matter
# where you run the command from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from config import agent
from monitoring.db_save import save_conversation
from monitoring.db_feedback import save_feedback
from monitoring.judge import evaluate_relevance

st.set_page_config(page_title="GridMind", page_icon="🎓")
st.title("GridMind — StudyGrid Assistant")

# NOTE: this history is UI-only, for display. `agent.chat()` builds a
# fresh [system, user] messages list on every call (see agent.py) — it
# does not see earlier turns. So the assistant currently answers each
# question independently, with no memory of the conversation so far.
# That's fine for a FAQ-style assistant, but worth knowing before you
# rely on follow-up questions like "and what about groups?" working.
if "messages" not in st.session_state:
    st.session_state.messages = []

# One shared function, used both for past messages and the one we
# just answered — key_suffix must be unique per button on the page,
# or Streamlit throws a DuplicateWidgetID error on rerun.
def render_feedback_buttons(conversation_id, key_suffix):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍", key=f"up_{key_suffix}"):
            save_feedback(conversation_id, "user", score=1)
            st.toast("شكرًا على رأيك!")
    with col2:
        if st.button("👎", key=f"down_{key_suffix}"):
            save_feedback(conversation_id, "user", score=-1)
            st.toast("شكرًا، هنحاول نحسّن الإجابة.")


for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "metrics" in msg:
            st.caption(msg["metrics"])
        if msg["role"] == "assistant" and msg.get("relevance"):
            st.caption(f"🧑‍⚖️ Judge: {msg['relevance']}")
        if msg["role"] == "assistant" and msg.get("conversation_id"):
            render_feedback_buttons(msg["conversation_id"], key_suffix=f"hist_{i}")

question = st.chat_input("اسأل حاجة عن StudyGrid...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("بدور في الإجابة..."):
            answer = agent.chat(question)
        st.write(answer)

        record = agent.last_call
        metrics_line = (
            f"⏱ {record.response_time:.2f}s · "
            f"🔁 {record.llm_calls} LLM call(s) · "
            f"🔢 {record.total_tokens} tokens · "
            f"💰 ${record.cost:.5f}"
        )
        st.caption(metrics_line)

        conversation_id = save_conversation(record)

        # NOTE (same caveat as the lesson): this runs inline, so it adds
        # a real LLM call's worth of latency and cost to every question.
        # In production you'd return the answer first and judge it in
        # the background, or sample only a fraction of questions.
        relevance, explanation, judge_cost = evaluate_relevance(question, answer)
        save_feedback(
            conversation_id, "judge",
            relevance=relevance, explanation=explanation, cost=judge_cost,
        )
        st.caption(f"🧑‍⚖️ Judge: {relevance}")

        render_feedback_buttons(conversation_id, key_suffix=f"new_{conversation_id}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "metrics": metrics_line,
        "conversation_id": conversation_id,
        "relevance": relevance,
    })