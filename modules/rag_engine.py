import os
import sys
import pickle
from sentence_transformers import SentenceTransformer
import faiss

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import VECTOR_STORE_PATH

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_vector_store():
    chunks_file = os.path.join(VECTOR_STORE_PATH, "chunks.pkl")
    index_file = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")

    if not os.path.exists(chunks_file) or not os.path.exists(index_file):
        raise FileNotFoundError("FAISS index or chunks file not found. Run build_faiss.py first.")

    with open(chunks_file, "rb") as f:
        chunks = pickle.load(f)

    index = faiss.read_index(index_file)
    return index, chunks

def retrieve_relevant_chunks(query, top_k=5):
    index, chunks = load_vector_store()
    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0]]
    return results
