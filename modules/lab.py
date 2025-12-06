import streamlit as st
import pandas as pd
from config import DEBUG

# ------------------------------
# Sample Lab Reference Data
# ------------------------------
LAB_REF_DATA = {
    "Hemoglobin": {"unit": "g/dL", "normal_male": (13.5, 17.5), "normal_female": (12.0, 15.5)},
    "WBC": {"unit": "10^3/uL", "normal": (4.0, 11.0)},
    "Platelets": {"unit": "10^3/uL", "normal": (150, 450)},
    "Creatinine": {"unit": "mg/dL", "normal": (0.7, 1.3)},
    "BUN": {"unit": "mg/dL", "normal": (7, 20)},
    "ALT": {"unit": "U/L", "normal": (7, 56)},
    "AST": {"unit": "U/L", "normal": (10, 40)},
    "TSH": {"unit": "uIU/mL", "normal": (0.4, 4.0)},
    "Troponin": {"unit": "ng/mL", "normal": (0, 0.04)}
}

# ------------------------------
# Lab Interpretation
# ------------------------------
def interpret_lab(test_name, value, gender=None):
    ref = LAB_REF_DATA.get(test_name)
    if not ref:
        return f"No reference data available for {test_name}."

    low, high = ref.get("normal", (None, None))
    # Gender-specific ranges
    if gender and f"normal_{gender.lower()}" in ref:
        low, high = ref[f"normal_{gender.lower()}"]

    if low is None or high is None:
        return "Reference range not defined."

    if value < low:
        return f"{test_name}: {value} {ref['unit']} (Low) – Possible causes: anemia, blood loss, malnutrition."
    elif value > high:
        return f"{test_name}: {value} {ref['unit']} (High) – Possible causes: infection, dehydration, liver/kidney dysfunction."
    else:
        return f"{test_name}: {value} {ref['unit']} (Normal)."

# ------------------------------
# Streamlit UI
# ------------------------------
def lab_module_ui():
    st.title("HealthChecker360 - Lab Test Interpretation")
    st.markdown(
        "Enter your lab test results to get a quick interpretation and suggestions."
    )

    test_name = st.selectbox("Select Test:", list(LAB_REF_DATA.keys()))
    value = st.number_input("Enter Value:", value=0.0, step=0.1)
    gender = None
    if test_name in ["Hemoglobin"]:
        gender = st.radio("Gender:", ["Male", "Female"])

    if st.button("Interpret"):
        result = interpret_lab(test_name, value, gender)
        st.success(result)

# ------------------------------
# Direct run
# ------------------------------
if __name__ == "__main__":
    lab_module_ui()
