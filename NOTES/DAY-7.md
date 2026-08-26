# DAY 7 — RAG Evaluation & Grounding

## 1. Goal

The goal of Day 7 is to evaluate the RAG Knowledge Assistant systematically.

The evaluation checks whether the system:

- Retrieves relevant information
- Produces answers supported by documents
- Refuses unsupported questions
- Handles tricky or near-miss questions correctly
- Avoids unsupported claims

---

## 2. RAG Evaluation Pipeline

The evaluation process is:

Question
↓
Embedding
↓
Similarity Search
↓
Top-K Retrieved Chunks
↓
Context
↓
LLM
↓
Answer
↓
Evaluation

The important difference from normal testing is that we inspect not only the final answer, but also the retrieved evidence.

---

## 3. 25-Question Evaluation

The evaluation contains 25 questions divided into three categories.

### Section A — Answerable Questions

Q1–Q15 test whether the system can answer questions supported by the knowledge base.

Examples include:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Generative AI
- LLMs
- Embeddings
- Vector stores
- RAG
- RAG pipeline
- Chunking
- Embedding models
- Retrievers
- AI agents
- APIs

### Section B — Unanswerable Questions

Q16–Q20 test whether the system refuses information that is not available.

Examples include:

- Future political predictions
- Future Bitcoin price
- Private phone information
- Future company revenue
- Future AI market share

Expected behavior:

"I could not find this information in the provided documents."

### Section C — Tricky / Near-Miss Questions

Q21–Q25 test whether the system can distinguish between:

- Directly supported information
- Related but insufficient information
- Completely unsupported information

---

## 4. Grounding

Grounding means generating an answer based on retrieved evidence or context.

The system should not treat a related topic as proof of an answer.

The grounding rule is:

If the answer exists in the provided documents:
→ Answer using the retrieved evidence.

If the answer cannot be found:
→ Refuse instead of inventing information.

---

## 5. Prompt V1

The original RAG prompt instructed the LLM to:

- Use only the provided context
- Avoid outside knowledge
- Avoid guessing
- Refuse unsupported information

This produced the initial baseline.

---

## 6. Baseline Result

The first evaluation produced:

**20 / 25 = 80%**

This established the V1 baseline.

The baseline is important because later improvements must be compared against it.

---

## 7. Prompt V2

Prompt V2 introduced stronger grounding instructions.

It added rules for:

- Directly supported answers
- Related but insufficient information
- Unsupported questions
- Preventing invented facts
- Avoiding assumptions
- Mentioning source files or sections when possible

---

## 8. V1 vs V2

The tested V2 cases did not show an observable improvement over V1.

Important cases included:

- Q7
- Q13
- Q14
- Q15
- Q21
- Q25

This demonstrated an important engineering lesson:

Changing the prompt alone does not necessarily solve a RAG retrieval problem.

---

## 9. Failure Analysis

### Q7 — Vector Database

The question asks about a vector database.

The retrieved knowledge discusses a vector store but does not explicitly provide the requested definition.

Classification:

**Source / terminology coverage issue**

The assistant correctly avoided inventing an unsupported definition.

---

### Q13 — AI Agent

The current knowledge base does not contain sufficient information to define an AI agent.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused to use outside knowledge.

---

### Q14 — AI Agent Tools / APIs

The current knowledge base does not contain sufficient information about an AI agent using tools or APIs.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused to invent an answer.

---

### Q15 — API

The current knowledge base does not contain sufficient information about APIs for the requested answer.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused unsupported information.

---

### Q21 — RAG and Hallucination

Question:

"Does using RAG guarantee that an LLM will never hallucinate?"

The retrieval diagnostic showed that the top five chunks were general RAG information.

The retrieved chunks included topics such as:

- RAG architecture
- RAG pipeline
- Grounded generation
- Why RAG is needed
- What RAG is
- Relevant context retrieval

However, they did not explicitly provide evidence about whether RAG guarantees that hallucinations never occur.

Classification:

**Retrieval / source coverage issue**

This demonstrates that semantically related retrieval does not always provide sufficient evidence for the exact question.

---

## 10. Faithfulness

Faithfulness means that the generated answer should remain supported by the retrieved context.

A useful principle is:

Relevant topic ≠ sufficient evidence.

A retrieved chunk may be related to a question while still not containing enough information to answer it.

Therefore, RAG evaluation must inspect the retrieved evidence rather than judging only the final answer.

---

## 11. Important Engineering Lesson

A RAG system is not only an LLM.

Its performance depends on multiple stages:

Documents
→ Chunking
→ Embeddings
→ Retrieval
→ Context
→ LLM
→ Grounded Generation

A problem in retrieval or knowledge coverage can cause an answer failure even when the LLM prompt is well designed.

---

## 12. Day 7 Artifacts

Files created or updated:

- `test-questions.md`
- `test-answers.md`
- `eval_template.md`
- `baseline_results_v1.md`
- `baseline_results.md`
- `rag_v1.py`
- `diagnose_q21.py`

---

## 13. Current Status

- [x] 25-question evaluation
- [x] V1 baseline
- [x] 20/25 baseline result
- [x] Failure analysis
- [x] Prompt V2
- [x] V1/V2 comparison
- [x] Q21 retrieval diagnostic
- [x] Evaluation record
- [ ] Final practice
- [ ] Final PDF
- [ ] GitHub update

---

## 14. Key Takeaway

The most important lesson from Day 7 is:

**A RAG system must be evaluated at both the retrieval and generation levels.**

A good answer is not enough.

We need to know:

1. What was retrieved?
2. Was the retrieved information relevant?
3. Did it actually support the answer?
4. Did the LLM remain grounded?
5. Did the system refuse when evidence was missing?