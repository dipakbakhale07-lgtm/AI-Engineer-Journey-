# RAG V1 — Day 7 Baseline Evaluation

This file records the baseline behavior before Day 7 grounding improvements.

Documents: 3

Total chunks: 32

Questions: 25

---

## Q1

**Question:** What is Artificial Intelligence?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.8349
- ai-fundamentals.md — similarity 0.5667
- ai-fundamentals.md — similarity 0.5571

**LLM Answer:**

According to the provided context in the SOURCE FILE: ai-fundamentals.md, Artificial Intelligence (AI) refers to the development of computer systems capable of carrying out tasks that typically demand human intelligence.

---

## Q2

**Question:** What is Machine Learning, and how is it related to Artificial Intelligence?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.7771
- ai-fundamentals.md — similarity 0.6883
- ai-fundamentals.md — similarity 0.6445

**LLM Answer:**

Machine Learning (ML) is a subset of Artificial Intelligence (AI) in which systems learn from data rather than relying on predefined rules or explicit programming.

---

## Q3

**Question:** What is Deep Learning?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.8747
- ai-fundamentals.md — similarity 0.6680
- ai-fundamentals.md — similarity 0.5521

**LLM Answer:**

Deep Learning is a specialized form of machine learning that relies on neural networks with many layers to capture intricate patterns in data.

---

## Q4

**Question:** What is Generative AI?

**Retrieved Sources:**

- llm-generative-ai.md — similarity 0.7961
- ai-fundamentals.md — similarity 0.5196
- ai-fundamentals.md — similarity 0.4752

**LLM Answer:**

Generative AI refers to artificial intelligence systems capable of creating new content based on a given input or prompt.

---

## Q5

**Question:** What is a Large Language Model (LLM)?

**Retrieved Sources:**

- llm-generative-ai.md — similarity 0.7832
- llm-generative-ai.md — similarity 0.5580
- rag-fundamentals.md — similarity 0.4921

**LLM Answer:**

An LLM stands for Large Language Model. An LLM is a machine learning model trained on vast quantities of textual data, enabling it to understand and generate human-like language.

---

## Q6

**Question:** What are embeddings, and why are they useful in AI applications?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.8062
- llm-generative-ai.md — similarity 0.7609
- rag-fundamentals.md — similarity 0.5516

**LLM Answer:**

Based on the provided context, an embedding is a numerical vector representation of information such as text that captures semantic meaning. The numerical values are not normally interpreted manually, but are used by AI systems to compare semantic relationships between pieces of information.

---

## Q7

**Question:** What is a vector database?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.6461
- rag-fundamentals.md — similarity 0.5914
- rag-fundamentals.md — similarity 0.3686

**LLM Answer:**

Based on the provided context, a vector database is not explicitly mentioned. Therefore, I could not find this information in the provided documents.

---

## Q8

**Question:** What is Retrieval-Augmented Generation (RAG)?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.6777
- llm-generative-ai.md — similarity 0.6365
- rag-fundamentals.md — similarity 0.5344

**LLM Answer:**

According to the provided context, Retrieval-Augmented Generation (RAG) is a system architecture that retrieves relevant information from a knowledge source and provides that information to a Large Language Model (LLM) before generating an answer. This is mentioned in both the "What is RAG?" section of the "RAG Fundamentals" file and the "RAG" section of the "LLM Generative AI" file.

---

## Q9

**Question:** What are the main stages of a basic RAG pipeline?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.3979
- llm-generative-ai.md — similarity 0.3947
- rag-fundamentals.md — similarity 0.3903

**LLM Answer:**

Based on the provided context, the main stages of a basic RAG pipeline are:

User Question
↓
Retrieve Relevant Information
↓
Relevant Context
↓
LLM
↓
Generated Answer

This is described in the first source file, "RAG Fundamentals.md", under the section "What is RAG?"

---

## Q10

**Question:** Why are documents divided into smaller chunks before being stored for retrieval?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.6869
- rag-fundamentals.md — similarity 0.6557
- rag-fundamentals.md — similarity 0.4698

**LLM Answer:**

According to the provided context, documents are divided into smaller chunks because it allows the retrieval system to find specific relevant sections instead of treating the entire document as one piece.

---

## Q11

**Question:** What is the role of an embedding model in a RAG system?

**Retrieved Sources:**

- llm-generative-ai.md — similarity 0.6774
- rag-fundamentals.md — similarity 0.6241
- rag-fundamentals.md — similarity 0.5984

