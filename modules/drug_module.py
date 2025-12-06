import streamlit as st
from .config import DRUG_DB_PATH
import json
import os

def drug_module_ui():
    st.write("Drug Module")
    if os.path.exists(DRUG_DB_PATH):
        with open(DRUG_DB_PATH, "r") as f:
            drugs = json.load(f)
        st.json(drugs)
    else:
        st.write("Drug database not found.")
