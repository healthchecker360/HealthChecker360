import streamlit as st

# ------------------------------
# LAB MODULE UI
# ------------------------------
def lab_module_ui():
    st.title("HealthChecker360 - Lab Test Interpretation")
    st.write("Enter your lab values to get a basic interpretation.")

    # Example labs
    labs = {
        "Hemoglobin (g/dL)": (12, 16),
        "WBC (10^3/µL)": (4, 11),
        "Platelets (10^3/µL)": (150, 450),
        "Creatinine (mg/dL)": (0.6, 1.3),
        "BUN (mg/dL)": (7, 20),
        "ALT (U/L)": (7, 56),
        "AST (U/L)": (10, 40),
        "TSH (µIU/mL)": (0.4, 4.0),
        "Blood Glucose Fasting (mg/dL)": (70, 100),
        "HbA1c (%)": (4, 5.6)
    }

    user_values = {}
    for lab_name, (low, high) in labs.items():
        user_values[lab_name] = st.number_input(f"{lab_name} [{low}-{high}]", min_value=0.0)

    if st.button("Interpret Labs"):
        st.subheader("Interpretation Results")
        for lab_name, (low, high) in labs.items():
            value = user_values[lab_name]
            if value < low:
                st.markdown(f"**{lab_name}:** Low ({value})")
            elif value > high:
                st.markdown(f"**{lab_name}:** High ({value})")
            else:
                st.markdown(f"**{lab_name}:** Normal ({value})")
