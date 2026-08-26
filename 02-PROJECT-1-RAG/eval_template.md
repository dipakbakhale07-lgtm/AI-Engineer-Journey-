# RAG Evaluation — Day 7

## Purpose

Evaluate whether the RAG Knowledge Assistant:

- Retrieves relevant information
- Produces grounded answers
- Refuses unsupported questions
- Handles tricky or near-miss questions correctly
- Avoids unsupported claims

---

## Baseline

Prompt V1:

- Answer only from provided context
- Do not use outside knowledge
- Do not guess
- Refuse when information is unavailable

Baseline result:

**20/25 = 80%**

---

## Evaluation Summary

| Category | Questions | Result |
|---|---|---|
| Answerable and correctly answered | Q1-Q6, Q8-Q12 | Pass |
| Source/knowledge-base coverage issue | Q7, Q13-Q15 | Needs improvement |
| Correct unsupported-question refusal | Q16-Q20 | Pass |
| Retrieval/source coverage issue | Q21 | Needs improvement |
| Correct tricky/near-miss behavior | Q22-Q25 | Pass |

---

## Failure Analysis

### Q7 — Vector Database

The question asks about a vector database.

The retrieved knowledge uses the terminology "vector store" rather than explicitly defining "vector database".

Classification:

**Source/terminology coverage issue**

The assistant correctly avoided inventing an unsupported definition.

---

### Q13 — AI Agent

The current approved document set does not provide a sufficient definition of an AI agent.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused to use outside knowledge.

---

### Q14 — AI Agent Tools/APIs

The current approved document set does not provide sufficient information about an AI agent using tools or APIs.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused to invent an answer.

---

### Q15 — API

The current approved document set does not provide sufficient API information for the requested answer.

Classification:

**Knowledge-base coverage issue**

The assistant correctly refused unsupported information.

---

### Q21 — RAG and Hallucination

The question asks whether RAG guarantees that an LLM will never hallucinate.

The retrieval diagnostic showed that the top five retrieved chunks were general RAG material:

- RAG architecture
- RAG pipeline and grounded generation
- Why RAG is needed
- What is RAG?
- Why relevant context is retrieved

The retrieved chunks did not explicitly contain evidence about whether RAG guarantees zero hallucinations.

Classification:

**Retrieval/source coverage issue**

This should not be treated as a prompt-only failure.

---

## Prompt Comparison

### Prompt V1

The original prompt instructed the LLM to:

- Answer only using provided context
- Refuse unsupported information
- Avoid guessing

### Prompt V2

Prompt V2 added:

- Distinction between directly supported and merely related information
- Explicit prohibition against filling evidence gaps
- Source/section attribution when possible
- Stronger unsupported-answer rules

### Result

The tested V2 cases showed no observable behavioral change from V1.

Therefore:

**Prompt V2 alone did not improve the measured evaluation result.**

This indicates that the remaining limitations are primarily related to retrieval and knowledge-base coverage.

---

## Faithfulness Assessment

The system uses retrieved context as the basis for generation.

For unsupported questions, the system generally follows the grounding rule and refuses rather than inventing information.

The Q21 diagnostic demonstrated that the retrieval stage can return semantically related information that is insufficient to answer the exact question.

Therefore:

**Faithfulness limitation identified: relevant topic retrieval does not always mean sufficient evidence retrieval.**

---

## Engineering Conclusion

The baseline RAG system successfully demonstrates the complete pipeline:

Document
→ Chunking
→ Embeddings
→ Retrieval
→ Context
→ LLM
→ Grounded Answer

The baseline achieved:

**20/25 = 80%**

The evaluation revealed that improving RAG quality requires more than changing the LLM prompt.

The main improvement areas are:

1. Better knowledge-base coverage
2. Better retrieval for near-miss questions
3. More explicit source attribution
4. Systematic faithfulness evaluation
5. Before/after measurement

---

## Day 7 Status

- [x] 25-question evaluation created
- [x] Baseline evaluation completed
- [x] 20/25 baseline result recorded
- [x] Failure cases identified
- [x] Prompt V2 implemented
- [x] V1/V2 comparison performed
- [x] Q21 retrieval diagnostic completed
- [x] Retrieval limitation identified
- [ ] Final faithfulness metrics
- [ ] Final Day 7 PDF
- [ ] GitHub update