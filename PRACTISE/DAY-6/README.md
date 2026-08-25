# DAY 6 PRACTICE — RAG V1

## Objective

Practice the complete RAG pipeline and understand each component.

---

## Task 1 — Explain the Pipeline

Explain this pipeline in your own words:

Document
↓
Chunking
↓
Embedding
↓
Similarity Search
↓
Retrieval
↓
Context
↓
LLM
↓
Answer

---

## Task 2 — Definitions

Write a one- or two-line definition for:

1. Document Loader
2. Chunk
3. Chunking
4. Embedding
5. Embedding Model
6. Vector
7. Similarity Search
8. Cosine Similarity
9. Top-K Retrieval
10. Context
11. Prompt
12. Grounding
13. Hallucination
14. Retrieval
15. RAG

---

## Task 3 — Numerical Understanding

Our project produced:

21 chunks

and each embedding contained:

384 dimensions.

Answer:

1. What does 21 represent?
2. What does 384 represent?
3. What does `(21, 384)` mean?

---

## Task 4 — Retrieval Analysis

Question:

"What is RAG?"

The top retrieved chunk was:

`## What is RAG?`

Similarity:

`0.7831`

Answer:

1. Why was this a good retrieval result?
2. What does the similarity score represent?
3. Why do we retrieve multiple chunks instead of automatically using
   only one?

---

## Task 5 — Grounding Test

Question:

"What is the capital of France?"

The information does not exist in our RAG knowledge base.

Expected behavior:

"I could not find this information in the provided documents."

Explain why this behavior is important.

---

## Task 6 — Architecture

Draw the complete RAG architecture on paper:

User Question
↓
Query Embedding
↓
Similarity Search
↓
Top-K Retrieval
↓
Context
↓
Prompt
↓
LLM
↓
Grounded Answer

Also draw the knowledge preparation side:

Documents
↓
Chunking
↓
Embeddings
↓
Stored Vectors

---

## Task 7 — Code Understanding

In `rag_v1.py`, identify:

1. Which function loads the document?
2. Which function creates chunks?
3. Which model creates embeddings?
4. Which function calculates cosine similarity?
5. Where is Top-K selected?
6. Which function creates the context?
7. Which function calls Ollama?
8. Where is the grounding instruction written?

---

## Task 8 — Mini Experiment

Change:

`TOP_K = 3`

to:

`TOP_K = 1`

Run the program with:

"What is RAG?"

Observe the retrieved result.

Then change it to:

`TOP_K = 5`

Run it again.

Write down what changes.

---

## Day 6 Practice Result

Completed:

[ ] Pipeline explanation

[ ] Definitions

[ ] Numerical understanding

[ ] Retrieval analysis

[ ] Grounding test

[ ] Architecture diagram

[ ] Code understanding

[ ] TOP-K experiment