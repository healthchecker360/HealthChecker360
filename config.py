import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()  # reads .env file in project root

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = Path(__file__).parent.resolve()

# Folders
DOCS_PATH = BASE_DIR / "pdfs"             # Place all your guideline files here (pdf, txt, docx)
VECTOR_PATH = BASE_DIR / "vector_store"   # FAISS index & chunks storage
TEMP_PATH = BASE_DIR / "temp"             # Generated PDFs, audio
LOG_PATH = BASE_DIR / "logs"              # Logs for debugging

# Auto-create directories if missing
for path in [DOCS_PATH, VECTOR_PATH, TEMP_PATH, LOG_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# FAISS index file
FAISS_INDEX_PATH = VECTOR_PATH / "faiss_index.bin"
CHUNKS_FILE_PATH = VECTOR_PATH / "chunks.pkl"

# ------------------------------
# API KEYS
# ------------------------------
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY", "")

# ------------------------------
# RAG Settings
# ------------------------------
CHUNK_SIZE = 1000           # characters per chunk
CHUNK_OVERLAP = 200         # overlap to avoid cutting sentences
TOP_K = 3                   # top K chunks retrieved per query

# ------------------------------
# Debug Mode
# ------------------------------
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
