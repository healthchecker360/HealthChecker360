import os
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# API KEYS & URLs
# ------------------------------

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://api.gemini.com/v1/")

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/v1/")

# ------------------------------
# Text-to-Speech Settings
# ------------------------------
TTS_LANG = os.getenv("TTS_LANG", "en")   # default to English

# ------------------------------
# RAG / FAISS Settings
# ------------------------------
TOP_K = int(os.getenv("TOP_K", 5))  # Number of top relevant chunks to retrieve

# ------------------------------
# PDF & Vector Store Paths
# ------------------------------
PDF_FOLDER = os.getenv("PDF_FOLDER", "pdfs/")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store/")
