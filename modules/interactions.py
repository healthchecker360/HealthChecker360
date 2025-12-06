import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_speech, text_to_pdf
from modules.rag_engine import retrieve_relevant_chunks
from PIL import Image
import io

# ------------------------------
# Diagnosis Module
# ------------------------------
def chat_diagnosis_module():
    user_query = st.text_input("Enter your medical query:")
    if st.button("Get Clinical Answer") and user_query:
        # Process query...

    # Text input
    user_query = st.text_input("Enter your medical query:")

    # Image input
    uploaded_file = st.file_uploader("Or upload an image (symptom, rash, scan):", type=["jpg","png","jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        # Convert image to bytes for AI processing
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        user_query += " [Image attached]"  # Mark input for AI

    # Voice input
    audio_file = st.file_uploader("Or record voice query (mp3/wav):", type=["wav","mp3"])
    if audio_file:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                voice_text = recognizer.recognize_google(audio_data)
                st.write(f"Voice recognized: {voice_text}")
                user_query += f" {voice_text}"
            except Exception as e:
                st.warning(f"Could not recognize audio: {e}")

    if st.button("Get Clinical Answer") and user_query:
        # Step 1: Try local FAISS documents
        chunks = retrieve_relevant_chunks(user_query)
        if chunks:
            answer = generate_clinical_answer(user_query, chunks=chunks)
        else:
            # Step 2: Fallback to AI online if no chunks
            answer = generate_clinical_answer(user_query, online_fallback=True)

        # Step 3: Display results
        st.subheader("Clinical Answer:")
        st.markdown(answer)

        # Optional: Generate PDF or audio
        if st.button("Generate PDF"):
            pdf_path = text_to_pdf(user_query, answer)
            st.success(f"PDF saved: {pdf_path}")

        if st.button("Listen Answer"):
            audio_path = text_to_speech(answer)
            st.audio(audio_path)
