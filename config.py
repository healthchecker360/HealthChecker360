import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# Project Paths
# ------------------------------
BASE_DIR = Path(__file__).parent.resolve()

DOCS_PATH = BASE_DIR / "docs"             # Medical guidelines PDFs/TXT/DOCX
VECTOR_PATH = BASE_DIR / "vector_store"   # FAISS embeddings
TEMP_PATH = BASE_DIR / "temp"             # Generated PDFs & audio
DRUG_DB_PATH = BASE_DIR / "database" / "drugs.json"  # Drug database (JSON)
LAB_DB_PATH = BASE_DIR / "database" / "labs.json"    # Lab reference database (JSON)

VECTOR_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)
(DRUG_DB_PATH.parent).mkdir(parents=True, exist_ok=True)
(LAB_DB_PATH.parent).mkdir(parents=True, exist_ok=True)

# ------------------------------
# API KEYS
# ------------------------------
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY", "")

# ------------------------------
# RAG / Engine Settings
# ------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3

# Debug mode
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
