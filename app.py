# app.py
import streamlit as st

# ------------------------------
# Module Imports
# ------------------------------
from modules.interactions import chat_diagnosis_module
from modules.drug_module import drug_module_ui
from modules.lab import lab_module_ui
from modules.calculators import (
    calculate_bmi, calculate_bsa, calculate_gfr, calculate_dose, calculate_iv_rate
)

# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(
    page_title="HealthChecker 360",
    page_icon="💊",
    layout="wide"
)

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("HealthChecker 360")
menu_options = ["AI Diagnosis", "Drugs", "Lab Interpretation", "Calculators"]
choice = st.sidebar.selectbox("Select Module", menu_options)

# ------------------------------
# MAIN APP LOGIC
# ------------------------------
if choice == "AI Diagnosis":
    st.header("AI Clinical Diagnosis")
    st.write("Ask your medical question below:")
    chat_diagnosis_module()

elif choice == "Drugs":
    st.header("Drug Information")
    drug_module_ui()

elif choice == "Lab Interpretation":
    st.header("Lab Test Analysis")
    lab_module_ui()

elif choice == "Calculators":
    st.header("Clinical & Pharma Calculators")
    st.write("Select a calculator below:")

    calc_choice = st.selectbox(
        "Choose Calculator",
        ["BMI", "BSA", "GFR", "Dose Adjustment", "IV Rate"]
    )

    if calc_choice == "BMI":
        calculate_bmi()
    elif calc_choice == "BSA":
        calculate_bsa()
    elif calc_choice == "GFR":
        calculate_gfr()
    elif calc_choice == "Dose Adjustment":
        calculate_dose()
    elif calc_choice == "IV Rate":
        calculate_iv_rate()

# ------------------------------
# Footer / Credits
# ------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("HealthChecker 360 © 2025")
