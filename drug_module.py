import json
import os
import streamlit as st
from config import DRUG_DB_PATH

# -----------------------------
# Load Drug Database
# -----------------------------
@st.cache_data
def load_drug_database():
    """Load drug data from JSON"""
    if not os.path.exists(DRUG_DB_PATH):
        st.warning(f"Drug database file not found: {DRUG_DB_PATH}")
        return {}
    with open(DRUG_DB_PATH, "r") as f:
        return json.load(f)


# -----------------------------
# Get Drug Info
# -----------------------------
def get_drug_info(drug_name: str):
    db = load_drug_database()
    for key, value in db.items():
        if key.lower() == drug_name.lower():
            return value
    return None


# -----------------------------
# Search Drugs
# -----------------------------
def search_drugs(keyword: str):
    db = load_drug_database()
    keyword = keyword.lower()
    matches = []
    for key, value in db.items():
        if (keyword in key.lower() 
            or any(keyword in b.lower() for b in value.get("brand_names", []))
            or any(keyword in f.lower() for f in value.get("formulations", []))):
            matches.append(key)
    return matches


# -----------------------------
# Streamlit UI
# -----------------------------
def drug_module_ui():
    st.header("💊 Drug Information Module")
    query = st.text_input("Enter drug name or keyword")
    if not query:
        return

    matches = search_drugs(query)
    if not matches:
        st.info(f"No drugs found for '{query}'")
        return

    st.write(f"Found {len(matches)} drug(s): {', '.join(matches)}")

    for drug in matches:
        info = get_drug_info(drug)
        if info:
            st.subheader(drug)
            st.write("**Brand Names:**", ", ".join(info.get("brand_names", [])))
            st.write("**Formulations:**", ", ".join(info.get("formulations", [])))
            st.write("**MOA:**", info.get("moa", "N/A"))
            st.write("**Pharmacodynamics:**", info.get("pharmacodynamics", "N/A"))
            st.write("**Pharmacokinetics:**", info.get("pharmacokinetics", "N/A"))
            st.write("**Dose:**", info.get("dose", "N/A"))
            st.write("**Adjustments:**", info.get("adjustments", "N/A"))
            st.write("**Side Effects:**", ", ".join(info.get("side_effects", [])))
            st.write("**Interactions:**", ", ".join(info.get("interactions", [])))
            st.write("**Contraindications:**", ", ".join(info.get("contraindications", [])))
            st.write("**Pregnancy/Lactation:**", info.get("pregnancy_lactation", "N/A"))
            st.write("**Max Daily Dose:**", info.get("max_dose", "N/A"))
        else:
            st.warning(f"No data found for {drug}")


# -----------------------------
# Optional CLI fallback
# -----------------------------
if __name__ == "__main__":
    import sys
    st = sys.modules.get("streamlit")  # For CLI testing
    if not st:
        from pprint import pprint as st
    drug_module_ui()
