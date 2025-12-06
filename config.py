import os
from dotenv import load_dotenv

# ----------------------------------
# Load Environment Variables
# ----------------------------------
load_dotenv()

# ----------------------------------
# API Keys
# ----------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ----------------------------------
# RAG / Vector Store Settings
# ----------------------------------
VECTOR_FOLDER = "vector_store"
FAISS_INDEX_PATH = os.path.join(VECTOR_FOLDER, "faiss_index.bin")
CHUNKS_PATH = os.path.join(VECTOR_FOLDER, "chunks.pkl")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ----------------------------------
# PDF / File Settings
# ----------------------------------
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# ----------------------------------
# Model Settings
# ----------------------------------
DEFAULT_ENGINE = "gemini"   # gemini / openai / local
TOP_K = 5                    # number of retrieved chunks

# ----------------------------------
# UI Settings
# ----------------------------------
APP_NAME = "HealthChecker 360"
APP_DESCRIPTION = "AI-powered Clinical Decision Support System"

# ----------------------------------
# Lab Interpretation Settings
# ----------------------------------
LAB_REFERENCE = "labs_reference.json"  # future file

# ----------------------------------
# Safety Settings
# ----------------------------------
MAX_QUERY_LENGTH = 500
