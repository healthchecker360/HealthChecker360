import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ------------------------------
# Paths
# ------------------------------
VECTOR_FOLDER = "vector_store"
INDEX_FILE = os.path.join(VECTOR_FOLDER, "faiss_index.idx")
TEXTS_FILE = os.path.join(VECTOR_FOLDER, "texts.pkl")

# ------------------------------
# Load SentenceTransformer model for embedding queries
# ------------------------------
MODEL_NAME = "all-MiniLM-L6-v2"  # Lightweight and fast
model = SentenceTransformer(MODEL_NAME)

# ------------------------------
# Load FAISS index and texts
# ------------------------------
if not os.path.exists(INDEX_FILE) or not os.path.exists(TEXTS_FILE):
    raise FileNotFoundError(
        "FAISS index or texts.pkl not found. Please run build_faiss.py first."
    )

index = faiss.read_index(INDEX_FILE)

with open(TEXTS_FILE, "rb") as f:
    texts = pickle.load(f)

# ------------------------------
# RAG Retrieval Function
# ------------------------------
def retrieve_relevant_chunks(query, top_k=5):
    """
    Retrieve top-k most relevant text chunks from PDF data using FAISS.

    Parameters:
    - query (str): The text query.
    - top_k (int): Number of top relevant chunks to return.

    Returns:
    - List[str]: Top-k relevant text chunks.
    """
    if not query.strip():
        return []

    # Convert query to embedding
    query_vec = model.encode([query], convert_to_numpy=True)

    # Search FAISS index
    distances, indices = index.search(query_vec, top_k)

    # Retrieve corresponding texts
    results = []
    for idx in indices[0]:
        if idx < len(texts):
            results.append(texts[idx])

    return results
