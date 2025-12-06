import streamlit as st
import pandas as pd
from pathlib import Path

# ------------------------------
# CONFIG
# ------------------------------
DRUG_DB_PATH = Path("docs/drug_database.csv")  # Example CSV file with drug info

# ------------------------------
# LOAD DRUG DATA
# ------------------------------
def load_drug_data():
    if DRUG_DB_PATH.exists():
        df = pd.read_csv(DRUG_DB_PATH)
        return df
    else:
        st.warning("Drug database not found. Please place 'drug_database.csv' in docs folder.")
        return pd.DataFrame()  # Empty DataFrame

# ------------------------------
# DRUG MODULE UI
# ------------------------------
def drug_module_ui():
    st.title("HealthChecker360 - Drug Module")
    st.write("Search for drug information including MOA, dosage, side effects, and interactions.")

    df = load_drug_data()
    if df.empty:
        return

    drug_list = df['Drug Name'].tolist()
    selected_drug = st.selectbox("Select Drug", [""] + drug_list)

    if selected_drug:
        drug_info = df[df['Drug Name'] == selected_drug].iloc[0]

        st.subheader(f"{selected_drug} Information")
        st.markdown(f"**Mechanism of Action (MOA):** {drug_info.get('MOA', 'N/A')}")
        st.markdown(f"**Indications:** {drug_info.get('Indications', 'N/A')}")
        st.markdown(f"**Dosage:** {drug_info.get('Dosage', 'N/A')}")
        st.markdown(f"**Side Effects:** {drug_info.get('Side Effects', 'N/A')}")
        st.markdown(f"**Warnings / Precautions:** {drug_info.get('Warnings', 'N/A')}")
        st.markdown(f"**Drug Interactions:** {drug_info.get('Interactions', 'N/A')}")
        st.markdown(f"**Brand Names:** {drug_info.get('Brand Names', 'N/A')}")
