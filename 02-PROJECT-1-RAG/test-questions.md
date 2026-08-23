# RAG Knowledge Assistant — Evaluation Questions

## Purpose

This question set will be used to evaluate whether the RAG Knowledge Assistant can:

- Retrieve the correct information
- Answer using the provided documents
- Connect information from different parts of the knowledge base
- Avoid unsupported claims
- Refuse questions when the required information is not available

Total Questions: 25

---

# Section A — Normal / Answerable Questions

## Q1
What is Artificial Intelligence?

## Q2
What is Machine Learning, and how is it related to Artificial Intelligence?

## Q3
What is Deep Learning?

## Q4
What is Generative AI?

## Q5
What is a Large Language Model (LLM)?

## Q6
What are embeddings, and why are they useful in AI applications?

## Q7
What is a vector database?

## Q8
What is Retrieval-Augmented Generation (RAG)?

## Q9
What are the main stages of a basic RAG pipeline?

## Q10
Why are documents divided into smaller chunks before being stored for retrieval?

## Q11
What is the role of an embedding model in a RAG system?

## Q12
What is the role of a retriever in a RAG application?

## Q13
What is an AI agent?

## Q14
How can an AI agent use tools or APIs to complete a task?

## Q15
What is an API, and how can an AI application use one?

---

# Section B — Unanswerable Questions

These questions should NOT be answerable from the provided knowledge base.

The assistant should clearly say that the information could not be found in the provided documents.

## Q16
Who will be the Prime Minister of India in 2035?

## Q17
What will the price of Bitcoin be exactly one year from today?

## Q18
What is the private phone number of the person who created these documents?

## Q19
What is the exact revenue of OpenAI for the next financial year?

## Q20
Which AI company will have the largest market share in 2035?

---

# Section C — Tricky / Near-Miss Questions

These questions are designed to sound related to the knowledge base but require information that may not actually be supported by the documents.

## Q21
Does using RAG guarantee that an LLM will never hallucinate?

## Q22
Is a vector database always better than a traditional database for every AI application?

## Q23
Can an AI agent automatically perform any action that a user requests?

## Q24
Does an LLM always retrieve information from a vector database before answering a question?

## Q25
If a document contains a topic but does not contain the specific answer to a question, should the RAG assistant still generate an answer from the LLM's general knowledge?

---

# Expected Behavior

### Normal Questions

The assistant should provide a clear answer based on the information contained in the approved documents.

### Unanswerable Questions

The assistant should not invent information.

Expected fallback:

> "I could not find this information in the provided documents."

### Tricky / Near-Miss Questions

The assistant should distinguish between:

- Information explicitly supported by the documents
- Information that is related but not actually supported
- Information that is completely outside the knowledge base

The assistant should not present unsupported information as a document-grounded fact.