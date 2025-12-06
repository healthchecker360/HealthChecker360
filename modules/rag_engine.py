# modules/rag_engine.py
import pickle
from pathlib import Path
import faiss
from config import VECTOR_PATH, DEBUG

# ------------------------------
# Load FAISS vector store
# ------------------------------
def load_vector_store():
    """
    Load FAISS index and chunks. Returns (index, chunks) or (None, []) if fails.
    """
    INDEX_FILE = VECTOR_PATH / "faiss_index.bin"
    CHUNKS_FILE = VECTOR_PATH / "chunks.pkl"

    if not INDEX_FILE.exists() or not CHUNKS_FILE.exists():
        if DEBUG:
            print("[DEBUG] FAISS index or chunks file missing.")
        return None, []

    try:
        index = faiss.read_index(str(INDEX_FILE))
        with open(CHUNKS_FILE, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error loading FAISS index: {e}")
        return None, []

# ------------------------------
# Retrieve relevant chunks from FAISS
# ------------------------------
def retrieve_relevant_chunks(query, top_k=5):
    """
    Query FAISS vector store to retrieve most relevant document chunks.
    """
    index, chunks = load_vector_store()
    if index is None or not chunks:
        return []  # FAISS not available, fallback needed

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_vector = model.encode([query])
    try:
        D, I = index.search(query_vector, top_k)
        retrieved_chunks = [chunks[i] for i in I[0] if i < len(chunks)]
        return retrieved_chunks
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS search failed: {e}")
        return []
