# app.py
import streamlit as st
from modules.interactions import chat_diagnosis_module
from modules.drug_module import drug_module_ui
from modules.lab import lab_module_ui
from modules.calculators import calculators_ui
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
# Dark Mode Professional Styling
# ------------------------------
st.markdown(
    """
    <style>
        /* App Background */
        .stApp {
            background-color: #1e1e2f !important;  /* dark charcoal */
            color: #ffffff;
        }

        /* Titles */
        h1, h2, h3 {
            color: #4fc3f7 !important;  /* bright cyan-blue */
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #2b2b3f !important;
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
            font-weight: 600;
        }

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea {
            background-color: #2b2b3f !important;
            color: #ffffff !important;
            border: 1px solid #4fc3f7 !important;
            border-radius: 8px !important;
        }

        /* Radio Buttons */
        div[role="radiogroup"] label {
            color: #4fc3f7 !important;
            font-weight: 600;
        }

        /* Buttons */
        .stButton>button {
            background-color: #4fc3f7 !important;
            color: #1e1e2f !important;
            border-radius: 6px !important;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1da1f2 !important;
            color: #ffffff !important;
        }

        /* Markdown / normal text */
        .stMarkdown p, .stText {
            color: #d0d0d0 !important;
            font-size: 16px !important;
        }

        /* Info boxes */
        .stInfo {
            background-color: #2b2b3f !important;
            color: #4fc3f7 !important;
            border-left: 5px solid #4fc3f7;
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
        Enter your symptoms or medical questions below.
        The system uses a local medical database (FAISS) and online LLMs for accurate answers.
        """
    )

    # Call the interactive clinical diagnosis module
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
