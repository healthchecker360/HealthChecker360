# app.py
import streamlit as st
from modules.interactions import chat_diagnosis_module
from modules.drug_module import drug_module_ui
from modules.lab import lab_module_ui
from modules.calculators import calculators_ui
from modules.ai_engine import text_to_pdf, text_to_speech
from config import DEBUG

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

    # Call the new diagnosis module
    chat_diagnosis_module()

# ------------------------------
# Drug Info Module
# ------------------------------
elif menu == "Drug Info":
    st.header("💊 Drug Information")
    drug_name = st.text_input("Enter Drug Name:")
    if st.button("Get Drug Info") and drug_name:
        result = drug_module_ui(drug_name)
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


