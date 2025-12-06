import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech

# ------------------------------
# CHAT DIAGNOSIS MODULE
# ------------------------------
def chat_diagnosis_module():
    st.title("HealthChecker360 - Symptom Checker / Diagnosis")
    st.write("Enter your symptoms or medical query to get relevant information.")

    user_query = st.text_area("Enter your medical query:")

    if st.button("Get Answer"):
        if not user_query.strip():
            st.warning("Please enter a query first!")
            return

        # Generate clinical answer using RAG
        with st.spinner("Fetching relevant medical information..."):
            answer = generate_clinical_answer(user_query)
        
        st.subheader("Clinical Answer")
        st.write(answer)

        # ------------------------------
        # PDF Download
        # ------------------------------
        if st.button("Download as PDF"):
            pdf_file = text_to_pdf(answer, filename="clinical_answer.pdf")
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name="clinical_answer.pdf",
                    mime="application/pdf"
                )

        # ------------------------------
        # Audio Download
        # ------------------------------
        if st.button("Listen to Answer"):
            audio_file = text_to_speech(answer, filename="clinical_answer.mp3")
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
