import os
import pickle
from pathlib import Path
from gtts import gTTS
from fpdf import FPDF
import requests
from config import VECTOR_PATH, TEMP_PATH, TOP_K, DEBUG, GOOGLE_API_KEY, GROQ_API_KEY
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------ PDF generation ------------------------------
def text_to_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf_file = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        try:
            pdf.multi_cell(0, 8, line.encode('latin-1', 'replace').decode('latin-1'))
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] PDF encoding error: {e}")
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
    if not GOOGLE_API_KEY:
        if DEBUG:
            print("[DEBUG] GEMINI_API_KEY missing")
        return ""
    url = "https://api.generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
    headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "temperature": 0.2, "maxOutputTokens": 512}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Gemini API error: {e}")
        return ""

# ------------------------------ Groq API ------------------------------
def query_groq(query: str) -> str:
    if not GROQ_API_KEY:
        if DEBUG:
            print("[DEBUG] GROQ_API_KEY missing")
        return ""
    url = "https://api.groq.ai/v1/generate"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "max_tokens": 512, "temperature": 0.2}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result.get('text', '')
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Groq API error: {e}")
        return ""

# ------------------------------ Main clinical answer ------------------------------
def generate_clinical_answer(query: str, top_k: int = TOP_K) -> str:
    answer = ""

    # Step 1: Local FAISS retrieval
    try:
        chunks = retrieve_relevant_chunks(query, top_k=top_k)
        if DEBUG:
            print(f"[DEBUG] FAISS retrieved {len(chunks)} chunks")
        if chunks:
            answer = "\n\n".join([f"• {chunk.strip()}" for chunk in chunks])
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval skipped: {e}")

    # Step 2: Gemini fallback
    if not answer.strip():
        answer = query_gemini(query)
        if DEBUG:
            print(f"[DEBUG] Gemini answer length: {len(answer)}")

    # Step 3: Groq fallback
    if not answer.strip():
        answer = query_groq(query)
        if DEBUG:
            print(f"[DEBUG] Groq answer length: {len(answer)}")

    # Step 4: Final fallback
    if not answer.strip():
        answer = "⚠️ No answer found locally or online. Please consult a healthcare professional."

    return answer
