import streamlit as st
import json
import os
import sys

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import DRUG_DB_PATH

def drug_module_ui():
    st.write("Drug Module")
    if os.path.exists(DRUG_DB_PATH):
        with open(DRUG_DB_PATH, "r") as f:
            drugs = json.load(f)
        st.json(drugs)
    else:
        st.write("Drug database not found.")

