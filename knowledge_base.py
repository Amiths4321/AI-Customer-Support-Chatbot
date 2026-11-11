
import os
import json
import faiss

KNOWLEDGE_BASE_DIR = "knowledge_base"

INDEX_FILE = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "company.index"
)

CHUNKS_FILE = os.path.join(
    KNOWLEDGE_BASE_DIR,
    "company_chunks.json"
)


def save_knowledge_base(index, chunks):

    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, INDEX_FILE)

    # Save document chunks as JSON
    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)

    return True


def load_knowledge_base():

    if not (
        os.path.exists(INDEX_FILE)
        and os.path.exists(CHUNKS_FILE)
    ):
        return None, []

    # Load FAISS index
    index = faiss.read_index(INDEX_FILE)

    # Load document chunks
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Verify index and chunk counts
    if index.ntotal != len(chunks):
        raise ValueError(
            "Knowledge base is inconsistent. "
            "Index and chunk counts do not match."
        )

    return index, chunks
