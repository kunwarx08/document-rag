# Document RAG

Local Retrieval-Augmented Generation system. Runs on laptop, learns core AI engineering concepts. Built in phases — each phase is independently usable.

> **First time?** Read [`README.md`](./README.md) — it has the full setup guide, architecture walkthrough, and detailed roadmap. This file covers agent-specific conventions only.

## Current Phase

Phase 1 complete. Next: Phase 2.

| Phase | What | Status |
|---|---|---|
| 1 — LLM Integration | CLI + LLM client + chat | Done |
| 2 — Document Ingestion | Text extraction, chunking | Next |
| 3 — Embeddings & Vector Store | Embeddings, ChromaDB | Not started |
| 4 — Retrieval Pipeline | Dense retrieval, top-k | Not started |
| 5 — RAG Generation | Context injection, RAG loop | Not started |
| 6 — Evaluation & Iteration | Metrics, failure analysis | Not started |

## Commands

```
# Install
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Run
python -m src.cli ask "question"
python -m src.cli chat

# Test (MANDATORY before marking any work complete)
python -m pytest tests/ -v
```

## Project Structure

```
document-rag/
  src/
    config.py      # Settings from .env (LLM_BASE_URL, LLM_API_KEY, LLM_MODEL)
    generator.py   # Stateless LLM client (OpenAI-compatible — Ollama, NVIDIA, etc.)
    chat.py        # In-memory ChatSession with history
    cli.py         # Click CLI: `ask` (single) and `chat` (interactive)
  tests/
    test_generator.py
    test_chat.py
  data/documents/  # Place test documents here (Phase 2+)
  .env             # API keys — NEVER commit
```

## Design Principles

1. **Generator stays stateless** — it sends messages, doesn't track them. State lives in higher-level wrappers like ChatSession.
2. **Provider is a config detail** — not a code branch. Switch providers by changing .env, not if/else.
3. **Each phase produces a working CLI command** — no half-built features. Phase N must be usable before Phase N+1 starts.
4. **API keys in .env only** — never hardcode, never commit.
5. **Phase isolation** — don't modify completed phases unless fixing a bug. Add new files for new phases.

## Conventions

- Python 3.11+ with type hints everywhere
- No docstrings on self-documenting code
- Tests in tests/ mirroring src/ structure, mocking external APIs
- Minimal dependencies — prefer stdlib over new packages

## Provider Setup

Default: Ollama (no API key, runs locally).
To switch: edit .env — LLM_BASE_URL, LLM_API_KEY, LLM_MODEL.

## Git Conventions

Commit messages should describe WHAT changed and WHY, structured so any agent joining fresh can `git log` and understand progress.

All prior work in this repo was done by AI agents. Future agents may be from different sessions — always read AGENTS.md first, then check `git log` for context on what was done and why.

## Error Handling Patterns

- null content from LLM: return "" (not None)
- API errors: let openai SDK exceptions propagate (no wrapping)
