# Retrieval-Augmented-Workflow-using-Qdrant


A retrieval-augmented generation (RAG) workflow that transparently answers contract-related questions over the CUAD (Contract Understanding Atticus Dataset). This project leverages:

- **LangGraph** for explainable, multi-step agent workflows  
- **Qdrant** as a high-performance vector database for semantic search  
- **OpenAI (GPT-4)** for generative answering  
- **FastAPI** (with built-in Swagger UI) to expose a REST API and a simple HTML form  

The full tutorial is available as Part 6 of my series on Medium:  
> [Implementing LLM Applications Using LangChain (Part 6): Retrieval-Augmented Agents with LangGraph & FastAPI](https://medium.com/@jagadeshvarma07/implementing-llm-applications-using-langchain-part-6-retrieval-augmented-agents-with-langgraph-2ba7ac31492a)

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Directory Structure](#directory-structure)  
5. [Usage](#usage)  
6. [Testing & Swagger UI](#testing--swagger-ui)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## Project Overview

This repository demonstrates a complete pipeline to build a production-ready RAG agent:

1. **Indexing**: Extracts contract clauses from the CUAD JSON and stores vector embeddings in Qdrant.  
2. **Agent Logic**: Uses LangGraph to define a clear workflow—receive a question, retrieve relevant clauses, generate an answer via GPT-4.  
3. **API Exposure**: Wraps the agent in a FastAPI server, providing both a JSON-based endpoint and a simple HTML form.  

By following this repository, you’ll learn how to go from raw contract data to a fully functional LLM service capable of answering complex legal questions in real time.

---

## Prerequisites

- **Python 3.9+** (tested on 3.10/3.11/3.12)  
- **Docker** (to run Qdrant locally)  
- **OpenAI API Key** (with access to GPT-4 or GPT-3.5)  
- **Git** (to clone this repo)  

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Think-Round-Inc/ThinkxLife-CUAD-RAG.git
   cd ThinkxLife-CUAD-RAG
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # .venv\Scripts\activate    # Windows PowerShell
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn python-dotenv langchain langchain-openai langchain-qdrant langgraph qdrant-client
   ```

4. **Create a `.env` file** at the project root with your OpenAI API key:

   ```env
   OPENAI_API_KEY=sk-<your_openai_key_here>
   ```

   > **Do not commit** your `.env` file or share your key publicly.

---

## Directory Structure

```
├── data/
│   └── cuad.json               # CUAD dataset (Contract Understanding Atticus)
├── build_index.py              # Extracts & indexes CUAD clauses into Qdrant
├── chatbot_core.py             # LangGraph agent logic (retrieval + LLM chain)
├── main.py                     # FastAPI server exposing `/ask` and HTML form
├── .env                        # (not checked in) environment variables (OpenAI key)
└── README.md                   # This file
```

---

## Usage

Follow these steps to get the RAG agent up and running:

### 1. Configure Environment Variables

Ensure a file named `.env` exists at the project root containing:

```
OPENAI_API_KEY=sk-<your_openai_key_here>
```

### 2. Run Qdrant via Docker

Start a local Qdrant instance on port 6333:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Verify that Qdrant is running:

```bash
curl http://localhost:6333/collections
# Response: {"result":{"collections":[]}, ...}
```

### 3. Index CUAD Data

Populate Qdrant with contract clause embeddings:

```bash
python build_index.py
```

This step:

* Loads each clause’s text from `data/cuad.json`
* Embeds them via the OpenAI API
* Stores the resulting vectors in Qdrant under the collection named `cuad_contracts`

### 4. Start the FastAPI Server

Launch the API server:

```bash
python -m uvicorn main:app --reload
```

* The server runs on `http://127.0.0.1:8000` by default
* The `--reload` flag restarts the server on code changes

---

## Testing & Swagger UI

### JSON Endpoint

1. Open **`http://127.0.0.1:8000/docs`** in your browser.
2. Use the **`POST /ask`** endpoint to submit JSON with a `"question"`.
3. Review the generated answer in the Swagger UI response pane.

### HTML Form

1. Open **`http://127.0.0.1:8000/`** in your browser.
2. Enter a question and submit.
3. View the answer on the results page.

---

## Contributing

Contributions are welcome! If you find bugs or have suggestions (e.g., multi-tool orchestration, guardrails integration, deployment scripts), please open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to reuse, modify, and redistribute under the MIT terms.

---
