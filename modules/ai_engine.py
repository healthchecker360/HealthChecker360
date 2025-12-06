import os
from typing import List
from fpdf import FPDF
from gtts import gTTS
from .rag_engine import retrieve_relevant_chunks
from rag_engine import retrieve_relevant_chunks

# ---------------------------
# Clinical Answer Generation
# ---------------------------
def generate_clinical_answer(query: str, engine: str = DEFAULT_ENGINE, top_k: int = TOP_K) -> str:
    """
    Generate a clinical answer for a medical query.
    Steps:
    1. Retrieve top K relevant chunks from RAG.
    2. Feed chunks + query to AI engine (Gemini/OpenAI).
    3. Return concise answer.
    """
    try:
        # Retrieve relevant chunks
        chunks = retrieve_relevant_chunks(query, top_k=top_k)
        context = "\n".join(chunks)

        # Here you can integrate Gemini/OpenAI API call
        # For example, pseudo-call:
        answer = f"Clinical Answer (simulated):\nContext:\n{context}\nQuery: {query}"
        # Replace above line with actual API call
        return answer

    except Exception as e:
        return f"Error generating answer: {e}"


# ---------------------------
# Text to PDF
# ---------------------------
def text_to_pdf(text: str, output_file: str = "output.pdf"):
    """
    Convert a text string into a PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    
    pdf.output(output_file)
    return output_file


# ---------------------------
# Text to Speech
# ---------------------------
def text_to_speech(text: str, output_file: str = "output.mp3", lang: str = "en"):
    """
    Convert text to speech and save as mp3 file.
    """
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    return output_file
