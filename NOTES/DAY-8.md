# DAY 8 — Improve the RAG User Experience

## Goal

Make the RAG project understandable and usable by another person.

## What I Learned

Day 8 focused on improving the user experience of the RAG Assistant.

The RAG system should not only work technically; another person
should be able to understand and use it without detailed instructions.

## Interface

Created a basic Streamlit interface for the RAG Assistant.

The interface includes:

- Project title
- Short instruction for the user
- Question input box
- Ask button
- Clean answer display
- Source information below the answer

## Error Handling

Added friendly handling for:

- Empty questions
- Ollama/API connection failure
- API request failure
- Timeout
- General processing errors

The application displays a friendly message instead of exposing
a Python traceback to the user.

## RAG Flow

The user experience follows this flow:

```text
User Question
     ↓
Question Embedding
     ↓
Similarity Search
     ↓
Relevant Chunks
     ↓
LLM
     ↓
Grounded Answer
     ↓
Source