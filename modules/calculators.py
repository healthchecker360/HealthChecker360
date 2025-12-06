import streamlit as st
import math

# ==============================
# CALCULATORS MODULE
# ==============================
def calculators_ui():
    st.title("HealthChecker360 - Calculators Module")
    st.write("Perform clinical, pharmaceutical, and industry calculations easily.")

    calc_type = st.selectbox("Select Calculator Type", ["Clinical", "Pharmaceutical", "Industry"])

    # ------------------------------
    # CLINICAL CALCULATORS
    # ------------------------------
    if calc_type == "Clinical":
        st.subheader("Clinical Calculators")

        option = st.selectbox("Choose Calculator", ["BMI", "BSA", "GFR", "ABG"])

        if option == "BMI":
            weight = st.number_input("Weight (kg)", 0.0)
            height = st.number_input("Height (cm)", 0.0)
            if st.button("Calculate BMI"):
                if height > 0:
                    bmi = weight / ((height/100)**2)
                    st.success(f"BMI: {bmi:.2f}")
                else:
                    st.error("Height must be greater than 0")

        elif option == "BSA":
            weight = st.number_input("Weight (kg)", 0.0)
            height = st.number_input("Height (cm)", 0.0)
            if st.button("Calculate BSA"):
                if height > 0:
                    bsa = math.sqrt((height * weight)/3600)
                    st.success(f"BSA: {bsa:.2f} m²")
                else:
                    st.error("Height must be greater than 0")

        elif option == "GFR":
            creatinine = st.number_input("Serum Creatinine (mg/dL)", 0.0)
            age = st.number_input("Age (years)", 0)
            sex = st.selectbox("Sex", ["Male", "Female"])
            if st.button("Calculate GFR"):
                if creatinine > 0 and age > 0:
                    if sex == "Male":
                        gfr = 175 * (creatinine ** -1.154) * (age ** -0.203)
                    else:
                        gfr = 175 * (creatinine ** -1.154) * (age ** -0.203) * 0.742
                    st.success(f"Estimated GFR: {gfr:.2f} mL/min/1.73m²")
                else:
                    st.error("Enter valid creatinine and age")

        elif option == "ABG":
            ph = st.number_input("pH", 0.0)
            pco2 = st.number_input("PaCO2 (mmHg)", 0.0)
            hco3 = st.number_input("HCO3- (mEq/L)", 0.0)
            if st.button("Interpret ABG"):
                st.write("ABG interpretation (simplified):")
                if ph < 7.35:
                    st.write("Acidemia")
                elif ph > 7.45:
                    st.write("Alkalemia")
                else:
                    st.write("Normal pH")
                st.write(f"PaCO2: {pco2} mmHg, HCO3-: {hco3} mEq/L")

    # ------------------------------
    # PHARMACEUTICAL CALCULATORS
    # ------------------------------
    elif calc_type == "Pharmaceutical":
        st.subheader("Pharmaceutical Calculators")

        option = st.selectbox("Choose Calculator", ["Dilution", "pH", "Isotonicity"])

        if option == "Dilution":
            stock_conc = st.number_input("Stock Concentration (mg/mL)", 0.0)
            final_conc = st.number_input("Desired Concentration (mg/mL)", 0.0)
            final_vol = st.number_input("Final Volume (mL)", 0.0)
            if st.button("Calculate Dilution"):
                if final_conc > 0:
                    vol_needed = (final_conc * final_vol)/stock_conc
                    st.success(f"Volume of stock solution needed: {vol_needed:.2f} mL")
                else:
                    st.error("Desired concentration must be greater than 0")

        elif option == "pH":
            st.write("pH calculator coming soon...")

        elif option == "Isotonicity":
            st.write("Isotonicity calculator coming soon...")

    # ------------------------------
    # INDUSTRY CALCULATORS
    # ------------------------------
    elif calc_type == "Industry":
        st.subheader("Industry Calculators")

        option = st.selectbox("Choose Calculator", ["Batch Size", "Yield", "Coating/ Mixing"])

        if option == "Batch Size":
            target_batch = st.number_input("Target Batch Size (kg)", 0.0)
            if st.button("Calculate"):
                st.success(f"Batch Size confirmed: {target_batch} kg")

        elif option == "Yield":
            theoretical_yield = st.number_input("Theoretical Yield (kg)", 0.0)
            actual_yield = st.number_input("Actual Yield (kg)", 0.0)
            if st.button("Calculate Yield"):
                if theoretical_yield > 0:
                    yield_percent = (actual_yield / theoretical_yield) * 100
                    st.success(f"Yield: {yield_percent:.2f} %")
                else:
                    st.error("Theoretical yield must be greater than 0")

        elif option == "Coating/ Mixing":
            st.write("Coating/Mixing calculations coming soon...")
