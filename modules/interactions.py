# modules/interactions.py
import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
from modules.rag_engine import retrieve_relevant_chunks
import tempfile
import os
import docx
from PyPDF2 import PdfReader
import speech_recognition as sr

# -----------------------------------------------------------
#               CLINICAL DIAGNOSIS MODULE (FINAL)
# -----------------------------------------------------------
def chat_diagnosis_module():
    st.set_page_config(page_title="🩺 HealthChecker360", layout="wide")
    st.title("🩺 HealthChecker360 - Clinical Diagnosis Assistant")

    # -----------------------------
    # Input Type Selection
    # -----------------------------
    input_type = st.radio(
        "Choose Input Type:",
        ("Text", "Voice", "File Upload")
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
        st.info("Upload a short MP3/WAV recording describing symptoms.")
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
            elif uploaded_file.type == \
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                text_content = "\n".join([p.text for p in doc.paragraphs])

            user_query = text_content
            st.success("File processed successfully.")

    # =======================================================
    #                  PROCESS THE QUERY
    # =======================================================
    if st.button("Get Clinical Answer") and user_query.strip():
        with st.spinner("Analyzing clinically..."):

            # Step 1 — Get chunks from vector store
            try:
                chunks = retrieve_relevant_chunks(user_query)
            except:
                chunks = []

            # Step 2 — Always pass context into AI model
            retrieved_context = "\n".join(chunks) if chunks else ""

            # Step 3 — Generate final clinical-grade response
            answer = generate_clinical_answer(
                user_query=user_query,
                retrieved_context=retrieved_context
            )

        # =======================================================
        #                  DISPLAY THE ANSWER
        # =======================================================
        st.subheader("✅ Clinical Answer")
        st.markdown(
            answer.replace("\n", "  \n- "),
            unsafe_allow_html=True
        )

        # =======================================================
        #                DOWNLOAD & AUDIO OPTIONS
        # =======================================================
        col1, col2 = st.columns(2)

        # -------- PDF --------
        with col1:
            if st.button("Download as PDF"):
                pdf_path = text_to_pdf(answer)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f.read(),
                        file_name="clinical_answer.pdf",
                        mime="application/pdf"
                    )

        # -------- AUDIO --------
        with col2:
            if st.button("Play as Voice"):
                audio_path = text_to_speech(answer)
                st.audio(audio_path, format="audio/mp3")
