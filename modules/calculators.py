import streamlit as st
import math

# ------------------------------
# Clinical Calculators
# ------------------------------

def calculate_bmi(weight, height):
    """BMI = weight(kg) / height(m)^2"""
    if height <= 0:
        return None
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def calculate_bsa(weight, height):
    """Mosteller formula: BSA = sqrt((height(cm)*weight(kg))/3600)"""
    bsa = math.sqrt((height * weight) / 3600)
    return round(bsa, 2)

def calculate_gfr(creatinine, age, sex, race='non-black'):
    """
    Simplified CKD-EPI equation (ml/min/1.73 m^2)
    sex: 'male' or 'female'
    race: 'black' or 'non-black'
    """
    k = 0.7 if sex.lower() == 'female' else 0.9
    alpha = -0.329 if sex.lower() == 'female' else -0.411
    min_scr_k = min(creatinine / k, 1)
    max_scr_k = max(creatinine / k, 1)
    gfr = 141 * (min_scr_k ** alpha) * (max_scr_k ** -1.209) * (0.993 ** age)
    if sex.lower() == 'female':
        gfr *= 1.018
    if race.lower() == 'black':
        gfr *= 1.159
    return round(gfr, 2)

# ------------------------------
# Pharmaceutical Calculators
# ------------------------------

def drip_rate(volume_ml, time_min, drop_factor=20):
    """IV drip rate in drops/min"""
    rate = (volume_ml * drop_factor) / time_min
    return round(rate, 1)

def isotonicity_calc(solute_mEq, solvent_L):
    """Simple isotonicity check (mOsm/L)"""
    try:
        osmolarity = solute_mEq / solvent_L
        return round(osmolarity, 2)
    except:
        return None

def ph_calculator(h_concentration):
    """Calculate pH from H+ concentration (mol/L)"""
    try:
        ph = -math.log10(h_concentration)
        return round(ph, 2)
    except:
        return None

# ------------------------------
# Streamlit UI
# ------------------------------
def calculators_ui():
    st.title("HealthChecker360 - Clinical & Pharmaceutical Calculators")

    st.subheader("BMI Calculator")
    weight = st.number_input("Weight (kg):", value=70.0)
    height_m = st.number_input("Height (m):", value=1.7)
    if st.button("Calculate BMI"):
        bmi = calculate_bmi(weight, height_m)
        st.success(f"BMI: {bmi}")

    st.subheader("BSA Calculator")
    weight = st.number_input("Weight (kg):", value=70.0, key="bsa_weight")
    height_cm = st.number_input("Height (cm):", value=170.0, key="bsa_height")
    if st.button("Calculate BSA"):
        bsa = calculate_bsa(weight, height_cm)
        st.success(f"BSA: {bsa} m²")

    st.subheader("GFR Calculator")
    creatinine = st.number_input("Serum Creatinine (mg/dL):", value=1.0)
    age = st.number_input("Age (years):", value=30)
    sex = st.radio("Sex:", ["Male", "Female"])
    race = st.radio("Race:", ["Non-Black", "Black"])
    if st.button("Calculate GFR"):
        gfr = calculate_gfr(creatinine, age, sex, race.lower())
        st.success(f"Estimated GFR: {gfr} ml/min/1.73 m²")

    st.subheader("IV Drip Rate Calculator")
    volume_ml = st.number_input("Volume (mL):", value=500)
    time_min = st.number_input("Time (minutes):", value=60)
    drop_factor = st.number_input("Drop factor (drops/mL):", value=20)
    if st.button("Calculate Drip Rate"):
        rate = drip_rate(volume_ml, time_min, drop_factor)
        st.success(f"Drip Rate: {rate} drops/min")

    st.subheader("Isotonicity Calculator")
    solute_mEq = st.number_input("Solute (mEq):", value=100.0)
    solvent_L = st.number_input("Solvent (L):", value=1.0)
    if st.button("Calculate Osmolarity"):
        osm = isotonicity_calc(solute_mEq, solvent_L)
        st.success(f"Osmolarity: {osm} mOsm/L")

    st.subheader("pH Calculator")
    h_conc = st.number_input("H+ concentration (mol/L):", value=1e-7, format="%.10f")
    if st.button("Calculate pH"):
        ph = ph_calculator(h_conc)
        st.success(f"pH: {ph}")

# ------------------------------
# Direct run
# ------------------------------
if __name__ == "__main__":
    calculators_ui()
