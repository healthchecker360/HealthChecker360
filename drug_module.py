import json
import os
from ai_engine import generate_clinical_answer, text_to_speech, text_to_pdf

# ------------------------------
# Drug Database Path
# ------------------------------
DRUG_DB_PATH = "medical_drug_db.json"

# ------------------------------
# Sample Drug Database
# ------------------------------
sample_drug_db = {
    "Paracetamol": {
        "Dose": "500-1000 mg every 4-6 hours, max 4 g/day",
        "MOA": "Inhibits prostaglandin synthesis in CNS; analgesic and antipyretic effect",
        "Warnings": "Liver disease, alcohol use, hypersensitivity",
        "Side_effects": "Rare: rash, thrombocytopenia, hepatotoxicity in overdose",
        "Formulations": "Tablet, suspension, IV"
    },
    "Ibuprofen": {
        "Dose": "200-400 mg every 6-8 hours, max 1200 mg/day OTC",
        "MOA": "Non-selective COX inhibitor; reduces prostaglandin synthesis",
        "Warnings": "GI bleeding, renal impairment, hypersensitivity",
        "Side_effects": "Dyspepsia, nausea, headache, rash",
        "Formulations": "Tablet, suspension, IV"
    }
}

# Save sample DB if not exists
if not os.path.exists(DRUG_DB_PATH):
    with open(DRUG_DB_PATH, "w") as f:
        json.dump(sample_drug_db, f, indent=4)

# ------------------------------
# Load Drug Database
# ------------------------------
def load_drug_db():
    with open(DRUG_DB_PATH, "r") as f:
        return json.load(f)

# ------------------------------
# Retrieve Drug Info
# ------------------------------
def get_drug_info(drug_name, use_llm=False):
    """
    Retrieve concise drug monograph
    - First check internal DB
    - If not found and use_llm=True, call LLM
    """
    db = load_drug_db()
    drug_name_cap = drug_name.capitalize()

    if drug_name_cap in db:
        info = db[drug_name_cap]
        monograph = (
            f"Drug: {drug_name_cap}\n"
            f"Dose: {info['Dose']}\n"
            f"MOA: {info['MOA']}\n"
            f"Warnings: {info['Warnings']}\n"
            f"Side effects: {info['Side_effects']}\n"
            f"Formulations: {info['Formulations']}"
        )
        return monograph
    elif use_llm:
        prompt = f"Provide a concise professional drug monograph for {drug_name}: Dose, MOA, Warnings, Side effects, Formulations."
        answer = generate_clinical_answer(prompt, engine="gemini")
        return answer
    else:
        return f"[INFO] Drug '{drug_name}' not found in internal DB."

# ------------------------------
# Optional: Streamlit Interface
# ------------------------------
def drug_module_ui(st):
    st.header("💊 Drug Information Module")

    drug_name = st.text_input("Enter drug name:")
    use_llm = st.checkbox("Use AI for unknown drugs?", value=True)

    if st.button("Get Drug Info") and drug_name:
        with st.spinner("Fetching drug info..."):
            info = get_drug_info(drug_name, use_llm=use_llm)

        st.subheader("✅ Drug Monograph")
        st.text_area("Monograph", value=info, height=250)

        # Optional TTS
        tts_file = text_to_speech(info)
        st.audio(tts_file, format="audio/mp3")

        # Optional PDF
        pdf_file = text_to_pdf(info)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"{drug_name}_monograph.pdf", mime="application/pdf")


# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    import streamlit as st
    drug_module_ui(st)
