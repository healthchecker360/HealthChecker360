import os
import json
import requests
from config import DEBUG, OPENFDA_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, TEMP_PATH
from modules.ai_engine import query_gemini, query_groq

DRUG_DB_PATH = os.path.join("database", "drugs.json")

# ------------------------------
# Load local drug database
# ------------------------------
def load_local_drug_db():
    if os.path.exists(DRUG_DB_PATH):
        with open(DRUG_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        if DEBUG:
            print(f"[DEBUG] Drug database not found at {DRUG_DB_PATH}")
        return {}

# ------------------------------
# Query OpenFDA for a drug
# ------------------------------
def query_openfda(drug_name: str):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}&limit=1"
    try:
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])
        if results:
            result = results[0]
            info = {
                "name": drug_name,
                "indications": result.get("indications_and_usage", ["Not available"])[0],
                "warnings": result.get("warnings", ["Not available"])[0],
                "dosage": result.get("dosage_and_administration", ["Not available"])[0],
            }
            return info
        else:
            return None
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] OpenFDA query failed: {e}")
        return None

# ------------------------------
# Query AI (Gemini or Groq)
# ------------------------------
def query_ai_drug_info(drug_name: str):
    prompt = f"Provide professional medical information about the drug '{drug_name}': indications, dosage, warnings, side effects."
    try:
        if GOOGLE_API_KEY:
            return query_gemini(prompt)
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Gemini query failed: {e}")
    try:
        if GROQ_API_KEY:
            return query_groq(prompt)
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Groq query failed: {e}")
    return f"No detailed AI info available for {drug_name}."

# ------------------------------
# Main function to get drug info
# ------------------------------
def get_drug_info(drug_name: str):
    local_db = load_local_drug_db()
    drug_info = local_db.get(drug_name.lower())
    
    if drug_info:
        return drug_info

    # Check OpenFDA
    drug_info = query_openfda(drug_name)
    if drug_info:
        return drug_info

    # Fallback to AI
    ai_info = query_ai_drug_info(drug_name)
    return {"name": drug_name, "info": ai_info}

# ------------------------------
# Streamlit UI function
# ------------------------------
def drug_module_ui(drug_name: str):
    info = get_drug_info(drug_name)
    text = f"**Drug Name:** {info.get('name')}\n\n"
    if 'indications' in info:
        text += f"**Indications:** {info.get('indications')}\n"
        text += f"**Warnings:** {info.get('warnings')}\n"
        text += f"**Dosage:** {info.get('dosage')}\n"
    else:
        text += f"**Info:** {info.get('info')}\n"
    return text
