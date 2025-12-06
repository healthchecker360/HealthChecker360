import streamlit as st

# ==============================
# SAMPLE LAB REFERENCE RANGES
# ==============================
# This is a minimal reference. Expand as needed.
LAB_REFERENCE = {
    "CBC": {
        "Hemoglobin": {"male": "13.5-17.5 g/dL", "female": "12-16 g/dL"},
        "WBC": "4,000-11,000 /µL",
        "Platelets": "150,000-450,000 /µL"
    },
    "LFT": {
        "ALT": "7-56 U/L",
        "AST": "10-40 U/L",
        "Bilirubin": "0.1-1.2 mg/dL"
    },
    "RFT": {
        "Creatinine": "0.6-1.3 mg/dL",
        "BUN": "7-20 mg/dL",
        "eGFR": "≥90 mL/min/1.73m²"
    },
    "Electrolytes": {
        "Na": "135-145 mmol/L",
        "K": "3.5-5.0 mmol/L",
        "Ca": "8.5-10.5 mg/dL"
    }
}

# ==============================
# LAB MODULE UI
# ==============================
def lab_module_ui():
    st.title("Lab Interpretation Module")
    st.write("Enter your lab values to get basic interpretation and recommendations.")

    lab_type = st.selectbox("Select Lab Type", list(LAB_REFERENCE.keys()))
    lab_values = {}

    # Input fields for each lab parameter dynamically
    for param in LAB_REFERENCE[lab_type]:
        lab_values[param] = st.text_input(f"Enter value for {param}", "")

    if st.button("Interpret Lab Values"):
        st.subheader("Interpretation Results")

        for param, value in lab_values.items():
            if not value:
                st.warning(f"{param} value is missing!")
                continue

            try:
                value_float = float(value)
            except ValueError:
                st.error(f"{param} must be a numeric value!")
                continue

            ref = LAB_REFERENCE[lab_type][param]
            if isinstance(ref, dict):  # Gender specific (e.g., Hemoglobin)
                male_range = ref.get("male", "")
                female_range = ref.get("female", "")
                st.write(f"{param} Reference - Male: {male_range}, Female: {female_range}")
            else:
                st.write(f"{param} Reference: {ref}")

            # Basic interpretation (simple comparison)
            if isinstance(ref, str) and "-" in ref:
                low, high = map(float, ref.split("-"))
                if value_float < low:
                    st.write(f"{param}: LOW")
                elif value_float > high:
                    st.write(f"{param}: HIGH")
                else:
                    st.write(f"{param}: Normal")
            else:
                st.write(f"{param}: Check reference manually")
