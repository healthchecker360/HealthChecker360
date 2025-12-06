import streamlit as st
import pandas as pd
from config import DRUG_DB_PATH, DEBUG

# ------------------------------
# Load Drug Database
# ------------------------------
def load_drug_db():
    """
    Load the drug database as a pandas DataFrame.
    """
    if not DRUG_DB_PATH.exists():
        if DEBUG:
            st.warning(f"Drug database not found at {DRUG_DB_PATH}. You can add a local CSV or fallback to APIs.")
        return pd.DataFrame()  # empty df
    try:
        df = pd.read_csv(DRUG_DB_PATH)
        return df
    except Exception as e:
        st.error(f"Error loading drug database: {e}")
        return pd.DataFrame()

# ------------------------------
# Get Drug Info
# ------------------------------
def get_drug_info(drug_name, df):
    """
    Search local drug DB for the drug_name.
    Returns dictionary of drug info if found, else None
    """
    if df.empty:
        return None
    drug_row = df[df['drug_name'].str.lower() == drug_name.lower()]
    if not drug_row.empty:
        return drug_row.iloc[0].to_dict()
    return None

# ------------------------------
# Streamlit UI
# ------------------------------
def drug_module_ui():
    st.title("HealthChecker360 - Drug Information Module")
    st.markdown(
        "Search for any drug to get MOA, PK/PD, doses, side effects, interactions, and formulations."
    )

    drug_name = st.text_input("Enter drug name:")
    df = load_drug_db()

    if st.button("Get Drug Info") and drug_name.strip():
        info = get_drug_info(drug_name, df)
        
        if info:
            st.subheader(f"Information for {drug_name.title()}")
            st.write(f"**Mechanism of Action (MOA):** {info.get('MOA', 'N/A')}")
            st.write(f"**Pharmacodynamics (PD):** {info.get('PD', 'N/A')}")
            st.write(f"**Pharmacokinetics (PK):** {info.get('PK', 'N/A')}")
            st.write(f"**Dosage:** {info.get('dosage', 'N/A')}")
            st.write(f"**Side Effects:** {info.get('side_effects', 'N/A')}")
            st.write(f"**Interactions:** {info.get('interactions', 'N/A')}")
            st.write(f"**Brands/Formulations:** {info.get('brands', 'N/A')}")
        else:
            st.warning(f"{drug_name.title()} not found in local database.")
            st.info("This can be extended to fetch from RxNorm/OpenFDA or other online sources.")

# ------------------------------
# Direct run
# ------------------------------
if __name__ == "__main__":
    drug_module_ui()
