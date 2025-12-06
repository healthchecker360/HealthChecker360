import os

# ==============================
# BASE PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Project base directory
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "vector_store")  # Path to store FAISS index & chunks
DOCS_PATH = os.path.join(BASE_DIR, "docs")  # Folder containing all medical guideline files

# ==============================
# MODEL CONFIGURATION
# ==============================
SENTENCE_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Sentence Transformer model

# ==============================
# RAG PARAMETERS
# ==============================
CHUNK_SIZE = 500  # Number of characters per chunk
TOP_K = 5  # Number of relevant chunks to retrieve for a query

# ==============================
# OTHER SETTINGS
# ==============================
SUPPORTED_DOCS = [".pdf", ".txt", ".docx"]  # Supported document types for ingestion

# Ensure folders exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)
