# modules/ai_engine.py
import os
import pickle
from pathlib import Path
import requests
from gtts import gTTS
from fpdf import FPDF
from config import VECTOR_STORE_PATH, TEMP_PATH, TOP_K, DEBUG, GEMINI_API_KEY, GEMINI_API_URL, GROQ_API_KEY, GROQ_API_URL
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------ PDF generation (Unicode safe) ------------------------------
def text_to_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf_file = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)  # use '' style for Unicode-safe
    for line in text.split("\n"):
        # remove unsupported characters
        safe_line = line.encode('latin-1', errors='replace').decode('latin-1')
        pdf.multi_cell(0, 8, safe_line)
    pdf.output(str(pdf_file))
    return str(pdf_file)

# ------------------------------ Audio generation ------------------------------
def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    audio_file = TEMP_PATH / filename
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_file))
    return str(audio_file)

# ------------------------------ Gemini API ------------------------------
def query_gemini(query: str) -> str:
    if not GEMINI_API_KEY or not GEMINI_API_URL:
        if DEBUG:
            print("[DEBUG] GEMINI_API_KEY or URL missing in .env")
        return ""
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "temperature": 0.2, "maxOutputTokens": 512}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result.get('candidates', [{}])[0].get('content', '').strip()
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Gemini API error: {e}")
        return ""

# ------------------------------ Groq API ------------------------------
def query_groq(query: str) -> str:
    if not GROQ_API_KEY or not GROQ_API_URL:
        if DEBUG:
            print("[DEBUG] GROQ_API_KEY or URL missing in .env")
        return ""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "max_tokens": 512, "temperature": 0.2}
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result.get('text', '').strip()
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Groq API error: {e}")
        return ""

# ------------------------------ Main clinical answer function ------------------------------
def generate_clinical_answer(query: str, top_k: int = TOP_K) -> str:
    """
    Returns professional medical answer:
    1. Tries local FAISS vector store first.
    2. Falls back to Gemini API.
    3. Falls back to Groq API if needed.
    """
    answer = ""

    # Step 1: Local FAISS retrieval
    try:
        chunks = retrieve_relevant_chunks(query, top_k=top_k)
        if chunks:
            answer = "\n\n".join([f"• {c.strip()}" for c in chunks])
        else:
            if DEBUG:
                print("[DEBUG] No local FAISS chunks found.")
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval failed: {e}")

    # Step 2: Gemini API fallback
    if not answer.strip():
        answer = query_gemini(query)
        if DEBUG:
            print("[DEBUG] Gemini API returned:", answer)

    # Step 3: Groq API fallback
    if not answer.strip():
        answer = query_groq(query)
        if DEBUG:
            print("[DEBUG] Groq API returned:", answer)

    # Step 4: Final fallback
    if not answer.strip():
        answer = "⚠️ No answer found locally or online. Please consult a healthcare professional."

    return answer
