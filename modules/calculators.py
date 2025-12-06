import streamlit as st
import math

# ------------------------------
# CALCULATORS MODULE UI
# ------------------------------
def calculators_ui():
    st.title("HealthChecker360 - Calculators")
    st.write("Select a calculator below:")

    calc_options = [
        "BMI",
        "BSA (Mosteller)",
        "Cockcroft-Gault GFR",
        "IV Drip Rate (mL/hr)",
        "Paracetamol Dose (mg/kg)"
    ]
    choice = st.selectbox("Choose Calculator", [""] + calc_options)

    # ------------------------------
    # BMI Calculator
    # ------------------------------
    if choice == "BMI":
        weight = st.number_input("Weight (kg)", min_value=0.0)
        height = st.number_input("Height (cm)", min_value=0.0)
        if st.button("Calculate BMI"):
            if height > 0:
                bmi = weight / ((height / 100) ** 2)
                st.markdown(f"**BMI:** {bmi:.2f}")
                if bmi < 18.5:
                    st.markdown("Underweight")
                elif 18.5 <= bmi < 25:
                    st.markdown("Normal weight")
                elif 25 <= bmi < 30:
                    st.markdown("Overweight")
                else:
                    st.markdown("Obese")
            else:
                st.warning("Height must be greater than 0")

    # ------------------------------
    # BSA Calculator (Mosteller)
    # ------------------------------
    elif choice == "BSA (Mosteller)":
        weight = st.number_input("Weight (kg)", min_value=0.0, key="bsa_weight")
        height = st.number_input("Height (cm)", min_value=0.0, key="bsa_height")
        if st.button("Calculate BSA"):
            if height > 0 and weight > 0:
                bsa = math.sqrt((height * weight) / 3600)
                st.markdown(f"**BSA:** {bsa:.2f} m²")
            else:
                st.warning("Height and weight must be greater than 0")

    # ------------------------------
    # Cockcroft-Gault GFR
    # ------------------------------
    elif choice == "Cockcroft-Gault GFR":
        age = st.number_input("Age (years)", min_value=0)
        weight = st.number_input("Weight (kg)", min_value=0.0, key="gfr_weight")
        creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0)
        gender = st.selectbox("Gender", ["Male", "Female"])
        if st.button("Calculate GFR"):
            if creatinine > 0 and weight > 0:
                gfr = ((140 - age) * weight) / (72 * creatinine)
                if gender == "Female":
                    gfr *= 0.85
                st.markdown(f"**Estimated GFR:** {gfr:.2f} mL/min")
            else:
                st.warning("Enter valid weight and creatinine")

    # ------------------------------
    # IV Drip Rate Calculator
    # ------------------------------
    elif choice == "IV Drip Rate (mL/hr)":
        total_volume = st.number_input("Total Volume (mL)", min_value=0.0)
        duration = st.number_input("Duration (hours)", min_value=0.0)
        if st.button("Calculate Drip Rate"):
            if duration > 0:
                rate = total_volume / duration
                st.markdown(f"**IV Drip Rate:** {rate:.2f} mL/hr")
            else:
                st.warning("Duration must be greater than 0")

    # ------------------------------
    # Paracetamol Dose Calculator
    # ------------------------------
    elif choice == "Paracetamol Dose (mg/kg)":
        weight = st.number_input("Weight (kg)", min_value=0.0, key="para_weight")
        dose_per_kg = 15  # mg/kg single dose
        max_daily = 4000  # mg/day
        if st.button("Calculate Dose"):
            if weight > 0:
                single_dose = weight * dose_per_kg
                st.markdown(f"**Single Dose:** {single_dose:.0f} mg")
                st.markdown(f"**Maximum Daily Dose:** {max_daily} mg")
            else:
                st.warning("Weight must be greater than 0")
