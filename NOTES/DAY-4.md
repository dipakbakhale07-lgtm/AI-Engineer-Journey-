# DAY 4 — Project 1: Define the RAG Assistant

## Goal

Decide exactly what the document assistant should and should not do.

## Project

Project 1 — RAG Assistant

## Problem Statement

Build a document-based question-answering assistant that answers
questions using only information contained in the supplied documents.

The assistant must distinguish between:

- What the LLM may already know
- What information is actually present in the supplied documents

If the supplied documents do not contain the answer, the assistant
must not use outside knowledge.

## User

The user asks questions about the information contained in the
provided documents.

## Scope

The RAG Assistant should:

- Accept questions from the user.
- Search the supplied documents.
- Retrieve relevant information.
- Use the retrieved information to generate an answer.
- Clearly state when the answer cannot be found in the documents.

The assistant should NOT:

- Invent information.
- Use outside knowledge when the supplied documents do not contain
  the answer.
- Pretend that information is present when it is not.

## Data Source

Safe public/sample documents.

Suggested sources:

- Course FAQ
- Sample policy
- Simple AI notes

## Correct-Answer Boundary

The assistant must answer only when the information is supported
by the supplied documents.

If the answer is not present in the documents, the assistant must say:

> "I could not find this in the provided documents."

This is the correct-answer boundary for the RAG Assistant.

## Questions

15 realistic questions were prepared for testing.

5 questions are intentionally marked as questions that the
documents cannot answer.

The test questions are stored in:

`test-questions.md`

Expected answers are stored in:

`test-answers.md`

## Architecture

The RAG Assistant architecture is:

```text
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
Vector Store
    ↓
Retrieval
    ↓
LLM
    ↓
Answers