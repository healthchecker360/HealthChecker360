import streamlit as st
from ai_engine import text_to_speech, text_to_pdf
import math

# ------------------------------
# Calculator Functions
# ------------------------------
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def calculate_bsa(weight_kg, height_cm):
    # Mosteller formula
    bsa = math.sqrt((height_cm * weight_kg) / 3600)
    return round(bsa, 2)

def calculate_gfr(creatinine_mg_dl, age, sex, race="non-black"):
    """
    Simplified MDRD equation (ml/min/1.73m2)
    """
    gfr = 175 * (creatinine_mg_dl ** -1.154) * (age ** -0.203)
    if sex.lower() == "female":
        gfr *= 0.742
    if race.lower() == "black":
        gfr *= 1.212
    return round(gfr, 2)

# ------------------------------
# Streamlit Calculators Module
# ------------------------------
def calculators_module_ui():
    st.header("🧮 Clinical & Pharma Calculators")

    calc_type = st.selectbox("Select Calculator:", ["BMI", "BSA", "GFR"])

    result_text = ""

    if calc_type == "BMI":
        weight = st.number_input("Weight (kg):", min_value=1.0)
        height = st.number_input("Height (cm):", min_value=1.0)
        if st.button("Calculate BMI"):
            bmi = calculate_bmi(weight, height)
            result_text = f"BMI: {bmi}\nInterpretation:\n- Underweight: <18.5\n- Normal: 18.5–24.9\n- Overweight: 25–29.9\n- Obese: ≥30"

    elif calc_type == "BSA":
        weight = st.number_input("Weight (kg):", min_value=1.0)
        height = st.number_input("Height (cm):", min_value=1.0)
        if st.button("Calculate BSA"):
            bsa = calculate_bsa(weight, height)
            result_text = f"BSA: {bsa} m² (Mosteller formula)"

    elif calc_type == "GFR":
        creatinine = st.number_input("Serum Creatinine (mg/dL):", min_value=0.1)
        age = st.number_input("Age (years):", min_value=1)
        sex = st.selectbox("Sex:", ["Male", "Female"])
        race = st.selectbox("Race:", ["Non-Black", "Black"])
        if st.button("Calculate GFR"):
            gfr = calculate_gfr(creatinine, age, sex, race=race.lower())
            result_text = f"Estimated GFR: {gfr} mL/min/1.73 m²"

    # Display result + optional TTS and PDF
    if result_text:
        st.subheader("✅ Result")
        st.text_area("Output", value=result_text, height=200)

        # Optional TTS
        tts_file = text_to_speech(result_text)
        st.audio(tts_file, format="audio/mp3")

        # Optional PDF
        pdf_file = text_to_pdf(result_text)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"{calc_type}_result.pdf", mime="application/pdf")

# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    import streamlit as st
    calculators_module_ui()
