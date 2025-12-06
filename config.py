# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ------------------------------
# Paths
# ------------------------------
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "vector_store/"))
TEMP_PATH = Path(os.getenv("PDF_FOLDER", "pdfs/"))
TEMP_PATH.mkdir(exist_ok=True, parents=True)

# ------------------------------
# API Keys
# ------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")

# ------------------------------
# Other Config
# ------------------------------
TOP_K = int(os.getenv("TOP_K", 5))
DEBUG = os.getenv("DEBUG", "True") == "True"
TTS_LANG = os.getenv("TTS_LANG", "en")
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY")
