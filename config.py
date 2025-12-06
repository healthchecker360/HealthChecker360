# config.py
import os

# Path to vector store (FAISS index + chunks)
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")

# Path to drug database (JSON)
DRUG_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "drug_db.json")
