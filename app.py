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
# Professional Medical UI Styling
# ------------------------------
st.markdown(
    """
    <style>
        /* Main Background */
        .stApp {
            background-color: #ffffff !important;
        }

        /* Titles */
        h1, h2, h3, h4 {
            color: #043672 !important;     /* Medical navy blue */
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f0f4fa !important;  /* Light clinical blue */
        }

        /* Buttons */
        .stButton>button {
            background-color: #0a5dc2 !important;
            color: white !important;
            border-radius: 6px;
            padding: 8px 18px;
            font-size: 15px;
            border: none;
        }

        .stButton>button:hover {
            background-color: #074a99 !important;
            color: #e9f1ff !important;
        }

        /* Inputs */
        .stTextInput input, textarea, .stTextArea textarea {
            border: 1px solid #aac6e8 !important;
        }

        /* Radio Buttons */
        div[role="radiogroup"] label {
            color: #043672 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
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
# Home — Diagnosis Module
# ------------------------------
if menu == "Home":
    st.title("🩺 Medical Query Checker")

    st.write(
        """
        Quickly analyze symptoms, diseases, and clinical queries.
        
        The system uses:
        - Local medical database (FAISS + embeddings)
        - Online medical LLMs (Gemini / Groq)
        
        **Enter your symptoms or condition below.**
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
        st.markdown(result, unsafe_allow_html=True)

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
