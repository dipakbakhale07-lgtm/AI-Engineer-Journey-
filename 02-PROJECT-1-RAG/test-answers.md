# RAG Knowledge Assistant — Expected Answers

## Purpose

This file contains the expected answer or expected behavior for the 25 evaluation questions.

Important:

These are expected results for the evaluation design stage.

Final answers and Pass/Fail results will be recorded only after the actual knowledge documents are prepared and the RAG system is tested.

---

# Section A — Normal / Answerable Questions

## Q1 — What is Artificial Intelligence?

### Expected Answer

Artificial Intelligence (AI) is the broad field of creating systems that can perform tasks associated with intelligent behavior, such as understanding language, recognizing patterns, making predictions, generating content, or taking actions.

### Expected Behavior

Answer using information supported by the provided documents.

---

## Q2 — What is Machine Learning, and how is it related to Artificial Intelligence?

### Expected Answer

Machine Learning (ML) is a subset of Artificial Intelligence in which systems learn patterns from data and use those patterns to make predictions or decisions.

### Expected Behavior

Clearly explain the relationship:

AI → broader field
ML → subset of AI

---

## Q3 — What is Deep Learning?

### Expected Answer

Deep Learning is a subset of Machine Learning that commonly uses neural networks with multiple layers to learn patterns from data.

### Expected Behavior

The answer should remain grounded in the provided documents.

---

## Q4 — What is Generative AI?

### Expected Answer

Generative AI refers to AI systems that can generate new content such as text, images, audio, code, or other forms of content.

### Expected Behavior

The answer should explain the concept using information supported by the documents.

---

## Q5 — What is a Large Language Model (LLM)?

### Expected Answer

A Large Language Model (LLM) is an AI model designed to work with language and can perform tasks such as generating text, answering questions, summarizing information, explaining concepts, and generating or transforming code.

### Expected Behavior

The answer should be supported by the knowledge base.

---

## Q6 — What are embeddings, and why are they useful in AI applications?

### Expected Answer

Embeddings are numerical vector representations of information such as text. They are useful for tasks such as semantic similarity search and retrieval because similar information can be represented by similar vectors.

### Expected Behavior

The answer should explain both:
1. What an embedding is
2. Why it is useful

---

## Q7 — What is a vector database?

### Expected Answer

A vector database is a system designed to store and retrieve vector representations of information, allowing applications to perform similarity-based or semantic searches.

### Expected Behavior

The answer should connect vector databases to embeddings and retrieval.

---

## Q8 — What is Retrieval-Augmented Generation (RAG)?

### Expected Answer

RAG stands for Retrieval-Augmented Generation. It is an approach where relevant information is retrieved from a knowledge source and provided to an LLM as context before the LLM generates an answer.

### Expected Behavior

The answer should explain the connection between retrieval and generation.

---

## Q9 — What are the main stages of a basic RAG pipeline?

### Expected Answer

A basic RAG pipeline can be represented as:

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
Relevant Context
↓
LLM
↓
Answer