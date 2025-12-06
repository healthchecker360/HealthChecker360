import os
import pickle
from pathlib import Path
from gtts import gTTS
from fpdf import FPDF
from config import VECTOR_PATH, TEMP_PATH, TOP_K, DEBUG, GOOGLE_API_KEY, GROQ_API_KEY
from modules.rag_engine import retrieve_relevant_chunks

# ------------------------------
# Helper: Generate PDF from text
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
# Helper: Generate speech from text
# ------------------------------
def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    audio_file = TEMP_PATH / filename
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_file))
    return str(audio_file)

# ------------------------------
# Helper: Call online AI (Gemini/Groq)
# ------------------------------
def call_gemini_or_groq_api(query: str) -> str:
    """
    Placeholder function to call Gemini/Groq API.
    Replace with actual API integration.
    """
    # Example pseudo-code:
    # response = gemini_client.ask(query)
    # return response.text
    return f"[Online AI Answer Placeholder for query: {query}]"

# ------------------------------
# Main function: generate clinical answer
# ------------------------------
def generate_clinical_answer(query: str, top_k: int = TOP_K) -> str:
    """
    Returns a professional medical answer.
    1. Tries local FAISS vector store first.
    2. Falls back to Gemini/Groq online AI if local search fails.
    """
    answer = ""

    # Step 1: Try local FAISS
    try:
        faiss_index_file = VECTOR_PATH / "faiss_index.bin"
        chunks_file = VECTOR_PATH / "chunks.pkl"
        if faiss_index_file.exists() and chunks_file.exists():
            retrieved_chunks = retrieve_relevant_chunks(query, top_k=top_k)
            if retrieved_chunks:
                answer = "\n\n".join(retrieved_chunks)
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] FAISS retrieval skipped: {e}")

    # Step 2: Online AI fallback
    if not answer.strip():
        try:
            answer = call_gemini_or_groq_api(query)
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Online AI fallback failed: {e}")
            answer = "No answer found locally or online. Please consult a healthcare professional."

    return answer
