from .ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech
import streamlit as st

def chat_diagnosis_module():
    user_query = st.text_input("Enter your medical query:")
    if user_query:
        answer = generate_clinical_answer(user_query)
        st.write(answer)
