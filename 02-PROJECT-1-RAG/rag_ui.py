from pathlib import Path
import html

import numpy as np
import requests
import streamlit as st
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DOCUMENTS_PATH = BASE_DIR / "documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3:latest"

TOP_K = 3

FALLBACK_MESSAGE = (
    "I could not find this information in the provided documents."
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("🤖 RAG Assistant")

st.write(
    "Ask a question based on the available knowledge documents."
)


# ============================================================
# LOAD DOCUMENTS
# ============================================================

@st.cache_data
def load_documents():
    """
    Load Markdown knowledge documents.
    """

    documents = []

    for file_path in sorted(
        DOCUMENTS_PATH.glob("*.md")
    ):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "filename": file_path.name,
                "text": text
            }
        )

    if not documents:
        raise FileNotFoundError(
            "No knowledge documents were found."
        )

    return documents


# ============================================================
# CHUNKING
# ============================================================

def section_based_chunks(text):
    """
    Split Markdown content using level-2 headings.
    """

    lines = text.strip().splitlines()

    chunks = []
    current = []

    for line in lines:

        if line.startswith("## "):

            if current:
                chunks.append(
                    "\n".join(current).strip()
                )

            current = [line]

        elif current:

            current.append(line)

    if current:
        chunks.append(
            "\n".join(current).strip()
        )

    return [
        chunk
        for chunk in chunks
        if chunk
    ]


# ============================================================
# BUILD VECTOR DATABASE
# ============================================================

def build_vector_database(documents):
    """
    Create chunks while preserving source filenames.
    """

    database = []

    for document in documents:

        chunks = section_based_chunks(
            document["text"]
        )

        for chunk in chunks:

            database.append(
                {
                    "filename": document["filename"],
                    "text": chunk
                }
            )

    return database


# ============================================================
# EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        EMBEDDING_MODEL
    )


# ============================================================
# CREATE DOCUMENT EMBEDDINGS
# ============================================================

@st.cache_resource
def create_embeddings(texts):

    model = load_embedding_model()

    return model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(
    query_vector,
    document_vectors
):
    """
    Calculate cosine similarity between
    the question and document vectors.
    """

    query_norm = np.linalg.norm(
        query_vector
    )

    document_norms = np.linalg.norm(
        document_vectors,
        axis=1
    )

    return (
        np.dot(
            document_vectors,
            query_vector
        )
        /
        (
            document_norms
            * query_norm
            + 1e-10
        )
    )


# ============================================================
# RETRIEVE RELEVANT CHUNKS
# ============================================================

def retrieve(
    question,
    model,
    document_embeddings,
    database
):
    """
    Retrieve the top relevant chunks.
    """

    question_vector = model.encode(
        question,
        convert_to_numpy=True
    )

    scores = cosine_similarity(
        question_vector,
        document_embeddings
    )

    ranked_indices = np.argsort(
        scores
    )[::-1]

    top_indices = ranked_indices[:TOP_K]

    results = []

    for index in top_indices:

        results.append(
            {
                "text": database[index]["text"],
                "filename": database[index]["filename"],
                "score": float(scores[index])
            }
        )

    return results


# ============================================================
# GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(
    question,
    retrieved_results
):
    """
    Generate a detailed grounded answer
    using only retrieved context.
    """

    retrieved_text = "\n\n---\n\n".join(
        item["text"]
        for item in retrieved_results
    )

    prompt = f"""
You are a helpful document-based AI assistant.

Your job is to answer the user's question using ONLY the information
provided in the retrieved context.

IMPORTANT ANSWER RULES:

1. Give a clear, useful, and properly explained answer.
2. Do not give only a one-line answer when the context contains enough
   information for a fuller explanation.
3. For explanatory questions, write approximately 2 to 5 complete
   sentences.
4. Include important details from the retrieved context.
5. You may use short bullet points when they make the answer clearer.
6. Do not add information that is not present in the retrieved context.
7. Do not use outside knowledge.
8. Do not invent or guess facts.
9. If the answer cannot be found in the retrieved context, respond
   exactly with:

"{FALLBACK_MESSAGE}"

RETRIEVED CONTEXT:
------------------
{retrieved_text}

USER QUESTION:
--------------
{question}

Write a clear and detailed grounded answer:
"""

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,

            "options": {
                "temperature": 0.3,
                "num_predict": 500
            }
        },

        timeout=60
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

try:

    documents = load_documents()

    database = build_vector_database(
        documents
    )

    model = load_embedding_model()

    document_texts = [
        item["text"]
        for item in database
    ]

    document_embeddings = create_embeddings(
        tuple(document_texts)
    )

except Exception:

    st.error(
        "The knowledge base could not be loaded."
    )

    st.stop()


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "Enter your question:",
    placeholder=(
        "What is Retrieval-Augmented Generation?"
    )
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button("Ask"):

    # --------------------------------------------------------
    # EMPTY QUESTION
    # --------------------------------------------------------

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            # ------------------------------------------------
            # RETRIEVAL
            # ------------------------------------------------

            retrieved_results = retrieve(
                question.strip(),
                model,
                document_embeddings,
                database
            )

            # ------------------------------------------------
            # GENERATE ANSWER
            # ------------------------------------------------

            answer = generate_answer(
                question.strip(),
                retrieved_results
            )

            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            st.success(
                "Answer generated successfully."
            )

            # ------------------------------------------------
            # QUESTION
            # ------------------------------------------------

            st.subheader("Question")

            st.write(
                question.strip()
            )

            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            st.subheader("Answer")

            st.markdown(
                f"""
                <div style="
                    font-size: 20px;
                    line-height: 1.8;
                    white-space: normal;
                    overflow-wrap: break-word;
                ">
                    {
                        html.escape(answer)
                        .replace(chr(10), "<br>")
                    }
                </div>
                """,
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # SOURCE
            # ------------------------------------------------

            st.subheader("Source")

            source_files = []

            for item in retrieved_results:

                filename = item["filename"]

                if filename not in source_files:

                    source_files.append(
                        filename
                    )

            for filename in source_files:

                st.write(filename)

        # ----------------------------------------------------
        # OLLAMA CONNECTION FAILURE
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "I could not connect to the AI model. "
                "Please make sure Ollama is running and try again."
            )

        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            st.error(
                "The AI model took too long to respond. "
                "Please try again."
            )

        # ----------------------------------------------------
        # API FAILURE
        # ----------------------------------------------------

        except requests.exceptions.RequestException:

            st.error(
                "The AI service could not process your request. "
                "Please try again."
            )

        # ----------------------------------------------------
        # GENERAL ERROR
        # ----------------------------------------------------

        except Exception:

            st.error(
                "Something went wrong while processing "
                "your question. Please try again."
            )