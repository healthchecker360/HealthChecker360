# modules/interactions.py
import streamlit as st
import tempfile
import docx
from PyPDF2 import PdfReader
import speech_recognition as sr
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
from modules.rag_engine import retrieve_relevant_chunks
from config import DEBUG, TEMP_PATH

# -----------------------------------------------------------
#               CLINICAL DIAGNOSIS MODULE (FINAL)
# -----------------------------------------------------------
def chat_diagnosis_module():
    st.set_page_config(page_title="🩺 HealthChecker360", layout="wide")
    
    # ------------------------------
    # Dark professional theme
    # ------------------------------
    st.markdown(
        """
        <style>
        .stApp { background-color: #1c1c1c !important; color: #e0f0ff !important; }
        h1, h2, h3, h4, h5, h6 { color: #4da6ff !important; }
        .stButton>button { background-color: #0a5dc2 !important; color: white !important; }
        .stButton>button:hover { background-color: #074a99 !important; color: #e9f1ff !important; }
        .stTextInput>div>input, .stTextArea>div>textarea { background-color: #2a2a2a; color: #e0f0ff; border: 1px solid #4da6ff; }
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
    submitted = False

    # =======================================================
    #                     TEXT INPUT
    # =======================================================
    if input_type == "Text":
        user_query = st.text_area("Enter your medical query:", height=140)
        submitted = st.button("Get Clinical Answer")

    # =======================================================
    #                     VOICE INPUT
    # =======================================================
    elif input_type == "Voice":
        st.info("Upload a short MP3/WAV recording describing symptoms.")
        audio_file = st.file_uploader("Upload Voice File:", type=["mp3", "wav"])
        submitted = st.button("Transcribe & Get Clinical Answer")
        if audio_file and submitted:
            try:
                recognizer = sr.Recognizer()
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name
                with sr.AudioFile(tmp_path) as source:
                    audio_data = recognizer.record(source)
                user_query = recognizer.recognize_google(audio_data)
                st.success(f"Transcribed Text: {user_query}")
            except Exception as e:
                st.error(f"Unable to recognize speech: {e}")
                submitted = False

    # =======================================================
    #                    FILE UPLOAD INPUT
    # =======================================================
    elif input_type == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload medical document (PDF, TXT, DOCX):",
            type=["pdf", "txt", "docx"]
        )
        submitted = st.button("Process File & Get Clinical Answer")
        if uploaded_file and submitted:
            try:
                text_content = ""
                if uploaded_file.type == "application/pdf":
                    reader = PdfReader(uploaded_file)
                    for page in reader.pages:
                        text_content += page.extract_text() or ""
                elif uploaded_file.type == "text/plain":
                    text_content = uploaded_file.read().decode("utf-8")
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = docx.Document(uploaded_file)
                    text_content = "\n".join([p.text for p in doc.paragraphs])
                user_query = text_content
                st.success("File processed successfully.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                submitted = False

    # =======================================================
    #           Generate Clinical Answer
    # =======================================================
    if submitted and user_query.strip():
        with st.spinner("Analyzing symptoms and retrieving medical knowledge..."):
            try:
                answer = generate_clinical_answer(user_query)
            except Exception as e:
                answer = "⚠️ Failed to generate answer. Please check your configuration."
                if DEBUG:
                    st.error(f"[DEBUG] {e}")

        # Display Result
        st.subheader("✅ Clinical Answer")
        st.markdown(answer.replace("\n", "  \n- "), unsafe_allow_html=True)

        # Optional Outputs
        col1, col2 = st.columns(2)

        # PDF
        with col1:
            if st.button("Download as PDF"):
                try:
                    pdf_file = text_to_pdf(answer)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f.read(),
                            file_name="clinical_answer.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")

        # TTS Audio
        with col2:
            if st.button("Play as Voice"):
                try:
                    tts_file = text_to_speech(answer)
                    st.audio(tts_file, format="audio/mp3")
                except Exception as e:
                    st.error(f"Failed to generate audio: {e}")
