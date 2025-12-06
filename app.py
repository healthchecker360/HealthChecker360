# app.py
import streamlit as st
from modules.interactions import chat_diagnosis_module
from modules.drug_module import drug_module_ui
from modules.lab import lab_module_ui
from modules.calculators import calculators_ui
from config import DEBUG

# ------------------------------
# Global Page Configuration
# ------------------------------
st.set_page_config(
    page_title="HealthChecker360",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Professional UI Styling
# ------------------------------
st.markdown(
    """
    <style>
        /* Main Background */
        .stApp {
            background-color: #f5f7fa;
        }

        /* Titles */
        h1, h2, h3, .stMarkdown {
            color: #0b2e59 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #e8eef5;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0b2e59;
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-size: 1rem;
        }
        
        .stButton>button:hover {
            background-color: #154a85;
        }

        /* Radio button color */
        div[role="radiogroup"] > label {
            color: #0b2e59 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("🩺 HealthChecker360")
menu = st.sidebar.radio(
    "Navigate",
    ["Home", "Drug Info", "Lab Interpretation", "Calculators"]
)

# ------------------------------
# Home — Diagnosis Module
# ------------------------------
if menu == "Home":
    st.title("🩺 Medical Query Checker")

    st.write(
        """
        Quickly analyze medical symptoms, diseases, and clinical queries.
        The system uses:
        - Local medical database (FAISS + embeddings)
        - Online medical LLMs (Gemini / Groq)
        
        **Choose your input type and begin.**
        """
    )

    chat_diagnosis_module()

# ------------------------------
# Drug Information Module
# ------------------------------
elif menu == "Drug Info":
    st.header("💊 Drug Information")

    drug_name = st.text_input("Enter Drug Name:")

    if st.button("Get Drug Info") and drug_name.strip():
        result = drug_module_ui(drug_name)
        st.markdown(result)

# ------------------------------
# Lab Interpretation Module
# ------------------------------
elif menu == "Lab Interpretation":
    st.title("🧪 Lab Interpretation")
    lab_module_ui()

# ------------------------------
# Medical Calculators Module
# ------------------------------
elif menu == "Calculators":
    st.title("📊 Medical & Pharmaceutical Calculators")
    calculators_ui()

# ------------------------------
# Debug Info
# ------------------------------
if DEBUG:
    st.sidebar.write("**Debug Mode Enabled**")
