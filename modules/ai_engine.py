import streamlit as st
from modules.rag_engine import retrieve_relevant_chunks
from fpdf import FPDF
from gtts import gTTS
import os

# ------------------------------
# GENERATE CLINICAL ANSWER
# ------------------------------
def generate_clinical_answer(query, top_k=5):
    """
    Retrieve relevant medical information chunks and prepare answer.
    """
    try:
        chunks = retrieve_relevant_chunks(query, top_k)
        answer = "\n\n".join(chunks)
        return answer
    except Exception as e:
        return f"Error retrieving data: {e}"

# ------------------------------
# TEXT TO PDF
# ------------------------------
def text_to_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(filename)
    return filename

# ------------------------------
# TEXT TO SPEECH
# ------------------------------
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename
