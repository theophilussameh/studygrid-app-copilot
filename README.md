

# GridMind.

AI Copilot for the StudyGrid app, built with Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

GridMind is an AI-powered copilot designed for the StudyGrid application. It retrieves relevant information from a knowledge base and uses a Large Language Model (LLM) to generate accurate, context-aware answers.

This project is being developed step by step while studying the LLM Zoomcamp by DataTalksClub. Rather than simply reproducing the course notebooks, each concept is applied to a real-world project that evolves throughout the learning journey.

---

## Current Features

- Load a StudyGrid FAQ knowledge base from JSON.
- Build a search index using `minsearch`.
- Retrieve the most relevant documents.
- Build contextual prompts for the LLM.
- Generate answers using an LLM.
- Implement a basic Retrieval-Augmented Generation (RAG) pipeline.
- Demonstrate a basic Prompt Injection example.

---

## Tech Stack

- **Python** – Core development
- **MinSearch** – Keyword-based information retrieval
- **Groq LLM** – Answer generation
- **OpenAI Python SDK** – Client for interacting with the Groq API
- **JSON** – Knowledge base storage
- **Python Dotenv** – Environment variable management
- **Jupyter Notebook** – Development and experimentation
---

## Project Structure

```text
studygrid-app-copilot/
│
├── data/
│   └── studygrid_faq_bilingual.json
│
├── notebook.ipynb
├── main.py
├── README.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

---

---

## Author

**Theophilus Sameh**

Electrical and Computer Engineering student with a strong interest in Artificial Intelligence, Large Language Models (LLMs),  and Mobile Application Development.
 
This project documents my journey of applying the concepts learned in the LLM Zoomcamp to build production-oriented AI applications while continuously improving my software engineering skills.

- GitHub: https://github.com/theophilussameh
- LinkedIn: www.linkedin.com/in/theophilussameh