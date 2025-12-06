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
    
    # -----------------------------
    # Custom Dark Theme Styling
    # -----------------------------
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #0d1117 !important;
                color: #ffffff !important;
            }
            h1, h2, h3, h4 {
                color: #00aaff !important;
            }
            .stTextInput>div>input, .stTextArea>div>textarea {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #00aaff !important;
            }
            .stButton>button {
                background-color: #00aaff !important;
                color: #000000 !important;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 15px;
            }
            .stButton>button:hover {
                background-color: #0077aa !important;
                color: #ffffff !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #111827 !important;
                color: #ffffff !important;
            }
            div[role="radiogroup"] label {
                color: #00aaff !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🩺 HealthChecker360 - Clinical Diagnosis Assistant")

    # -----------------------------
    # Input Type Selection
    # -----------------------------
    input_type = st.radio(
        "Choose Input Type:",
        ("Text", "Voice", "File Upload")
    )

    user_query = ""

    # ==========================
    # TEXT INPUT
    # ==========================
    if input_type == "Text":
        user_query = st.text_area("Enter your medical query:", height=140)
        if st.button("Analyze Symptoms"):
            if user_query.strip():
                with st.spinner("Analyzing symptoms and retrieving relevant info..."):
                    # Retrieve chunks from FAISS
                    retrieved_context = retrieve_relevant_chunks(user_query)
                    # Generate answer
                    answer = generate_clinical_answer(
                        query=user_query,
                        retrieved_context=retrieved_context
                    )
                # Display answer
                st.subheader("✅ Clinical Answer")
                st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)

                # Optional Outputs
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
            else:
                st.warning("Please enter a query before clicking Analyze.")

    # ==========================
    # VOICE INPUT
    # ==========================
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

                if st.button("Analyze Voice Input"):
                    with st.spinner("Analyzing voice query..."):
                        retrieved_context = retrieve_relevant_chunks(user_query)
                        answer = generate_clinical_answer(
                            query=user_query,
                            retrieved_context=retrieved_context
                        )
                    st.subheader("✅ Clinical Answer")
                    st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
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
                    with col2:
                        if st.button("Play as Voice"):
                            tts_file = text_to_speech(answer)
                            st.audio(tts_file, format="audio/mp3")
            except Exception:
                st.error("Unable to process voice file. Please try again.")

    # ==========================
    # FILE UPLOAD INPUT
    # ==========================
    elif input_type == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload medical document (PDF, TXT, DOCX):",
            type=["pdf", "txt", "docx"]
        )

        if uploaded_file:
            text_content = ""
            # PDF
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text_content += page.extract_text() or ""
            # TXT
            elif uploaded_file.type == "text/plain":
                text_content = uploaded_file.read().decode("utf-8")
            # DOCX
            elif uploaded_file.type == \
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(uploaded_file)
                text_content = "\n".join([p.text for p in doc.paragraphs])

            user_query = text_content
            st.success("File processed successfully.")

            if st.button("Analyze File Input") and user_query.strip():
                with st.spinner("Analyzing uploaded file..."):
                    retrieved_context = retrieve_relevant_chunks(user_query)
                    answer = generate_clinical_answer(
                        query=user_query,
                        retrieved_context=retrieved_context
                    )
                st.subheader("✅ Clinical Answer")
                st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)

                col1, col2 = st.columns(2)
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
                with col2:
                    if st.button("Play as Voice"):
                        tts_file = text_to_speech(answer)
                        st.audio(tts_file, format="audio/mp3")