**LLM Answer:**

According to the provided context, an embedding model enables the identification of information that is conceptually similar to a user's query, even when exact wording differs. It does this by converting both the document and the question into vector form, allowing the system to detect semantic similarity and retrieve the most relevant content accordingly. Therefore, the role of an embedding model in a RAG system is to facilitate the retrieval of relevant information by detecting semantic similarity.

---

## Q12

**Question:** What is the role of a retriever in a RAG application?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.5961
- rag-fundamentals.md — similarity 0.5407
- rag-fundamentals.md — similarity 0.5407

**LLM Answer:**

According to the provided context in the "RAG is an Architecture" section, a RAG application combines multiple components, including:

* Retrieval

Therefore, the role of a retriever in a RAG application is:

Retrieval

---

## Q13

**Question:** What is an AI agent?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.6917
- ai-fundamentals.md — similarity 0.4952
- llm-generative-ai.md — similarity 0.4593

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q14

**Question:** How can an AI agent use tools or APIs to complete a task?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.5415
- llm-generative-ai.md — similarity 0.3891
- ai-fundamentals.md — similarity 0.3775

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q15

**Question:** What is an API, and how can an AI application use one? --- These questions should NOT be answerable from the provided knowledge base. The assistant should clearly say that the information could not be found in the provided documents.

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.4854
- llm-generative-ai.md — similarity 0.4010
- ai-fundamentals.md — similarity 0.4004

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q16

**Question:** Who will be the Prime Minister of India in 2035?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.1194
- llm-generative-ai.md — similarity 0.0867
- llm-generative-ai.md — similarity 0.0782

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q17

**Question:** What will the price of Bitcoin be exactly one year from today?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.0911
- ai-fundamentals.md — similarity 0.0778
- ai-fundamentals.md — similarity 0.0668

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q18

**Question:** What is the private phone number of the person who created these documents?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.3160
- rag-fundamentals.md — similarity 0.1509
- rag-fundamentals.md — similarity 0.1362

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q19

**Question:** What is the exact revenue of OpenAI for the next financial year?

**Retrieved Sources:**

- llm-generative-ai.md — similarity 0.1023
- llm-generative-ai.md — similarity 0.0708
- ai-fundamentals.md — similarity 0.0632

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q20

**Question:** Which AI company will have the largest market share in 2035? --- These questions are designed to sound related to the knowledge base but require information that may not actually be supported by the documents.

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.3994
- ai-fundamentals.md — similarity 0.3299
- rag-fundamentals.md — similarity 0.2467

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q21

**Question:** Does using RAG guarantee that an LLM will never hallucinate?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.4885
- rag-fundamentals.md — similarity 0.4773
- rag-fundamentals.md — similarity 0.4721

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q22

**Question:** Is a vector database always better than a traditional database for every AI application?

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.4277
- llm-generative-ai.md — similarity 0.3256
- rag-fundamentals.md — similarity 0.3187

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q23

**Question:** Can an AI agent automatically perform any action that a user requests?

**Retrieved Sources:**

- ai-fundamentals.md — similarity 0.4770
- llm-generative-ai.md — similarity 0.3517
- ai-fundamentals.md — similarity 0.2550

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q24

**Question:** Does an LLM always retrieve information from a vector database before answering a question?

**Retrieved Sources:**

- llm-generative-ai.md — similarity 0.4970
- rag-fundamentals.md — similarity 0.4935
- rag-fundamentals.md — similarity 0.4716

**LLM Answer:**

I could not find this information in the provided documents.

---

## Q25

**Question:** If a document contains a topic but does not contain the specific answer to a question, should the RAG assistant still generate an answer from the LLM's general knowledge? --- The assistant should provide a clear answer based on the information contained in the approved documents. The assistant should not invent information. Expected fallback: > "I could not find this information in the provided documents." The assistant should distinguish between: - Information explicitly supported by the documents - Information that is related but not actually supported - Information that is completely outside the knowledge base The assistant should not present unsupported information as a document-grounded fact.

**Retrieved Sources:**

- rag-fundamentals.md — similarity 0.6919
- rag-fundamentals.md — similarity 0.6375
- rag-fundamentals.md — similarity 0.6049

**LLM Answer:**

According to the provided context, I could not find this information in the provided documents. The documents only discuss the general idea of RAG systems and how they retrieve relevant information from documents to provide context to the LLM. There is no mention of what to do when a document contains a topic but does not contain the specific answer to a question.

---

