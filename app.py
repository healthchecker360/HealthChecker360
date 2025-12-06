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
# Dark Theme & Professional Styling
# ------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117 !important;
            color: #ffffff !important;
        }
        h1, h2, h3, h4 {
            color: #00aaff !important;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 1px solid #00aaff !important;
        }
        .stButton>button {
            background-color: #00aaff !important;
            color: #000000 !important;
            border-radius: 6px;
            padding: 6px 18px;
            font-size: 15px;
        }
        .stButton>button:hover {
            background-color: #0077aa !important;
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
            color: #ffffff !important;
        }
        div[role="radiogroup"] label {
            color: #00aaff !important;
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
# Home — Diagnostic / Clinical Query
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
    # Call the diagnostic module
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
