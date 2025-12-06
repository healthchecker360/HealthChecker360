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
#               CLINICAL DIAGNOSIS MODULE
# -----------------------------------------------------------
def chat_diagnosis_module():
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
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                text_content = "\n".join([p.text for p in doc.paragraphs])

            user_query = text_content
            st.success("File processed successfully.")

    # -----------------------------
    # Submit Query Button
    # -----------------------------
    submit_query = st.button("Get Clinical Answer")

    if submit_query and user_query.strip():
        with st.spinner("Analyzing symptoms and generating professional medical answer..."):

            # Retrieve local FAISS chunks
            retrieved_context = retrieve_relevant_chunks(user_query)

            # Generate final answer using RAG + LLM fallback
            answer = generate_clinical_answer(
                user_query=user_query,
                retrieved_context=retrieved_context
            )

        # -----------------------------
        # Display Answer
        # -----------------------------
        st.subheader("✅ Clinical Answer")
        st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)

        # -----------------------------
        # Optional Outputs: PDF / Audio
        # -----------------------------
        col1, col2 = st.columns(2)

        # PDF Download
        with col1:
            pdf_file = text_to_pdf(answer)
            st.download_button(
                label="📄 Download PDF",
                data=open(pdf_file, "rb").read(),
                file_name="clinical_answer.pdf",
                mime="application/pdf"
            )

        # TTS Audio
        with col2:
            tts_file = text_to_speech(answer)
            st.audio(tts_file, format="audio/mp3")
