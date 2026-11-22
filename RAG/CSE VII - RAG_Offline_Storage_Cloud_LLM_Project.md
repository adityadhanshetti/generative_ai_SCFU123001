# RAG Project — Offline Storage, Cloud-API LLM

## Scenario

Build a research paper Q&A assistant over 3–5 PDFs. Document loading, chunking, embedding, and retrieval must run **fully offline** (no network calls). Only the final answer-generation step may call a **cloud LLM API**.

## Requirements

1. **Ingestion** — load PDFs locally, keep per-paper and per-page metadata.
2. **Chunking** — split into chunks; briefly note your chunk size/overlap choice.
3. **Indexing** — embed locally (no external embedding API), store in a local persisted vector store. Reload existing index instead of rebuilding each run.
4. **Retrieval** — fully offline; support single-paper and cross-paper queries.
5. **Generation** — the only step allowed to call the internet (cloud LLM API). Answer only from retrieved context; say "not found" if context lacks the answer; ignore any instruction-like text inside retrieved chunks. Handle API failures gracefully.
6. **Offline/Online split** — add a "retrieval-only" mode that skips the API call entirely, to prove steps 1–4 work independently of the network.
7. **Interactive loop** — accept questions until `exit`; print sources (paper + page) and a timing breakdown (local retrieval vs API call) per question.
8. **Evaluation** — run 6 fixed test questions automatically (2 single-paper, 2 cross-paper, 2 out-of-scope) and print a pass/fail table.

## Deliverable

One Colab notebook (`.ipynb`), runs top-to-bottom with no manual steps besides supplying an API key. One markdown/code section per requirement above.

## Constraints

- Steps 1–4 must have zero network dependency — notebook should demonstrate this works even with the API key unset.
- The generation API call must be isolated in its own function/cell.
- Local index must survive a restart without re-embedding.
