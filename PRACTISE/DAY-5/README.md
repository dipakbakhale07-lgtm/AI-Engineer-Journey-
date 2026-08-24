# Day 5 Practice — RAG Document Preparation

## Practice Goal

Practice the document-preparation and chunking concepts used in the RAG Knowledge Assistant.

## Practice 1 — Document Structure

Source documents used:

- ai-fundamentals.md
- llm-generative-ai.md
- rag-fundamentals.md

The documents were inspected for meaningful Markdown headings and sections.

## Practice 2 — Chunk Quality

For selected chunks, inspect:

- Whether the chunk contains a complete idea
- Whether sentences are cut at awkward boundaries
- Whether the chunk contains unnecessary information
- Whether the chunk would be useful as retrieval context

## Practice 3 — Chunking Comparison

Two approaches were compared:

### Section-Based Chunking

Uses Markdown `##` headings as natural boundaries.

Observation:
The chunks generally preserve complete concepts and have cleaner semantic boundaries.

### Fixed-Size Chunking

Experiment:
- Chunk size: 500 characters
- Overlap: 50 characters

Observation:
Several chunks were cut in the middle of sentences or concepts.

## Practice 4 — Metadata

Planned metadata fields:

- filename
- topic
- section
- chunk_id

Example:

```text
filename = rag-fundamentals.md
topic = RAG Fundamentals
section = What is RAG?
chunk_id = rag-001