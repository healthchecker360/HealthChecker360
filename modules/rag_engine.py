import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from config import VECTOR_PATH, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, DEBUG

# ------------------------------
# File paths
# ------------------------------
CHUNKS_FILE = VECTOR_PATH / "chunks.pkl"
INDEX_FILE = VECTOR_PATH / "faiss_index.bin"

# ------------------------------
# Load FAISS vector store
# ------------------------------
def load_vector_store():
    if not CHUNKS_FILE.exists() or not INDEX_FILE.exists():
        raise FileNotFoundError(
            "FAISS index or chunks file not found! Run build_faiss.py first."
        )

    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    index = faiss.read_index(str(INDEX_FILE))

    if DEBUG:
        print(f"[RAG] Loaded {len(chunks)} chunks from {INDEX_FILE}")

    return index, chunks

# ------------------------------
# Embed query and retrieve relevant chunks
# ------------------------------
def retrieve_relevant_chunks(query, top_k=TOP_K):
    index, chunks = load_vector_store()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])

    # If no results found, placeholder for online search (Gemini/Groq)
    if not results:
        results.append("[No local docs found] - fallback to online search required")

    if DEBUG:
        print(f"[RAG] Retrieved {len(results)} chunks for query: '{query}'")

    return results
