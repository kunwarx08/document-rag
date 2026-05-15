# Document RAG — Personal Local RAG System

> Build a local Retrieval-Augmented Generation system from scratch. Runs on your laptop, learns core AI engineering concepts.

## Project Status

**Current Phase:** 1 ✅ — CLI with LLM integration (Ollama/NVIDIA) + interactive chat

| Phase | Status | What You'll Learn |
|---|---|---|
| 1 — LLM Integration | ✅ Done | API clients, prompt engineering, chat history, provider abstraction |
| 2 — Document Ingestion | 🔜 Next | Text extraction, chunking strategies (size, overlap, semantics) |
| 3 — Embeddings & Vector Store | ⏳ | Embedding models, vector databases, similarity search |
| 4 — Retrieval Pipeline | ⏳ | Dense retrieval, hybrid search, retrieval evaluation |
| 5 — RAG Generation | ⏳ | Context injection, prompt design, faithfulness |
| 6 — Evaluation & Iteration | ⏳ | Metrics (hit rate, MRR), failure analysis, systematic improvement |

---

## Quick Start

```bash
# Prerequisites: Python 3.10+, Ollama (for local inference)

# 1. Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
# Create .env with your provider settings (see Configuration section below)
# For Ollama (default): no .env needed at all — just run

# 3. Run
python -m src.cli ask "What is a vector embedding?"
```

---

## Architecture

### Current Code Structure

```
document-rag/
├── .env                  # Secrets (API keys) — NOT committed
├── requirements.txt      # Python dependencies
├── data/documents/       # Place test documents here (Phase 2+)
├── src/
│   ├── config.py         # Settings from .env (provider, model, params)
│   ├── generator.py      # LLM client — talks to Ollama or NVIDIA API
│   ├── chat.py           # In-memory conversation history
│   └── cli.py            # CLI entry point with `ask` and `chat` commands
└── tests/
    ├── test_generator.py # Generator unit tests (mocked API)
    └── test_chat.py      # ChatSession unit tests
```

### Data Flow

