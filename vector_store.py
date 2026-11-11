
import ollama
import faiss
import numpy as np

from config import OLLAMA_HOST, EMBEDDING_MODEL


def generate_embeddings(texts):

    client = ollama.Client(host=OLLAMA_HOST)

    response = client.embed(
        model=EMBEDDING_MODEL,
        input=texts
    )

    embeddings = np.array(
        response["embeddings"],
        dtype=np.float32
    )

    return embeddings


def build_vector_index(chunks):

    if not chunks:
        raise ValueError("No document chunks available.")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def search_documents(
    query,
    index,
    chunks,
    top_k=3
):
    if index is None or index.ntotal == 0:
        return []

    # Generate embedding for customer question
    query_embedding = generate_embeddings([query])

    # Normalize query embedding
    faiss.normalize_L2(query_embedding)

    # Search FAISS index
    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    search_results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        search_results.append({
            "score": float(score),
            "filename": chunks[idx]["filename"],
            "page": chunks[idx]["page"],
            "text": chunks[idx]["text"]
        })

    return search_results

