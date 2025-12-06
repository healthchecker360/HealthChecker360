import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    VECTOR_FOLDER,
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    EMBED_MODEL,
    TOP_K
)


# ------------------------------------------------------
# Load Embedding Model (loaded once)
# ------------------------------------------------------
def load_embedder():
    """Load the sentence transformer embedding model."""
    try:
        model = SentenceTransformer(EMBED_MODEL)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading embedding model: {e}")


# ------------------------------------------------------
# Load FAISS Index + Chunks
# ------------------------------------------------------
def load_vector_store():
    """Load FAISS index and chunk data."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError("FAISS index file not found. Build FAISS first.")

    if not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError("Chunks file not found. Build FAISS first.")

    # Load FAISS index
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
    except Exception as e:
        raise RuntimeError(f"Error reading FAISS index: {e}")

    # Load chunks
    try:
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading chunks.pkl: {e}")

    return index, chunks


# ------------------------------------------------------
# Retrieve Relevant Text Chunks
# ------------------------------------------------------
def retrieve_relevant_chunks(query: str, top_k: int = TOP_K):
    """Embed user query → search FAISS → return top K chunks."""
    
    embedder = load_embedder()

    # Convert query to vector
    try:
        query_vec = embedder.encode([query])
    except Exception as e:
        raise RuntimeError(f"Embedding error: {e}")

    # Load index + chunks
    index, chunks = load_vector_store()

    # Search index
    try:
        distances, indices = index.search(query_vec, top_k)
    except Exception as e:
        raise RuntimeError(f"FAISS search error: {e}")

    # Collect results
    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results
