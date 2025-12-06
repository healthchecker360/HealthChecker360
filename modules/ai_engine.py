import os
from modules.rag_engine import retrieve_relevant_chunks
from config import GOOGLE_API_KEY, GROQ_API_KEY, TEMP_PATH, DEBUG
from fpdf import FPDF
from gtts import gTTS

# ------------------------------
# Generate Clinical Answer
# ------------------------------
def generate_clinical_answer(query, top_k=3):
    """
    1. Try to get answer from local docs (RAG)
    2. If no results, fallback to Gemini/Groq API
    """
    chunks = retrieve_relevant_chunks(query, top_k=top_k)

    # If RAG returns placeholder, fallback to online AI
    if len(chunks) == 1 and "[No local docs found]" in chunks[0]:
        if DEBUG:
            print("[AI_ENGINE] No local docs found, querying Gemini/Groq API...")

        # Placeholder: call Gemini or Groq API here
        online_answer = query_online_medical_api(query)
        return online_answer

    # Otherwise, summarize or compile retrieved chunks
    answer = "\n\n".join(chunks)
    return answer

# ------------------------------
# Online Medical API Placeholder
# ------------------------------
def query_online_medical_api(query):
    """
    Here you can integrate:
    - Gemini API (Google)
    - Groq API
    - Medscape / UpToDate (if API available)
    """
    # Example placeholder
    result = f"[Online search simulated] Answer for: {query}"
    return result

# ------------------------------
# Text-to-PDF
# ------------------------------
def text_to_pdf(text, filename="output.pdf"):
    path = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(str(path))
    return str(path)

# ------------------------------
# Text-to-Speech
# ------------------------------
def text_to_speech(text, filename="output.mp3"):
    path = TEMP_PATH / filename
    tts = gTTS(text=text, lang='en')
    tts.save(str(path))
    return str(path)
