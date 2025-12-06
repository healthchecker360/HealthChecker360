import os
from fpdf import FPDF
from gtts import gTTS
from modules.rag_engine import retrieve_relevant_chunks

# ==============================
# GENERATE CLINICAL ANSWER
# ==============================
def generate_clinical_answer(query, top_k=5):
    """
    Retrieves relevant chunks from the RAG engine and returns
    a concise, professional clinical answer.
    """
    chunks = retrieve_relevant_chunks(query, top_k)
    
    # Combine relevant chunks into a single answer
    answer = "\n\n".join(chunks)
    
    # You can add extra formatting or AI summarization here if desired
    return answer

# ==============================
# TEXT TO PDF
# ==============================
def text_to_pdf(text, output_file="clinical_answer.pdf"):
    """
    Saves the provided text into a PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    
    pdf.output(output_file)
    return output_file

# ==============================
# TEXT TO SPEECH
# ==============================
def text_to_speech(text, output_file="clinical_answer.mp3", lang="en"):
    """
    Converts the provided text to speech and saves as MP3.
    """
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    return output_file
