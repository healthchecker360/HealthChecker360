import os
import pickle
from pathlib import Path
from gtts import gTTS
from fpdf import FPDF
import requests
from config import VECTOR_PATH, TEMP_PATH, TOP_K, DEBUG, GOOGLE_API_KEY, GROQ_API_KEY
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------ PDF generation (Unicode safe) ------------------------------
def text_to_pdf(text: str, filename: str = "output.pdf") -> str:
    pdf_file = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    
    # Add a Unicode TrueType font (ensure this path exists on your system)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Common on Linux
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    
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
            print("[DEBUG] GEMINI_API_KEY missing in .env")
        return ""
    url = "https://api.generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
    headers = {"Authorization": f"Bearer {GOOGLE_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "temperature": 0.2, "maxOutputTokens": 512}
    try:
        response = requests.post(url, headers=headers, json=data)
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
            print("[DEBUG] GROQ_API_KEY missing in .env")
        return ""
    url = "https://api.groq.ai/v1/generate"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": query, "max_tokens": 512, "temperature": 0.2}
    try:
        response = requests.post(url, headers=headers, json=data)
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

    # Step 1: Try local FAISS
    try:
        chunks = retrieve_relevant_chunks(query, top_k=top_k)
        if chunks:
            answer = "\n\n".join([f"• {chunk.strip()}" for chunk in chunks])
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval skipped: {e}")

    # Step 2: Gemini API fallback
    if not answer.strip():
        answer = query_gemini(query)
        if DEBUG:
            print("[DEBUG] Using Gemini API fallback")

    # Step 3: Groq API fallback
    if not answer.strip():
        answer = query_groq(query)
        if DEBUG:
            print("[DEBUG] Using Groq API fallback")

    # Step 4: Final fallback
    if not answer.strip():
        answer = "⚠️ No answer found locally or online. Please consult a healthcare professional."

    return answer