```
.env  ──reads──▶  config.py  ──passes to──▶  generator.py  ──sends to──▶  Ollama / NVIDIA API
                                   ▲                ▲
                                   │                │
                              cli.py (ask)     chat.py (chat)
                                   │                │
                                   └── both use ────┘
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| **OpenAI-compatible client** | Ollama and NVIDIA both speak this protocol — one `Generator` class works for both |
| **`Generator` is stateless** | It doesn't remember conversations. State lives in `ChatSession` |
| **`ChatSession` lives in memory** | History is a Python list — lost on exit. Persistent storage is a future addition |
| **Provider via env vars** | Change `.env` to switch between local (Ollama) and cloud (NVIDIA). No code changes needed |

---

## Configuration

The system reads from environment variables (via `.env`). Defaults point to Ollama locally:

| Variable | Default | Purpose |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | API endpoint (Ollama or cloud provider) |
| `LLM_API_KEY` | *(empty)* | API key for cloud providers (NVIDIA, OpenAI, etc.) |
| `LLM_MODEL` | `llama3.2` | Model name to use |

### Switching Providers

**Ollama (local, no key needed):**
```env
# .env — leave defaults, or explicitly:
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
```

**NVIDIA API (cloud):**
```env
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_API_KEY=nvapi-your-key-here
LLM_MODEL=meta/llama-3.1-70b-instruct
```

---

## CLI Commands

### `ask` — Single question, no memory

```bash
python -m src.cli ask "What is RAG?"
python -m src.cli ask "Explain embeddings" --system "You are a math tutor"
python -m src.cli ask "Hi" --model llama3.2 --temperature 0.3
```

### `chat` — Interactive conversation with history

```bash
python -m src.cli chat
python -m src.cli chat --system "You are a Python tutor"
python -m src.cli chat --model llama3.2
```

In-chat commands:

| Command | Action |
|---|---|
| `/exit` | Quit the chat |
| `/clear` | Reset conversation history (keeps system prompt) |

---

## Running Tests

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

Tests use mocked API calls — no live LLM needed. They validate:
- Settings defaults and env var loading
- Message formatting (system, user, assistant roles)
- Conversation history accumulation
- Edge cases (null response content, clear with system prompt)

---

## Roadmap — Phase by Phase

### Phase 1: LLM Integration ✅
Build a CLI that talks to an LLM via API.

- **Files:** `config.py`, `generator.py`, `chat.py`, `cli.py`
- **Concepts:** OpenAI-compatible API, provider abstraction, prompt structure, chat history
- **Deliverable:** `python -m src.cli ask "..."` and `python -m src.cli chat`

### Phase 2: Document Ingestion & Chunking 🔜
Load text and break it into manageable pieces for retrieval.

- **Files:** `src/loader.py`, `src/chunker.py`, `data/documents/`
- **Concepts:** Text extraction, chunk size, overlap strategies, document structure awareness
- **Deliverable:** `python -m src.cli ingest myfile.txt`

### Phase 3: Embeddings & Vector Store
Convert chunks into vectors and store them for similarity search.

- **Files:** `src/embeddings.py`, `src/vector_store.py`
- **Concepts:** Embedding models, vector databases (ChromaDB), cosine similarity
- **Deliverable:** `python -m src.cli ingest` actually stores vectors

### Phase 4: Retrieval Pipeline
Given a query, find the most relevant document chunks.

- **Files:** `src/retriever.py`
- **Concepts:** Dense retrieval, top-k, relevance scoring
- **Deliverable:** `python -m src.cli retrieve "question"` returns relevant chunks

### Phase 5: RAG Generation
Wire retrieval into generation — the actual RAG loop.

- **Files:** Updates to `generator.py` and `cli.py`
- **Concepts:** Context injection, prompt templates, grounding
- **Deliverable:** `rag` command that retrieves + generates in one step

### Phase 6: Evaluation & Iteration
Measure quality, find failure modes, improve systematically.

- **Files:** `src/evaluator.py`
- **Concepts:** Hit rate, MRR, faithfulness, systematic iteration
- **Deliverable:** `python -m src.cli eval` with a report card

---

## Agent Guidelines

For AI agents (OpenCode, assistants) working on this project:

### Conventions

- **Python 3.11+** with type hints everywhere
- **Minimal dependencies** — prefer standard library over new packages
- **`src/` package** — all application code lives here
- **Tests in `tests/`** — mirror `src/` structure, mock external APIs
- **No docstrings on obvious code** — code should be self-documenting
- **Phased delivery** — each phase is independently usable; don't skip ahead

### Design Principles

1. **`Generator` stays stateless** — it sends messages, doesn't track them
2. **State lives in higher-level wrappers** — like `ChatSession`
3. **Provider is a config detail** — not a code branch. Env vars, not if/else
4. **Each phase produces a working CLI command** — no half-built features
5. **API keys in `.env` only** — never hardcode, never commit

### Working with This Project

- READ THIS FILE first to understand current state and direction
- Each phase builds on the previous — don't modify completed phases unless fixing a bug
- When adding a new phase: create new files, don't bloat existing ones
- Run `pytest tests/ -v` before marking any work as complete

---

## Tech Stack

| Component | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Industry standard for ML/AI |
| LLM Client | `openai` SDK | Works with Ollama, NVIDIA, OpenAI, Together, etc. |
| LLM (local) | Ollama + Llama 3.2 | Runs on M1 MacBook Air |
| LLM (cloud) | NVIDIA API Catalog | Free credits, powerful models |
| CLI Framework | Click | Simple, well-documented, no boilerplate |
| Vector Store | ChromaDB (Phase 3) | Embedded, zero-config, runs locally |
| Embeddings | sentence-transformers (Phase 3) | Runs on CPU, well-supported |
| Testing | pytest + unittest.mock | Standard Python testing stack |
