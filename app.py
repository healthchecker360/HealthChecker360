import streamlit as st
from modules.interactions import chat_diagnosis_module
from modules.drug_module import drug_module_ui
from modules.lab import lab_module_ui
from modules.calculators import calculators_ui
from config import DEBUG
from modules.drug_module import drug_module_ui
from config import DRUG_DB_PATH, DEBUG

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="HealthChecker360",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("HealthChecker360")
menu = st.sidebar.radio(
    "Navigate",
    ["Home", "Drug Info", "Lab Interpretation", "Calculators"]
)

# ------------------------------
# Home / Medical Query
# ------------------------------
if menu == "Home":
    st.title("🩺 Medical Query Checker")
    st.write(
        "Enter your symptoms or disease query below. "
        "The app will first search its medical database. "
        "If not found, it will fetch results from online medical resources (Gemini/Groq)."
    )

    user_query = st.text_area("Enter your medical query:", height=120)

    if st.button("Get Diagnosis"):
        if user_query.strip():
            with st.spinner("Generating professional medical answer..."):
                answer = chat_diagnosis_module()  # Remove the argument
            st.success("Answer Generated ✅")
            st.markdown("### Clinical Answer:")
            st.write(answer)

            # Download PDF button
            from modules.ai_engine import text_to_pdf, text_to_speech
            pdf_file = text_to_pdf(answer)
            st.download_button(
                label="📄 Download PDF",
                data=open(pdf_file, "rb").read(),
                file_name="diagnosis.pdf",
                mime="application/pdf"
            )

            # Download Audio button
            audio_file = text_to_speech(answer)
            st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Please enter a query!")

# ------------------------------
# Drug Info Module
# ------------------------------
import streamlit as st

st.header("💊 Drug Information")

# Input field for drug name
drug_name = st.text_input("Enter Drug Name:")

# Button to fetch drug info
if st.button("Get Drug Info") and drug_name:
    result = drug_module_ui(drug_name)  # Pass the input to the function
    st.markdown(result)

# ------------------------------
# Lab Interpretation Module
# ------------------------------
elif menu == "Lab Interpretation":
    st.title("🧪 Lab Interpretation")
    lab_module_ui()

# ------------------------------
# Calculators Module
# ------------------------------
elif menu == "Calculators":
    st.title("📊 Medical & Pharmaceutical Calculators")
    calculators_ui()

# ------------------------------
# Debug Info (Optional)
# ------------------------------
if DEBUG:
    st.sidebar.write("**Debug Mode Enabled**")
