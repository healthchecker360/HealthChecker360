import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
VECTOR_FOLDER = "vector_store"
INDEX_FILE = os.path.join(VECTOR_FOLDER, "faiss_index.bin")
CHUNKS_FILE = os.path.join(VECTOR_FOLDER, "chunks.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"   # Small & HF-friendly model

# ---------------------------------------------------
# Load Embedding Model
# ---------------------------------------------------
@st.cache_resource
def load_encoder():
    return SentenceTransformer(MODEL_NAME)

encoder = load_encoder()

# ---------------------------------------------------
# Load Vector Index
# ---------------------------------------------------
def load_vector_store():
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError("FAISS index file not found!")

    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError("Chunks file not found!")

    # Load FAISS
    index = faiss.read_index(INDEX_FILE)

    # Load chunks
    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks

# ---------------------------------------------------
# Encode Query
# ---------------------------------------------------
def embed_text(text: str):
    emb = encoder.encode([text], convert_to_numpy=True)
    return np.array(emb).astype("float32")

# ---------------------------------------------------
# Retrieve Relevant Chunks
# ---------------------------------------------------
def retrieve_relevant_chunks(query, top_k=5):
    index, chunks = load_vector_store()

    query_vec = embed_text(query)

    # Search vectors
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])

    return results
