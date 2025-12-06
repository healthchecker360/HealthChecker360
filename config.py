from pathlib import Path
import os

# ------------------------------
# FOLDER PATHS
# ------------------------------
DOCS_FOLDER = Path("docs")              # Your PDF/TXT/DOCX guidelines
VECTOR_FOLDER = Path("vector_store")    # FAISS vector index & chunks

# FAISS files
CHUNKS_FILE = VECTOR_FOLDER / "chunks.pkl"
FAISS_INDEX_FILE = VECTOR_FOLDER / "faiss_index.bin"

# ------------------------------
# DRUG DATABASE
# ------------------------------
DRUG_DB_PATH = DOCS_FOLDER / "drug_database.csv"

# ------------------------------
# GENAI / GEMINI / GROQ API CONFIG
# ------------------------------
# Store API keys in .env file
GENAI_API_KEY = os.getenv("GENAI_API_KEY")       # Your Gemni / GenAI API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")         # Your Groq API Key

# Base URLs (example)
GENAI_API_URL = "https://api.genai.com/v1/query"
GROQ_API_URL = "https://api.groq.com/v1/query"

# ------------------------------
# RAG / Search Settings
# ------------------------------
TOP_K_CHUNKS = 5  # Number of chunks to retrieve from FAISS
