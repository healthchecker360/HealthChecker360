import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ------------------------------
# Paths
# ------------------------------
VECTOR_FOLDER = "vector_store"
INDEX_FILE = os.path.join(VECTOR_FOLDER, "index.faiss")
CHUNKS_FILE = os.path.join(VECTOR_FOLDER, "chunks.pkl")

# ------------------------------
# Embedding Model
# ------------------------------
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------
# Load Vector Store
# ------------------------------
def load_vector_store():
    """
    Loads FAISS index and stored text chunks.
    Raises an error if files are missing.
    """
    if not os.path.exists(INDEX_FILE) or not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(
            "FAISS index or chunks.pkl not found in vector_store/. "
            "Please run build_faiss.py or upload the required files."
        )

    index = faiss.read_index(INDEX_FILE)

    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks

# ------------------------------
# Retrieve Relevant Chunks
# ------------------------------
def retrieve_relevant_chunks(query, top_k=5):
    """
    Retrieves top-K relevant document chunks based on semantic similarity.
    """
    index, chunks = load_vector_store()

    query_emb = EMBED_MODEL.encode([query])
    query_emb = np.array(query_emb).astype("float32")

    distances, indices = index.search(query_emb, top_k)

    relevant = []
    for idx in indices[0]:
        if idx < len(chunks):
            relevant.append(chunks[idx])

    return relevant
