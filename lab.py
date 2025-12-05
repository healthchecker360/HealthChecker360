import streamlit as st
from ai_engine import generate_clinical_answer, text_to_speech, text_to_pdf
from rag_engine import retrieve_relevant_chunks
import os
from PyPDF2 import PdfReader

# ------------------------------
# Optional: Extract text from PDF
# ------------------------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

# ------------------------------
# Lab Interpretation
# ------------------------------
def interpret_lab_values(lab_input, top_k=5):
    """
    Takes lab values (text or PDF), retrieves relevant clinical context,
    and returns concise interpretation + next steps.
    """
    # If PDF is uploaded, extract text
    if hasattr(lab_input, "read"):  # Streamlit uploaded file
        lab_text = extract_text_from_pdf(lab_input)
    else:
        lab_text = lab_input

    # Retrieve relevant chunks from PDFs/guidelines
    context_chunks = retrieve_relevant_chunks(lab_text, top_k=top_k)
    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a professional clinical assistant. Interpret the following lab results concisely:
- Provide interpretation and next steps.
- Do not add extra information.

Lab results:
{lab_text}

Context from guidelines:
{context_text}
"""

    answer = generate_clinical_answer(prompt, engine="gemini")
    return answer.strip()

# ------------------------------
# Streamlit Lab Module
# ------------------------------
def lab_module_ui():
    st.header("🧪 Lab Interpretation Module")

    lab_input_type = st.radio("Input type:", ["Text", "PDF"])

    lab_input = None

    if lab_input_type == "Text":
        lab_input = st.text_area("Enter lab values:", height=100)
    elif lab_input_type == "PDF":
        uploaded_file = st.file_uploader("Upload Lab PDF", type=["pdf"])
        if uploaded_file is not None:
            lab_input = uploaded_file

    if st.button("Interpret Lab Results") and lab_input:
        with st.spinner("Generating concise lab interpretation..."):
            interpretation = interpret_lab_values(lab_input)

        st.subheader("✅ Lab Interpretation")
        st.text_area("Interpretation + Next Steps", value=interpretation, height=250)

        # Optional TTS
        tts_file = text_to_speech(interpretation)
        st.audio(tts_file, format="audio/mp3")

        # Optional PDF
        pdf_file = text_to_pdf(interpretation)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name="lab_interpretation.pdf", mime="application/pdf")

# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    import streamlit as st
    lab_module_ui()
