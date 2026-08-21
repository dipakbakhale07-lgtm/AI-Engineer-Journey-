# DAY 2/30 - AI Concepts & Application Architecture

## 🎯 Goal

Review and organize the core AI concepts I have already learned and understand how these concepts connect together when building real AI applications.

This day is a foundation check based on my existing AI learning.

---

## 🧠 Concepts Reviewed

### 1. Artificial Intelligence (AI)

Artificial Intelligence is the umbrella term for different fields of study focused on creating systems that exhibit intelligent behavior.

AI includes disciplines such as learning, reasoning, language, and perception, and decision-making.

---

### 2. Machine Learning (ML)

Machine Learning is a specialty within AI that focuses on systems learning patterns from data and applying those patterns to make predictions or decisions.

I have already learned the fundamentals of ML as part of my AI Engineer learning roadmap.

---

### 3. Deep Learning

Deep Learning is a specialty within ML that focuses on neural networks with many layers.

It is used in fields such as computer vision, speech and language processing, and modern generative AI.

---

### 4. Neural Networks

Neural networks are a type of algorithm made from layers of interconnected nodes that process data and learn patterns from data.

They are the foundation of deep learning.

---

### 5. Generative AI

Generative AI is a type of AI that is capable of generating new text, code, images, audio, and other content.

---

### 6. Large Language Models (LLMs)

Large Language Models are AI systems that understand and generate human language.

They can be used for tasks such as answering questions, summarizing, coding, reasoning, and more.

---

### 7. Embeddings

Embeddings are a way of representing information, such as text, as a vector of numbers.

They enable similarity detection and are used in semantic search and recommendation systems.

---

### 8. Vector Database

A vector database is a database that stores and retrieves vector representations of information.

It is useful in AI applications because it enables semantic search.

---

### 9. RAG

RAG stands for Retrieval-Augmented Generation.

A RAG system retrieves relevant documents from a knowledge source and passes those documents to an LLM when answering a query.

RAG will be the focus of

Project 1 - RAG Knowledge Assistant

---

### 10. AI Agents

An AI agent is an AI system that can perform specific tasks or achieve goals.

An AI agent can use tools and access data to complete a task within its scope of control.

The practical multi-tool agent will be built as

Project 4.

---

### 11. API

An API defines how different software systems communicate with each other.

Many AI applications use APIs to interact with models or other systems.

---

# 🔗 AI Application Architecture

A simple AI application can be represented as follows:

```text

User

↓

Application

↓

LLM

↓

Tool / Data

↓

Answer

```
# 📚 RAG Architecture

The basic RAG flow can be represented as:

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
Answer