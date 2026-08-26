from pathlib import Path

import numpy as np
import requests
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DOCUMENTS_PATH = Path("documents")
QUESTIONS_PATH = Path("test-questions.md")
RESULTS_PATH = Path("baseline_results.md")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3:latest"

TOP_K = 3


# ============================================================
# DOCUMENT LOADING
# ============================================================

def load_documents(folder_path: Path) -> list[dict]:
    """Load all Markdown documents from the documents folder."""

    documents = []

    for file_path in sorted(folder_path.glob("*.md")):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "filename": file_path.name,
            "text": text,
        })

    if not documents:
        raise FileNotFoundError(
            f"No Markdown documents found in: {folder_path}"
        )

    return documents


# ============================================================
# CHUNKING
# ============================================================

def section_based_chunks(text: str) -> list[str]:
    """Split Markdown content using level-2 headings."""

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

        elif not current:
            continue

        else:
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


def build_chunk_database(
    documents: list[dict]
) -> list[dict]:
    """Create chunks while preserving source filenames."""

    database = []

    for document in documents:

        chunks = section_based_chunks(
            document["text"]
        )

        for chunk in chunks:

            database.append({
                "filename": document["filename"],
                "text": chunk,
            })

    return database


# ============================================================
# SIMILARITY
# ============================================================

def cosine_similarity(
    query_vector: np.ndarray,
    document_vectors: np.ndarray
) -> np.ndarray:
    """Calculate cosine similarity."""

    query_norm = np.linalg.norm(
        query_vector
    )

    document_norms = np.linalg.norm(
        document_vectors,
        axis=1
    )

    return np.dot(
        document_vectors,
        query_vector
    ) / (
        document_norms * query_norm
    )


# ============================================================
# CONTEXT
# ============================================================

def build_context(
    database: list[dict],
    indices: np.ndarray
) -> str:
    """Build context from retrieved chunks."""

    retrieved_chunks = []

    for index in indices:

        item = database[index]

        retrieved_chunks.append(
            f"SOURCE FILE: {item['filename']}\n"
            f"{item['text']}"
        )

    return "\n\n---\n\n".join(
        retrieved_chunks
    )


# ============================================================
# LLM — PROMPT V2
# ============================================================

