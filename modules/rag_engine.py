import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss
from config import VECTOR_STORE_PATH, SENTENCE_MODEL_NAME, TOP_K

# ==============================
# LOAD VECTOR STORE
# ==============================
def load_vector_store():
    chunks_file = os.path.join(VECTOR_STORE_PATH, "chunks.pkl")
    faiss_file = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")

    if not os.path.exists(chunks_file) or not os.path.exists(faiss_file):
        raise FileNotFoundError(
            "FAISS index or chunks file not found! Run 'build_faiss.py' first."
        )

    with open(chunks_file, "rb") as f:
        chunks = pickle.load(f)

    index = faiss.read_index(faiss_file)
    return index, chunks

# ==============================
# RETRIEVE RELEVANT CHUNKS
# ==============================
def retrieve_relevant_chunks(query, top_k=TOP_K):
    index, chunks = load_vector_store()

    # Encode query
    model = SentenceTransformer(SENTENCE_MODEL_NAME)
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)
    relevant_chunks = [chunks[i] for i in indices[0]]

    return relevant_chunks
