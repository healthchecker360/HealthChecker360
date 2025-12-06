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
# Professional & Clear Clinical UI Styling
# ------------------------------
st.markdown(
    """
    <style>
        /* App Background */
        .stApp {
            background-color: #f7f9fc !important; /* very light grey-blue */
        }

        /* Main Title Colors */
        h1, h2, h3 {
            color: #0B3D91 !important; /* deep medical blue */
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #d3d7dd !important;
        }

        /* Sidebar labels */
        section[data-testid="stSidebar"] * {
            color: #0B3D91 !important;
            font-weight: 600;
        }

        /* Text Inputs */
        .stTextInput input,
        .stTextArea textarea {
            background-color: #ffffff !important;
            color: #1f1f1f !important;
            border: 1px solid #b8c4ce !important;
            border-radius: 6px !important;
        }

        /* Radio Buttons */
        div[role="radiogroup"] label {
            color: #0B3D91 !important;
            font-weight: 600;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0B3D91 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 10px 20px;
            border: none;
            font-size: 16px;
            font-weight: 600;
        }

        .stButton>button:hover {
            background-color: #082c6c !important;
        }

        /* Markdown / normal text */
        .stMarkdown p {
            color: #2a2a2a !important;
            font-size: 16px !important;
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
        Enter symptoms or medical questions below.
        The system uses a local medical database (FAISS) and online LLMs for accurate answers.
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
# Debug Mode Indicator
# ------------------------------
if DEBUG:
    st.sidebar.write("**Debug Mode Enabled**")
