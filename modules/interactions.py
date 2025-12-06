import streamlit as st
from modules.ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
from config import TEMP_PATH, DEBUG

# ------------------------------
# Chat / Diagnosis module
# ------------------------------
def chat_diagnosis_module():
    st.title("HealthChecker360 - Medical Query Assistant")
    st.markdown(
        "Enter your medical query below. The app will provide evidence-based answers "
        "from your uploaded medical documents or fallback to online resources if needed."
    )

    user_query = st.text_input("Enter your medical query:")

    if st.button("Get Answer") and user_query.strip():
        with st.spinner("Generating answer..."):
            answer = generate_clinical_answer(user_query)
        
        # Display answer
        st.subheader("Answer:")
        st.write(answer)

        # Option to download PDF
        if st.button("Download as PDF"):
            pdf_file = text_to_pdf(answer, filename=f"{user_query[:20]}.pdf")
            st.success(f"PDF saved at: {pdf_file}")
            st.download_button(
                label="Download PDF",
                data=open(pdf_file, "rb").read(),
                file_name=f"{user_query[:20]}.pdf",
                mime="application/pdf"
            )

        # Option to listen as audio
        if st.button("Listen Answer"):
            audio_file = text_to_speech(answer, filename=f"{user_query[:20]}.mp3")
            st.success(f"Audio generated at: {audio_file}")
            st.audio(audio_file)

# ------------------------------
# For direct run
# ------------------------------
if __name__ == "__main__":
    chat_diagnosis_module()
