import os
import pickle
from pathlib import Path
from gtts import gTTS
from fpdf import FPDF
import requests
from config import VECTOR_PATH, TEMP_PATH, TOP_K, DEBUG, GOOGLE_API_KEY, GROQ_API_KEY
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------
# PDF generation
# ------------------------------
def text_to_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf_file = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(str(pdf_file))
    return str(pdf_file)

# ------------------------------
# Audio generation
# ------------------------------
def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    audio_file = TEMP_PATH / filename
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_file))
    return str(audio_file)

# ------------------------------
# Online AI: Gemini
# ------------------------------
def query_gemini(query: str) -> str:
    if not GOOGLE_API_KEY:
        raise ValueError("GEMINI_API_KEY missing in .env")
    url = "https://api.generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
    headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "temperature": 0.2, "maxOutputTokens": 512}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result['candidates'][0]['content']

# ------------------------------
# Online AI: Groq (optional fallback)
# ------------------------------
def query_groq(query: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing in .env")
    url = "https://api.groq.ai/v1/generate"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "max_tokens": 512, "temperature": 0.2}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result.get('text', '')

# ------------------------------
# Main clinical answer function
# ------------------------------
def generate_clinical_answer(query: str, top_k: int = TOP_K) -> str:
    """
    Returns professional medical answer.
    1. Tries local FAISS vector store first.
    2. Falls back to Gemini API.
    3. Optional: fallback to Groq API if Gemini fails.
    """
    answer = ""

    # Step 1: Local FAISS retrieval
    try:
        faiss_index_file = VECTOR_PATH / "faiss_index.bin"
        chunks_file = VECTOR_PATH / "chunks.pkl"
        if faiss_index_file.exists() and chunks_file.exists():
            chunks = retrieve_relevant_chunks(query, top_k=top_k)
            if chunks:
                answer = "\n\n".join(chunks)
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval skipped: {e}")

    # Step 2: Online Gemini fallback
    if not answer.strip():
        try:
            answer = query_gemini(query)
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Gemini API failed: {e}")

    # Step 3: Groq fallback (if still empty)
    if not answer.strip():
        try:
            answer = query_groq(query)
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Groq API failed: {e}")
            answer = "No answer found locally or online. Please consult a healthcare professional."

    return answer