def generate_answer(
    question: str,
    context: str
) -> str:
    """Generate a grounded answer using Prompt V2."""

    prompt = f"""
You are a grounded RAG question-answering assistant.

Your answer must be based ONLY on the information contained
in the provided context.

Follow these rules:

1. If the context directly supports the answer,
   answer the question clearly.

2. If the context contains related information but does
   not provide enough evidence to answer the specific question,
   do not fill the gap using outside knowledge.

3. If the required information is not supported by the context,
   say exactly:

"I could not find this information in the provided documents."

4. Never invent facts, names, dates, numbers, predictions,
   or explanations that are not supported by the context.

5. Do not treat a related topic as proof of the answer.

6. When possible, mention the source file or section
   that supports your answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


# ============================================================
# QUESTION EXTRACTION
# ============================================================

def extract_questions(
    file_path: Path
) -> list[tuple[str, str]]:
    """Extract Q1-Q25 from test-questions.md."""

    text = file_path.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    questions = []

    current_id = None
    current_question = []

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("## Q"):

            if current_id and current_question:

                questions.append(
                    (
                        current_id,
                        " ".join(
                            current_question
                        ).strip()
                    )
                )

            current_id = (
                stripped
                .replace("## ", "")
                .strip()
            )

            current_question = []

        elif current_id:

            if stripped and not stripped.startswith("#"):

                current_question.append(
                    stripped
                )

    if current_id and current_question:

        questions.append(
            (
                current_id,
                " ".join(
                    current_question
                ).strip()
            )
        )

    return questions


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    question: str,
    model,
    embeddings: np.ndarray,
    database: list[dict]
) -> tuple[np.ndarray, np.ndarray]:

    query_embedding = model.encode(
        question
    )

    scores = cosine_similarity(
        query_embedding,
        embeddings
    )

    ranked_indices = np.argsort(
        scores
    )[::-1]

    top_indices = ranked_indices[
        :TOP_K
    ]

    return top_indices, scores


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 7 — RAG EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. LOAD DOCUMENTS
    # --------------------------------------------------------

    documents = load_documents(
        DOCUMENTS_PATH
    )

    print("\nDocuments loaded:")

    for document in documents:

        print(
            f"- {document['filename']} "
            f"({len(document['text'])} characters)"
        )

    # --------------------------------------------------------
    # 2. CREATE CHUNK DATABASE
    # --------------------------------------------------------

    database = build_chunk_database(
        documents
    )

    print(
        f"\nTotal chunks: {len(database)}"
    )

    # --------------------------------------------------------
    # 3. LOAD EMBEDDING MODEL
    # --------------------------------------------------------

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    # --------------------------------------------------------
    # 4. CREATE EMBEDDINGS
    # --------------------------------------------------------

    chunks = [
        item["text"]
        for item in database
    ]

    embeddings = model.encode(
        chunks
    )

    print(
        f"Embedding shape: "
        f"{embeddings.shape}"
    )

    # --------------------------------------------------------
    # 5. LOAD QUESTIONS
    # --------------------------------------------------------

    questions = extract_questions(
        QUESTIONS_PATH
    )

    print(
        f"Evaluation questions loaded: "
        f"{len(questions)}"
    )

    if len(questions) != 25:

        raise ValueError(
            f"Expected 25 questions, "
            f"found {len(questions)}"
        )

    # --------------------------------------------------------
    # 6. RUN EVALUATION
    # --------------------------------------------------------

    results = []

    for number, (
        question_id,
        question
    ) in enumerate(
        questions,
        start=1
    ):

        print(
            "\n" + "=" * 70
        )

        print(
            f"{question_id} — "
            f"{number}/25"
        )

        print(
            "=" * 70
        )

        print(
            f"\nQUESTION:\n{question}"
        )

        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        top_indices, scores = retrieve(
            question,
            model,
            embeddings,
            database
        )

        print(
            "\nRETRIEVED CHUNKS:"
        )

        retrieved_items = []

        for rank, index in enumerate(
            top_indices,
            start=1
        ):

            item = database[index]

            similarity = float(
                scores[index]
            )

            print(
                f"\nRank {rank}"
            )

            print(
                f"Similarity: "
                f"{similarity:.4f}"
            )

            print(
                f"Source: "
                f"{item['filename']}"
            )

            print(
                "-" * 60
            )

            print(
                item["text"]
            )

            retrieved_items.append({
                "source": item["filename"],
                "similarity": similarity,
                "text": item["text"],
            })

        # ----------------------------------------------------
        # CONTEXT
        # ----------------------------------------------------

        context = build_context(
            database,
            top_indices
        )

        print(
            "\nCONTEXT SENT TO LLM:"
        )

        print(
            "-" * 60
        )

        print(
            context
        )

        # ----------------------------------------------------
        # GENERATION
        # ----------------------------------------------------

        print(
            "\nLLM ANSWER:"
        )

        answer = generate_answer(
            question,
            context
        )

        print(
            answer
        )

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({
            "id": question_id,
            "question": question,
            "answer": answer,
            "retrieved": retrieved_items,
            "context": context,
        })

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    with RESULTS_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "# RAG V2 — Day 7 Evaluation\n\n"
        )

        file.write(
            "This file records the RAG behavior "
            "using the improved grounding Prompt V2.\n\n"
        )

        file.write(
            f"Documents: {len(documents)}\n\n"
        )

        file.write(
            f"Total chunks: {len(database)}\n\n"
        )

        file.write(
            f"Questions: {len(questions)}\n\n"
        )

        file.write(
            "---\n\n"
        )

        # ----------------------------------------------------
        # WRITE EACH RESULT
        # ----------------------------------------------------

        for result in results:

            file.write(
                f"## {result['id']}\n\n"
            )

            file.write(
                f"**Question:** "
                f"{result['question']}\n\n"
            )

            # -----------------------------------------------
            # RETRIEVED SOURCES
            # -----------------------------------------------

            file.write(
                "**Retrieved Sources:**\n\n"
            )

            for item in result["retrieved"]:

                file.write(
                    f"- {item['source']} — "
                    f"similarity "
                    f"{item['similarity']:.4f}\n"
                )

            # -----------------------------------------------
            # RETRIEVED CONTEXT
            # -----------------------------------------------

            file.write(
                "\n**Retrieved Context:**\n\n"
            )

            for item in result["retrieved"]:

                file.write(
                    f"### Source: "
                    f"{item['source']}\n\n"
                )

                file.write(
                    f"{item['text']}\n\n"
                )

            # -----------------------------------------------
            # LLM ANSWER
            # -----------------------------------------------

            file.write(
                "**LLM Answer:**\n\n"
            )

            file.write(
                f"{result['answer']}\n\n"
            )

            file.write(
                "---\n\n"
            )

    # ========================================================
    # COMPLETE
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "EVALUATION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        f"\nResults saved to: "
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()