# GridMind

AI Copilot for the StudyGrid app, built with Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

GridMind is an AI-powered copilot designed for the StudyGrid application. It retrieves relevant information from a knowledge base and uses a Large Language Model (LLM) to generate accurate, context-aware answers.

This project is being developed step by step while studying the **LLM Zoomcamp** by **DataTalksClub**. Rather than simply reproducing the course notebooks, every concept is integrated into a real-world AI application while following software engineering best practices such as modular design, separation of responsibilities, dependency injection, and reusable components.

---

## Current Features

- Load a bilingual (English & Arabic) StudyGrid FAQ knowledge base from JSON.
- Modular data ingestion pipeline.
- Reusable RAG helper architecture.
- Build an in-memory keyword search index using **MinSearch**.
- Build a persistent keyword search index using **SQLiteSearch**.
- Retrieve relevant documents from the knowledge base.
- Build contextual prompts for a Large Language Model.
- Generate context-aware answers using a Groq-hosted LLM.
- Implement a Retrieval-Augmented Generation (RAG) pipeline.
- Demonstrate Prompt Injection concepts.
- Separate ingestion from querying for a production-oriented architecture.
- Keep a legacy notebook for comparison and experimentation while migrating to a modular codebase.

---

## Tech Stack

- **Python** – Core development
- **MinSearch** – In-memory keyword retrieval
- **SQLiteSearch** – Persistent keyword retrieval
- **Groq LLM**
- **OpenAI Python SDK**
- **JSON**
- **Python Dotenv**
- **Jupyter Notebook**

---

## Project Structure

```text
studygrid-app-copilot/
│
├── data/
│   ├── studygrid_faq_bilingual.json
│   └── faq.db
│
├── legacy_rag_notebook.ipynb
├── sqlite_ingest.ipynb
├── persistent_rag_ingest.ipynb
├── ingest.py
├── rag_helper.py
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

---

## Architecture

The application follows a modular Retrieval-Augmented Generation (RAG) architecture.

```text
               StudyGrid FAQ (JSON)
                        │
                        ▼
                Data Ingestion
                        │
                        ▼
      Persistent SQLite Search Index
                        │
                        ▼
              Document Retrieval
                        │
                        ▼
               Context Builder
                        │
                        ▼
             Prompt Construction
                        │
                        ▼
                  Groq-hosted LLM
                        │
                        ▼
               Context-Aware Answer
```

By separating data ingestion from querying, the system becomes easier to maintain, reusable across applications, and closer to the architecture used in production RAG systems.

---

## Current Learning Progress

This repository evolves alongside the **LLM Zoomcamp**.

### Completed

- ✅ Basic RAG Pipeline
- ✅ Prompt Engineering
- ✅ MinSearch Retrieval
- ✅ Modular RAG Architecture
- ✅ SQLite-based Persistent Retrieval

### Planned

- 🔜 Embeddings
- 🔜 Vector Search
- 🔜 Hybrid Search
- 🔜 Evaluation
- 🔜 Production RAG
- 🔜 Agentic AI

---

## Author

**Theophilus Sameh**

Computer and Control Systems Engineering student passionate about Artificial Intelligence, Large Language Models, Information Retrieval, and Mobile Application Development.

This repository documents my journey toward becoming an LLM Engineer by applying every concept learned in the LLM Zoomcamp to a real-world project instead of simply reproducing the course notebooks.

- GitHub: https://github.com/theophilussameh
- LinkedIn: https://www.linkedin.com/in/theophilussameh