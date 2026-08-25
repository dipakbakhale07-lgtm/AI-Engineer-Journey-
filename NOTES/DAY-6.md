# DAY 6 — RAG V1: END-TO-END PIPELINE

## Objective

Build the first working version of a Retrieval-Augmented Generation (RAG)
system using a local Markdown knowledge base, embeddings, similarity search,
retrieval, context construction, and a local LLM.

---

# 1. Document Loading

A document loader reads the source document and converts it into text that
the application can process.

For this project:

Document:
`documents/rag-fundamentals.md`

The document contained approximately 8,103 characters.

Pipeline:

Document
↓
Document Loader
↓
Text

---

# 2. Chunking

Chunking is the process of dividing a document into smaller meaningful pieces.

For our Markdown documents, we selected section-based chunking.

A level-2 Markdown heading (`##`) represents a section boundary.

Example:

## What is RAG?
content...

## Why is RAG Needed?
content...

These become separate chunks.

The top-level document title (`# RAG Fundamentals`) is not treated as a
retrieval chunk.

Our RAG Fundamentals document produced:

21 retrieval chunks.

---

# 3. Embedding

An embedding is a numerical vector representation of information.

An embedding model converts text into a vector.

Text
↓
Embedding Model
↓
Numerical Vector

Embedding model used:

`all-MiniLM-L6-v2`

Each chunk produced a vector with:

384 dimensions.

For 21 chunks:

21 × 384

Embedding shape:

`(21, 384)`

---

# 4. Query Embedding

The user's question is also converted into an embedding.

Example:

Question:
"What is RAG?"

↓
Embedding Model
↓
Query Vector

The query vector can then be compared with the stored document vectors.

---

# 5. Similarity Search

Similarity search compares the query embedding with the embeddings of
the document chunks.

We used cosine similarity.

Cosine similarity measures the similarity between vectors based on the
angle between them.

Conceptually:

Query Vector
↓
Compare with Document Vectors
↓
Similarity Scores
↓
Rank Results

---

# 6. Top-K Retrieval

After calculating similarity scores, the chunks are ranked.

Top-K means selecting the K highest-ranked results.

Our first implementation used:

`TOP_K = 3`

Therefore, the three most similar chunks were retrieved for the question.

Example:

Question:
"What is RAG?"

Top result:

`## What is RAG?`

This showed that the retrieval system was working logically.

---

# 7. Context

Context is the relevant information retrieved from the knowledge base
and provided to the LLM.

Our system combined the top retrieved chunks into one context.

Conceptually:

Question
↓
Retrieval
↓
Relevant Chunks
↓
Context

The entire document was not sent to the LLM.

Only the retrieved context was passed forward.

---

# 8. Prompt

A prompt is the complete instruction and information given to the LLM.

Our RAG prompt contained:

- Grounding instruction
- Retrieved context
- User question

The LLM was instructed to use only the provided context.

---

# 9. Grounding

Grounding means generating an answer based on retrieved evidence or context.

Our grounding rule:

If the answer exists in the provided documents:
→ Answer using the retrieved evidence.

If the answer cannot be found:
→ Say that the information could not be found in the provided documents.

---

# 10. Hallucination

A hallucination occurs when an LLM generates information that is not
supported by the available evidence.

Our RAG system attempts to reduce unsupported generation by providing
retrieved context and a grounding instruction.

---

# 11. Local LLM

We used Ollama for local LLM generation.

LLM:

`llama3:latest`

Ollama endpoint:

`http://localhost:11434/api/generate`

The LLM receives:

Context + Question + Instructions

and produces the final answer.

---

# 12. Complete RAG Pipeline

Documents
↓
Document Loading
↓
Chunking
↓
Embeddings
↓
Similarity Search
↓
Top-K Retrieval
↓
Context Construction
↓
Prompt
↓
LLM
↓
Grounded Answer

---

# 13. Day 6 Validation

## Known Question

Question:

"What is RAG?"

The system retrieved the correct section:

`## What is RAG?`

The LLM generated:

"RAG stands for Retrieval-Augmented Generation."

Result:

PASS

---

## Unknown Question

Question:

"What is the capital of France?"

The information was not present in the RAG knowledge base.

The system produced:

"I could not find this information in the provided documents."

Result:

PASS

---

# 14. Important Engineering Lessons

1. An LLM alone does not guarantee application-specific knowledge.
2. Retrieval supplies relevant knowledge to the LLM.
3. Good chunking affects retrieval quality.
4. Embeddings represent semantic information numerically.
5. Similarity search finds relevant chunks.
6. Context connects retrieval with generation.
7. Grounding helps prevent unsupported answers.
8. A RAG system is a complete pipeline, not simply an LLM connected to a file.
9. Each component should be tested independently before integration.
10. Retrieval should be inspected before trusting the generated answer.

---

# 15. Day 6 Final Architecture

User Question
↓
Query Embedding
↓
Similarity Search
↓
Top-K Chunks
↓
Retrieved Context
↓
Grounded Prompt
↓
Llama 3
↓
Answer

Knowledge Preparation:

Document
↓
Chunking
↓
Embedding
↓
Stored Vectors