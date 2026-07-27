# GridMind

AI Copilot for the [StudyGrid](https://github.com/0xezzdev/StudyGrid) app — an agentic Retrieval-Augmented Generation (RAG) assistant built with function calling and Large Language Models (LLMs).

This project is being developed step by step while studying the **LLM Zoomcamp** by **DataTalksClub**. Rather than simply reproducing the course notebooks, every concept is integrated into a real-world AI application, following software engineering practices such as modular design, separation of responsibilities, dependency injection, and reusable components.

---

## Problem

StudyGrid is a mobile app for students that combines group chat, class materials, shared/personal to-do lists, and notifications. Students frequently have simple, repetitive questions about how the app works — how to create a group, invite members, upload files, manage tasks, and so on.

Answering these manually (via support tickets or a static FAQ page) doesn't scale and isn't available 24/7. GridMind solves this by giving StudyGrid an AI assistant that:

- Understands a student's question, even when phrased differently from the FAQ wording (e.g. "add members" vs "invite people to a group")
- Decides on its own whether it needs to search the knowledge base before answering
- Answers only from verified StudyGrid information, refusing to answer questions outside the app's scope

The long-term goal is to embed GridMind directly into the StudyGrid app as its in-app help assistant.

---

## How it works (Agentic RAG with Function Calling)

Unlike a traditional RAG pipeline that always retrieves context before answering, GridMind is an **agent**: the LLM itself decides, at each step, whether it needs to call a tool (`search`) or whether it already has enough information to answer.

```text
                    User question
                         │
                         ▼
        ┌────────────────────────────────┐
        │   LLM (with available tools)    │◀─────────┐
        └────────────────────────────────┘          │
                         │                            │
             does it need a tool?                     │
             ┌───────────┴────────────┐               │
            yes                       no               │
             │                         │                │
             ▼                         ▼                │
     Execute tool (search)     Return final answer       │
             │                                          │
             ▼                                          │
   Add tool result to conversation ─────────────────────┘
```

The loop repeats — searching, re-searching with different keywords, or stopping — until the model is confident it can answer, or a maximum iteration count is reached as a safety net.

### Why an agent instead of plain RAG?

A plain RAG pipeline (one search, one answer) works well for straightforward questions, but can miss the right document when a student's phrasing doesn't match the FAQ wording. Giving the model control over when and how many times to search lets it recover from a bad first search (e.g. searching again with better keywords) — the same benefit documented in the LLM Zoomcamp's Agentic Loop lesson.

---

## Current Features

- Load a bilingual (English & Arabic) StudyGrid FAQ knowledge base from JSON.
- Modular data ingestion pipeline (`ingest.py`), decoupled from retrieval.
- Function-calling agent loop (`agent.py` — `GridMindAgent`) that decides when to search and when to answer.
- Tool registry pattern with a `BaseTool` abstraction (`base_tool.py`), so new tools can be added without modifying the agent's dispatch logic.
- `search` tool (`search.py`, `tools.py`) backed by a pluggable retriever.
- In-memory keyword search index using **MinSearch**.
- Persistent keyword search index using **SQLiteSearch**.
- Context building (`context.py`) and prompt/instruction management (`prompts.py`), decoupled from the retriever itself.
- Context-aware answers generated via a Groq-hosted LLM through the OpenAI Python SDK.
- Separation of ingestion from querying, for a production-oriented architecture.
- CLI chat interface (`main.py`) for interactive testing.

---

## Tech Stack

- **Python** – Core development
- **MinSearch** – In-memory keyword retrieval
- **SQLiteSearch** – Persistent keyword retrieval
- **Groq LLM** (`openai/gpt-oss-20b`) via the **OpenAI Python SDK**
- **JSON** – Knowledge base storage
- **python-dotenv** – Environment/configuration management

---

## Project Structure

```text
studygrid-app-copilot/
│
├── data/
│   └── studygrid_faq_bilingual.json
│
├── main.py            # CLI entry point
├── config.py          # Composition root — wires everything together
├── agent.py           # GridMindAgent — the function-calling loop
├── tools.py           # TOOL_SCHEMAS — JSON schemas describing available tools
├── base_tool.py        # BaseTool abstraction for adding new tools
├── search.py           # SearchTool — the search tool implementation
├── retriever.py         # Retriever — keyword search over the knowledge base
├── context.py           # build_context — formats search results for the LLM
├── prompts.py            # INSTRUCTIONS and prompt templates
├── ingest.py              # Loads the FAQ knowledge base
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

---

## Roadmap / Learning Progress

This repository evolves alongside the **LLM Zoomcamp** curriculum.

### Completed

- ✅ Basic RAG pipeline
- ✅ Prompt engineering & input-scope guardrails
- ✅ MinSearch & SQLiteSearch keyword retrieval
- ✅ Modular architecture (ingestion, retrieval, context, prompts separated)
- ✅ Function calling & the agentic loop (`GridMindAgent`)
- ✅ Tool registry pattern for extensibility

### In progress

- 🔜 Vector search (embeddings, MinSearch/SQLiteSearch vector modes)
- 🔜 Retrieval evaluation (comparing keyword vs. vector search quantitatively)
- 🔜 LLM output evaluation
- 🔜 Hybrid search, reranking, and query rewriting

### Planned

- 🔜 Monitoring (user feedback collection + dashboard)
- 🔜 Web/API interface (beyond the current CLI)
- 🔜 Containerization (Docker / docker-compose)
- 🔜 Integration into the main [StudyGrid app](https://github.com/0xezzdev/StudyGrid)
- 🔜 Additional tools (e.g. summarizing group activity, searching uploaded course files)

---

## Evaluation Criteria Mapping

For reviewers familiar with the LLM Zoomcamp project rubric, here's where this project currently stands (updated as the roadmap above progresses):

| Criterion | Status |
|---|---|
| Problem description | Described above |
| Retrieval flow | Knowledge base + LLM, via an agentic function-calling loop |
| Retrieval evaluation | In progress (see Roadmap) |
| LLM evaluation | In progress (see Roadmap) |
| Interface | CLI (`main.py`) — a web/API interface is planned |
| Ingestion pipeline | Automated via `ingest.py` |
| Monitoring | Planned |
| Containerization | Planned |

---

## Author

**Theophilus Sameh**

Computer and Control Systems Engineering student passionate about Artificial Intelligence, Large Language Models, Information Retrieval, and Mobile Application Development.

This repository documents my journey toward becoming an LLM Engineer by applying every concept learned in the LLM Zoomcamp to a real-world project instead of simply reproducing the course notebooks.

- GitHub: https://github.com/theophilussameh
- LinkedIn: https://www.linkedin.com/in/theophilussameh
