# 🚀 Project Progress

> A simple log of features implemented phase by phase.

---

## ✅ Phase 1 — LLM Integration

**Status:** Complete

**What was built:**
- CLI tool that talks to an LLM (Ollama locally or NVIDIA cloud)
- `ask` command — ask a single question, get an answer
- `chat` command — have a full conversation with memory
- Spinner animation while waiting for responses
- `--provider` flag to switch between Ollama and NVIDIA without editing files
- Provider system that's easy to extend for new services

**Files created:** `config.py`, `generator.py`, `chat.py`, `cli.py`, `README.md`, `AGENTS.md`, `PROGRESS.md`

---

## 🔜 Phase 2 — Document Ingestion & Chunking

**Status:** Not started

**Goal:** Load text files and split them into meaningful chunks for retrieval.

---

## ⏳ Phase 3 — Embeddings & Vector Store

**Status:** Not started

**Goal:** Convert chunks into vectors and store them for similarity search.

---

## ⏳ Phase 4 — Retrieval Pipeline

**Status:** Not started

**Goal:** Given a query, find the most relevant document chunks.

---

## ⏳ Phase 5 — RAG Generation

**Status:** Not started

**Goal:** Wire retrieval into generation — the actual RAG loop.

---

## ⏳ Phase 6 — Evaluation & Iteration

**Status:** Not started

**Goal:** Measure quality, find failure modes, improve systematically.
