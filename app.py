import streamlit as st
from interactions import chat_diagnosis_module
from drug_module import drug_module_ui
from calculators import (
    calculate_bmi, calculate_bsa, calculate_gfr,
    calculate_dose, calculate_iv_rate
)
from lab import lab_module_ui

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="HealthChecker 360",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💊 HealthChecker 360")
st.markdown("Your AI Medical Assistant: Clinical, Pharma, and Lab Support")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
menu_options = [
    "Home",
    "Symptom Checker (AI Diagnosis)",
    "Drug Information",
    "Calculators",
    "Lab Interpretation"
]
choice = st.sidebar.radio("Go to", menu_options)

# -----------------------------
# HOME PAGE
# -----------------------------
if choice == "Home":
    st.subheader("Welcome to HealthChecker 360")
    st.write("""
    - AI-assisted diagnosis & clinical guidance  
    - Drug information & safety checks  
    - Clinical & pharmaceutical calculators  
    - Lab interpretation & recommendations  
    """)

# -----------------------------
# SYMPTOM CHECKER / AI DIAGNOSIS
# -----------------------------
elif choice == "Symptom Checker (AI Diagnosis)":
    st.subheader("Symptom Checker & AI Clinical Diagnosis")
    chat_diagnosis_module()  # RAG + AI engine handles queries

# -----------------------------
# DRUG INFORMATION MODULE
# -----------------------------
elif choice == "Drug Information":
    drug_module_ui()  # Streamlit-ready drug lookup UI

# -----------------------------
# CALCULATORS MODULE
# -----------------------------
elif choice == "Calculators":
    st.subheader("Clinical & Pharmaceutical Calculators")

    # BMI & BSA
    st.markdown("### BMI & BSA Calculator")
    weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=0.0, value=175.0)
    st.write("BMI:", calculate_bmi(weight, height))
    st.write("BSA:", calculate_bsa(weight, height))

    # GFR & Dose Adjustment
    st.markdown("### GFR & Dose Adjustment")
    age = st.number_input("Age (years)", min_value=0, value=50)
    serum_creatinine = st.number_input("Serum Creatinine (mg/dl)", min_value=0.0, value=1.0)
    gender = st.selectbox("Gender", ["Male", "Female"])
    gfr = calculate_gfr(age, weight, serum_creatinine, gender)
    st.write("Estimated GFR:", gfr)
    base_dose = st.number_input("Base Dose (mg)", min_value=0.0, value=500.0)
    adjusted_dose = calculate_dose(base_dose, gfr)
    st.write("Adjusted Dose:", adjusted_dose)

    # IV Drip Rate
    st.markdown("### IV Drip Rate Calculator")
    volume = st.number_input("IV Volume (ml)", min_value=0.0, value=500.0)
    time = st.number_input("Time (hours)", min_value=0.1, value=4.0)
    st.write("IV Rate (ml/hr):", calculate_iv_rate(volume, time))

# -----------------------------
# LAB INTERPRETATION
# -----------------------------
elif choice == "Lab Interpretation":
    lab_module_ui()  # Streamlit-ready lab module UI

# -----------------------------
# Footer / Info
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("HealthChecker 360 | AI Medical Assistant | v1.0")
st.sidebar.markdown("Developed for: Doctors, Pharmacists, Students, Patients")
