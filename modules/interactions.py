# modules/interactions.py
import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
from modules.rag_engine import retrieve_relevant_chunks
import tempfile
import docx
from PyPDF2 import PdfReader
import speech_recognition as sr
from pathlib import Path

# -----------------------------------------------------------
#               CLINICAL DIAGNOSIS MODULE (FINAL)
# -----------------------------------------------------------
def chat_diagnosis_module():
    # Page title
    st.title("🩺 HealthChecker360 - Clinical Diagnosis Assistant")

    # Dark theme for module
    st.markdown("""
        <style>
        .stApp { background-color: #1e1e2f !important; color: #e0f0ff; }
        h1, h2, h3 { color: #ffffff !important; }
        .stTextInput input, .stTextArea textarea { background-color: #2b2b3c !important; color: #ffffff !important; border: 1px solid #4a90e2; }
        .stButton>button { background-color: #4a90e2; color: #ffffff; border-radius: 6px; padding: 8px 18px; }
        .stButton>button:hover { background-color: #3571a3; }
        div[role="radiogroup"] label { color: #ffffff !important; }
        </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Input Type Selection
    # -----------------------------
    input_type = st.radio(
        "Choose Input Type:",
        ("Text", "Voice", "File Upload"),
        horizontal=True
    )

    user_query = ""

    # =======================================================
    #                     TEXT INPUT
    # =======================================================
    if input_type == "Text":
        user_query = st.text_area("Enter your medical query:", height=140)

    # =======================================================
    #                     VOICE INPUT
    # =======================================================
    elif input_type == "Voice":
        st.info("Upload a short MP3/WAV recording describing your symptoms.")
        audio_file = st.file_uploader("Upload Voice File:", type=["mp3", "wav"])
        if audio_file:
            try:
                recognizer = sr.Recognizer()
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name

                with sr.AudioFile(tmp_path) as source:
                    audio_data = recognizer.record(source)

                user_query = recognizer.recognize_google(audio_data)
                st.success(f"Transcribed Text: {user_query}")
            except Exception:
                st.error("Unable to recognize speech. Please try again.")

    # =======================================================
    #                    FILE UPLOAD INPUT
    # =======================================================
    elif input_type == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload medical document (PDF, TXT, DOCX):",
            type=["pdf", "txt", "docx"]
        )
        if uploaded_file:
            text_content = ""
            # ---- PDF ----
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text_content += page.extract_text() or ""
            # ---- TXT ----
            elif uploaded_file.type == "text/plain":
                text_content = uploaded_file.read().decode("utf-8")
            # ---- DOCX ----
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                text_content = "\n".join([p.text for p in doc.paragraphs])
            user_query = text_content
            st.success("File processed successfully.")

    # =======================================================
    #             GET CLINICAL ANSWER BUTTON
    # =======================================================
    if st.button("Get Clinical Answer") and user_query.strip():
        with st.spinner("Analyzing symptoms and searching medical knowledge..."):
            # Retrieve RAG chunks (local database)
            retrieved_context = retrieve_relevant_chunks(user_query)
            # Generate final answer
            answer = generate_clinical_answer(
                query=user_query
            )

        # ========================
        # Display Answer
        # ========================
        st.subheader("✅ Clinical Answer")
        st.markdown(f"<div style='background-color:#2b2b3c; padding:10px; border-radius:6px;'>{answer.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

        # ========================
        # Optional outputs: PDF / Audio
        # ========================
        col1, col2 = st.columns(2)

        # PDF
        with col1:
            if st.button("Download as PDF"):
                pdf_file = text_to_pdf(answer)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f.read(),
                        file_name="clinical_answer.pdf",
                        mime="application/pdf"
                    )
        # TTS Audio
        with col2:
            if st.button("Play as Voice"):
                tts_file = text_to_speech(answer)
                st.audio(tts_file, format="audio/mp3")
