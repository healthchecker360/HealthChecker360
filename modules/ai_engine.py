import pickle
import streamlit as st
from modules.rag_engine import retrieve_relevant_chunks
from pathlib import Path
from fpdf import FPDF
from gtts import gTTS
import requests
import os
from modules.config import GENAI_API_KEY, GROQ_API_KEY, GENAI_API_URL, GROQ_API_URL

# ------------------------------
# GENERATE CLINICAL ANSWER
# ------------------------------
def generate_clinical_answer(query, top_k=5):
    """
    Generate a clinical answer using:
    1. Local RAG search (FAISS + docs)
    2. Fallback to GenAI / Gemini / Groq if no local info
    """
    # Step 1: Try local RAG search
    chunks = retrieve_relevant_chunks(query, top_k)
    if chunks:
        answer = "\n\n".join(chunks)
    else:
        # Step 2: Fallback to external API
        answer = query_genai_api(query)
    
    return answer

# ------------------------------
# QUERY GENAI / GEMINI / GROQ API
# ------------------------------
def query_genai_api(query):
    """
    Query external GenAI / Gemini / Groq APIs to fetch medical info.
    Returns text answer.
    """
    # Example using GENAI
    headers = {"Authorization": f"Bearer {GENAI_API_KEY}"}
    payload = {"query": query, "max_tokens": 500}
    try:
        response = requests.post(GENAI_API_URL, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json().get("answer", "No result found.")
        else:
            # fallback to Groq API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {"query": query, "max_results": 5}
            response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=20)
            if response.status_code == 200:
                return response.json().get("answer", "No result found.")
            else:
                return "No relevant medical information found."
    except Exception as e:
        return f"Error fetching external data: {str(e)}"

# ------------------------------
# TEXT TO PDF
# ------------------------------
def text_to_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 5, line)
    pdf.output(filename)
    return filename

# ------------------------------
# TEXT TO SPEECH
# ------------------------------
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename
