# modules/ai_engine.py
import os
import pickle
from pathlib import Path
from gtts import gTTS
from fpdf import FPDF
import requests
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------ CONFIG ------------------------------
# These come from your .env or can be hardcoded for testing
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBMAiTquPaVv-b0SP9K8b-Ee-kDCB7h1gw"
GEMINI_API_URL = os.getenv("GEMINI_API_URL") or "https://api.gemini.com/v1/"
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "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"
GROQ_API_URL = os.getenv("GROQ_API_URL") or "https://api.groq.com/v1/"
TOP_K = int(os.getenv("TOP_K", 5))
PDF_FOLDER = Path(os.getenv("PDF_FOLDER") or "pdfs/")
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH") or "vector_store/")
DEBUG = os.getenv("DEBUG", "True") == "True"

PDF_FOLDER.mkdir(parents=True, exist_ok=True)

# ------------------------------ PDF generation ------------------------------
def text_to_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf_file = PDF_FOLDER / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Ensure Unicode-safe text
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line.encode("latin-1", "replace").decode("latin-1"))
    pdf.output(str(pdf_file))
    return str(pdf_file)

# ------------------------------ Audio generation ------------------------------
def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    audio_file = PDF_FOLDER / filename
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_file))
    return str(audio_file)

# ------------------------------ Gemini API ------------------------------
def query_gemini(query: str) -> str:
    url = GEMINI_API_URL + "text-bison-001:generateText"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "temperature": 0.2, "maxOutputTokens": 512}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        if DEBUG:
            print("[DEBUG] Gemini response:", result)
        return result['candidates'][0]['content']
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Gemini API error: {e}")
        return ""

# ------------------------------ Groq API ------------------------------
def query_groq(query: str) -> str:
    url = GROQ_API_URL + "generate"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "max_tokens": 512, "temperature": 0.2}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        if DEBUG:
            print("[DEBUG] Groq response:", result)
        return result.get('text', '')
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Groq API error: {e}")
        return ""

# ------------------------------ Main clinical answer ------------------------------
def generate_clinical_answer(query: str, top_k: int = TOP_K) -> str:
    answer = ""

    # Step 1: Try local FAISS
    try:
        chunks = retrieve_relevant_chunks(query, top_k=top_k)
        if chunks:
            answer = "\n\n".join([f"• {chunk.strip()}" for chunk in chunks])
            if DEBUG:
                print("[DEBUG] FAISS retrieved chunks")
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval skipped: {e}")

    # Step 2: Gemini fallback
    if not answer.strip():
        answer = query_gemini(query)
        if DEBUG:
            print("[DEBUG] Using Gemini fallback")

    # Step 3: Groq fallback
    if not answer.strip():
        answer = query_groq(query)
        if DEBUG:
            print("[DEBUG] Using Groq fallback")

    # Step 4: Final fallback
    if not answer.strip():
        answer = "⚠️ No answer found locally or online. Please consult a healthcare professional."

    return answer
