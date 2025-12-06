import streamlit as st

# ==============================
# SAMPLE DRUG DATABASE
# ==============================
# For demonstration, using a simple dictionary. 
# You can replace this with a CSV, JSON, or real database later.
DRUG_DB = {
    "Paracetamol": {
        "MOA": "Inhibits prostaglandin synthesis in CNS and blocks pain impulses peripherally.",
        "Indications": ["Fever", "Mild to moderate pain"],
        "Doses": {"Adult": "500-1000mg every 6-8 hours", "Child": "10-15mg/kg every 6-8 hours"},
        "Side Effects": ["Nausea", "Allergic reactions", "Hepatotoxicity in overdose"],
        "Warnings": ["Liver disease", "Alcohol use caution"],
        "Formulations": ["Tablet", "Syrup", "IV injection"]
    },
    "Ibuprofen": {
        "MOA": "Nonsteroidal anti-inflammatory drug (NSAID) that inhibits COX-1 and COX-2 enzymes.",
        "Indications": ["Pain", "Inflammation", "Fever"],
        "Doses": {"Adult": "200-400mg every 6-8 hours", "Child": "5-10mg/kg every 6-8 hours"},
        "Side Effects": ["GI upset", "Renal impairment", "Bleeding risk"],
        "Warnings": ["Peptic ulcer", "Renal disease", "Pregnancy caution"],
        "Formulations": ["Tablet", "Suspension", "IV injection"]
    }
}

# ==============================
# DRUG MODULE UI
# ==============================
def drug_module_ui():
    st.title("Drug Information Module")
    st.write("Search for drug information including MOA, doses, side effects, warnings, and formulations.")

    drug_name = st.text_input("Enter drug name", placeholder="e.g., Paracetamol")

    if st.button("Search") and drug_name:
        drug_info = DRUG_DB.get(drug_name.title())
        if drug_info:
            st.subheader(f"Drug: {drug_name.title()}")
            st.markdown(f"**Mechanism of Action (MOA):** {drug_info['MOA']}")
            st.markdown(f"**Indications:** {', '.join(drug_info['Indications'])}")
            st.markdown("**Doses:**")
            for key, dose in drug_info["Doses"].items():
                st.write(f"- {key}: {dose}")
            st.markdown(f"**Side Effects:** {', '.join(drug_info['Side Effects'])}")
            st.markdown(f"**Warnings:** {', '.join(drug_info['Warnings'])}")
            st.markdown(f"**Formulations:** {', '.join(drug_info['Formulations'])}")
        else:
            st.warning("Drug not found in database. Please check spelling or add to database.")
