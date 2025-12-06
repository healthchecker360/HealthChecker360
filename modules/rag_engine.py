import pickle
import faiss
from sentence_transformers import SentenceTransformer
from config import FAISS_INDEX_PATH, CHUNKS_FILE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, DEBUG

# ------------------------------
# Load FAISS index and chunks
# ------------------------------
def load_vector_store():
    """
    Load FAISS index and chunks from vector_store.
    Returns: index, chunks
    """
    if not FAISS_INDEX_PATH.exists() or not CHUNKS_FILE_PATH.exists():
        raise FileNotFoundError("FAISS index or chunks file not found! Run build_faiss.py first.")
    
    # Load FAISS index
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    # Load chunks
    with open(CHUNKS_FILE_PATH, "rb") as f:
        chunks = pickle.load(f)
    
    if DEBUG:
        print(f"Loaded FAISS index with {index.ntotal} vectors and {len(chunks)} chunks.")
    
    return index, chunks

# ------------------------------
# Retrieve relevant chunks
# ------------------------------
def retrieve_relevant_chunks(query, top_k=TOP_K):
    """
    Retrieve top_k chunks from FAISS most similar to query.
    Returns: list of chunks
    """
    index, chunks = load_vector_store()
    
    # Create embedding for the query
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode([query]).astype("float32")
    
    # Search
    distances, indices = index.search(query_vector, top_k)
    
    # Get corresponding chunks
    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])
    
    if DEBUG:
        print(f"Query: {query}")
        print(f"Top {top_k} chunks retrieved:")
        for r in results:
            print(r[:200], "...")  # show first 200 chars

    return results

# ------------------------------
# Optional: Online fallback placeholder
# ------------------------------
def fallback_online_search(query):
    """
    Placeholder function for API fallback (Gemini, Groq, Medscape, etc.)
    """
    # Implement API calls here
    # For example:
    # response = gemini_api_call(query)
    # return response["answer"]
    return "No local match found. This feature will use online medical databases."
