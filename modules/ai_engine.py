import os
from fpdf import FPDF
from gtts import gTTS
from config import TEMP_PATH, DEBUG
from modules.rag_engine import retrieve_relevant_chunks, fallback_online_search

# ------------------------------
# Generate clinical answer
# ------------------------------
def generate_clinical_answer(query, top_k=None):
    """
    Generates answer from local FAISS documents or fallback online.
    """
    if top_k is None:
        from config import TOP_K
        top_k = TOP_K
    
    # Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(query, top_k=top_k)
    
    if chunks:
        # Concatenate chunks for answer
        answer = "\n\n".join(chunks)
        if DEBUG:
            print(f"Answer from local docs for query '{query}':")
            print(answer[:500], "...")
        return answer
    else:
        # Fallback to online search if nothing found
        if DEBUG:
            print(f"No local docs found. Using online fallback for query '{query}'")
        return fallback_online_search(query)

# ------------------------------
# Convert text to PDF
# ------------------------------
def text_to_pdf(text, filename="output.pdf"):
    pdf_path = TEMP_PATH / filename
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 5, line)
    pdf.output(str(pdf_path))
    return pdf_path

# ------------------------------
# Convert text to speech
# ------------------------------
def text_to_speech(text, filename="output.mp3", lang="en"):
    audio_path = TEMP_PATH / filename
    tts = gTTS(text=text, lang=lang)
    tts.save(str(audio_path))
    return audio_path

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    query = "fever"
    answer = generate_clinical_answer(query)
    print(answer)
    pdf_file = text_to_pdf(answer)
    print(f"PDF saved at: {pdf_file}")
    audio_file = text_to_speech(answer)
    print(f"Audio saved at: {audio_file}")
