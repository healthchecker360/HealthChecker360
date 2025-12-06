# modules/interactions.py
import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
from modules.rag_engine import retrieve_relevant_chunks
import tempfile
import os
import docx
from PyPDF2 import PdfReader
import speech_recognition as sr

# -----------------------------
# Clinical Diagnosis Module
# -----------------------------
def chat_diagnosis_module():
    st.set_page_config(page_title="🩺 HealthChecker360", layout="wide")
    st.title("🩺 HealthChecker360 - Clinical Diagnosis Assistant")

    # -----------------------------
    # Input options
    # -----------------------------
    input_type = st.radio(
        "Choose input type:",
        ("Text", "Voice", "File Upload")
    )

    user_query = ""

    # ----- Text Input -----
    if input_type == "Text":
        user_query = st.text_area("Enter your medical query here:")

    # ----- Voice Input -----
    elif input_type == "Voice":
        st.info("Please record your voice in English describing your symptoms.")
        audio_file = st.file_uploader("Upload voice file (MP3/WAV):", type=["mp3", "wav"])
        if audio_file:
            r = sr.Recognizer()
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            with sr.AudioFile(tmp_path) as source:
                audio = r.record(source)
                try:
                    user_query = r.recognize_google(audio)
                    st.success(f"Transcribed Text: {user_query}")
                except:
                    st.error("Could not recognize speech. Try again.")

    # ----- File Upload -----
    elif input_type == "File Upload":
        uploaded_file = st.file_uploader("Upload medical file:", type=["pdf", "txt", "docx"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                user_query = text
            elif uploaded_file.type == "text/plain":
                user_query = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                user_query = "\n".join([p.text for p in doc.paragraphs])
            st.success("File content loaded as query.")

    # -----------------------------
    # Process query
    # -----------------------------
    if st.button("Get Clinical Answer") and user_query:
        with st.spinner("Analyzing symptoms and searching for relevant clinical info..."):
            # First search in local docs & FAISS
            chunks = retrieve_relevant_chunks(user_query)
            if chunks:
                # Local + FAISS answer
                answer = generate_clinical_answer(user_query)
            else:
                # Online fallback (Gemini + Groq)
                answer = generate_clinical_answer(user_query)

        # -----------------------------
        # Display result professionally
        # -----------------------------
        st.subheader("✅ Clinical Answer")
        st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)

        # -----------------------------
        # Optional outputs
        # -----------------------------
        col1, col2 = st.columns(2)

        # PDF Download
        with col1:
            if st.button("Download as PDF"):
                pdf_file = text_to_pdf(answer)
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="clinical_answer.pdf",
                    mime="application/pdf"
                )

        # Audio Playback
        with col2:
            if st.button("Play as Voice"):
                tts_audio = text_to_speech(answer)
                st.audio(tts_audio, format="audio/mp3")
