import pickle
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

# ------------------------------
# PATHS
# ------------------------------
VECTOR_PATH = Path("vector_store")
CHUNKS_FILE = VECTOR_PATH / "chunks.pkl"
INDEX_FILE = VECTOR_PATH / "faiss_index.bin"

# ------------------------------
# LOAD VECTOR STORE
# ------------------------------
def load_vector_store():
    """
    Load FAISS index and chunks from disk.
    """
    if not CHUNKS_FILE.exists() or not INDEX_FILE.exists():
        raise FileNotFoundError(
            "FAISS index or chunks file not found! Run build_faiss.py first."
        )

    # Load chunks
    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    # Load FAISS index
    index = faiss.read_index(str(INDEX_FILE))

    return index, chunks

# ------------------------------
# RETRIEVE RELEVANT CHUNKS
# ------------------------------
def retrieve_relevant_chunks(query, top_k=5):
    """
    Retrieve top-k relevant chunks for a user query.
    """
    index, chunks = load_vector_store()

    # Embed the query
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query]).astype("float32")

    # Search
    distances, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0]]

    return results
