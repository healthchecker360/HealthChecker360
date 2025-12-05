import streamlit as st
from ai_engine import generate_clinical_answer, text_to_speech, text_to_pdf
from PIL import Image
import io

# ------------------------------
# Chat & Diagnosis Module
# ------------------------------
def chat_diagnosis_module():
    st.header("💬 Chat & Diagnosis Module")

    # Input selection
    input_type = st.radio("Select Input Type:", ["Text", "Voice", "Image"])

    user_query = None
    uploaded_image = None

    # --- Text input ---
    if input_type == "Text":
        user_query = st.text_area("Enter your query:", height=100)

    # --- Voice input (basic) ---
    elif input_type == "Voice":
        st.info("Voice input: currently only upload a recorded audio file (mp3/wav).")
        audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])
        if audio_file is not None:
            # For now, we can save and convert audio to text later using Whisper / Gemini STT
            st.success("Voice uploaded! (STT not implemented yet)")
            user_query = "Transcribed text from audio here"  # Placeholder

    # --- Image input ---
    elif input_type == "Image":
        uploaded_image = st.file_uploader("Upload image for analysis", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            # Placeholder for image analysis
            user_query = "Analyzing uploaded image..."  # Placeholder

    # Submit button
    if st.button("Get Clinical Answer") and user_query:
        with st.spinner("Fetching concise clinical answer..."):
            answer = generate_clinical_answer(user_query, engine="gemini")

        # Display answer
        st.subheader("✅ Clinical Answer")
        st.text_area("Answer", value=answer, height=250)

        # Optional: Text-to-Speech
        tts_file = text_to_speech(answer)
        st.audio(tts_file, format="audio/mp3")

        # Optional: PDF download
        pdf_file = text_to_pdf(answer)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name="clinical_answer.pdf", mime="application/pdf")
