from .rag_engine import retrieve_relevant_chunks
from fpdf import FPDF
from gtts import gTTS

def generate_clinical_answer(query, top_k=5):
    chunks = retrieve_relevant_chunks(query, top_k)
    answer = " ".join(chunks)
    return answer

def text_to_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
