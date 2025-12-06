import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech

# ==============================
# CHAT DIAGNOSIS MODULE
# ==============================
def chat_diagnosis_module():
    """
    Streamlit-based user interface for querying medical guidelines.
    Accepts user query and returns professional clinical answers.
    """

    st.title("HealthChecker360 - Medical Query Assistant")
    st.write("Enter your medical query below:")

    user_query = st.text_input("Medical Query", placeholder="e.g., fever, headache, diabetes")

    if st.button("Get Clinical Answer") and user_query:
        with st.spinner("Retrieving relevant clinical information..."):
            # Generate clinical answer using AI Engine
            answer = generate_clinical_answer(user_query)
        
        # Display answer
        st.subheader("Clinical Answer")
        st.write(answer)

        # Option: Save as PDF
        if st.button("Save as PDF"):
            pdf_file = text_to_pdf(answer)
            st.success(f"PDF saved: {pdf_file}")
            st.download_button("Download PDF", pdf_file, file_name=pdf_file)

        # Option: Convert to Speech
        if st.button("Convert to Speech"):
            audio_file = text_to_speech(answer)
            st.success(f"Audio saved: {audio_file}")
            st.audio(audio_file, format="audio/mp3")
