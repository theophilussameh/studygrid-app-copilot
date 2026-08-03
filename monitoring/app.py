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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "metrics" in msg:
            st.caption(msg["metrics"])

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

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "metrics": metrics_line,
        "conversation_id": conversation_id,
    })