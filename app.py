import streamlit as st
from PIL import Image
import os

# Import our modules
from interactions import chat_diagnosis_module
from drug_module import drug_module_ui
from lab import lab_module_ui
from calculators import calculators_module_ui

# ------------------------------
# App Config
# ------------------------------
st.set_page_config(
    page_title="Health Checker 365",
    page_icon="🩺",
    layout="wide"
)

# Professional color palette
PRIMARY_COLOR = "#0B3954"    # Dark Blue
SECONDARY_COLOR = "#BFD7EA"  # Light Blue
ACCENT_COLOR = "#FF6663"     # Accent Red

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {SECONDARY_COLOR};
            color: {PRIMARY_COLOR};
        }}
        .stButton>button {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        .stSelectbox>div>div {{
            background-color: white;
            color: {PRIMARY_COLOR};
        }}
        .stTextInput>div>input {{
            background-color: white;
            color: {PRIMARY_COLOR};
        }}
        .stTextArea>div>textarea {{
            background-color: white;
            color: {PRIMARY_COLOR};
        }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Logo
# ------------------------------
logo_path = "logo.png"  # Replace with your logo file
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=150)
else:
    st.markdown("<h1 style='color:#0B3954;'>🩺 Health Checker 365</h1>", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("📌 Modules")
module = st.sidebar.radio("Select Module:", 
                          ["💬 Chat & Diagnosis", "💊 Drug Info", "🧪 Lab Interpretation", "🧮 Calculators"])

# Optional: show module description
if module == "💬 Chat & Diagnosis":
    st.sidebar.info("Ask clinical questions, upload images or voice, get targeted diagnosis + treatment suggestions.")
elif module == "💊 Drug Info":
    st.sidebar.info("Get concise drug monographs: Dose, MOA, Warnings, Side effects, Formulations.")
elif module == "🧪 Lab Interpretation":
    st.sidebar.info("Enter lab values or upload lab PDFs for concise interpretation + next steps.")
elif module == "🧮 Calculators":
    st.sidebar.info("Clinical & Pharma calculators with explanation. BMI, BSA, GFR, more.")

st.markdown("##")

# ------------------------------
# Render Module
# ------------------------------
if module == "💬 Chat & Diagnosis":
    chat_diagnosis_module()
elif module == "💊 Drug Info":
    drug_module_ui(st)
elif module == "🧪 Lab Interpretation":
    lab_module_ui()
elif module == "🧮 Calculators":
    calculators_module_ui()

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown("<p style='text-align:center;color:#0B3954;'>© 2025 Health Checker 365 | Your Professional Clinical Assistant 🩺</p>", unsafe_allow_html=True)
