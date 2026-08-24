# Metadata Design

## Purpose

Metadata provides information about each document chunk.

It helps the RAG system identify where retrieved information came from and can support source display and filtering.

## Metadata Fields

| Field | Purpose |
|---|---|
| filename | Identifies the source document |
| topic | Identifies the main subject |
| section | Identifies the document section |
| chunk_id | Gives each chunk a unique identifier |

## Example

Chunk text:

RAG stands for Retrieval-Augmented Generation.

Metadata:

filename = rag-fundamentals.md
topic = RAG
section = What is RAG?
chunk_id = rag-001

## Planned Metadata Structure

```text
{
    "filename": "...",
    "topic": "...",
    "section": "...",
    "chunk_id": "..."
}