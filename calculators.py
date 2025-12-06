import json
import os
from config import DRUG_DB_PATH

# -----------------------------
# Load Drug Database
# -----------------------------
def load_drug_database():
    """
    Loads drug data from a JSON file.
    Example JSON structure:
    {
        "Paracetamol": {
            "brand_names": ["Tylenol", "Panadol"],
            "formulations": ["Tablet 500mg", "Syrup 125mg/5ml"],
            "moa": "Inhibits prostaglandin synthesis",
            "pharmacodynamics": "Analgesic, antipyretic",
            "pharmacokinetics": "Metabolized in liver, excreted in urine",
            "dose": {"adult": "500-1000mg q6h", "child": "10-15mg/kg q6h"},
            "adjustments": {"renal": "reduce dose if GFR < 30"},
            "side_effects": ["Nausea", "Hepatotoxicity in overdose"],
            "interactions": ["Warfarin", "Isoniazid"]
        }
    }
    """
    if not os.path.exists(DRUG_DB_PATH):
        print(f"⚠️ Drug database file not found: {DRUG_DB_PATH}")
        return {}
    with open(DRUG_DB_PATH, "r") as f:
        data = json.load(f)
    return data


# -----------------------------
# Get Drug Info
# -----------------------------
def get_drug_info(drug_name: str):
    """
    Returns complete drug info for given name.
    """
    db = load_drug_database()
    drug_name_lower = drug_name.lower()

    for key, value in db.items():
        if key.lower() == drug_name_lower:
            return value
    return f"No data found for drug: {drug_name}"


# -----------------------------
# Search Drugs by Keyword
# -----------------------------
def search_drugs(keyword: str):
    """
    Search drugs by keyword in name, brand, or formulation.
    Returns list of matching drug names.
    """
    db = load_drug_database()
    keyword_lower = keyword.lower()
    matches = []

    for key, value in db.items():
        if (keyword_lower in key.lower()
            or any(keyword_lower in b.lower() for b in value.get("brand_names", []))
            or any(keyword_lower in f.lower() for f in value.get("formulations", []))):
            matches.append(key)
    return matches


# -----------------------------
# Example CLI Module
# -----------------------------
def drug_module_ui():
    """
    CLI-based interaction for drug info.
    Can be replaced with Streamlit UI later.
    """
    print("=== Drug Information Module ===")
    query = input("Enter drug name or keyword: ").strip()
    if not query:
        print("⚠️ Please enter a valid keyword!")
        return

    matches = search_drugs(query)
    if not matches:
        print("No drugs found matching:", query)
        return

    print(f"\nFound {len(matches)} drug(s): {', '.join(matches)}")
    for drug in matches:
        info = get_drug_info(drug)
        if isinstance(info, dict):
            print(f"\n--- {drug} ---")
            print("Brand Names:", ", ".join(info.get("brand_names", [])))
            print("Formulations:", ", ".join(info.get("formulations", [])))
            print("MOA:", info.get("moa", "N/A"))
            print("Pharmacodynamics:", info.get("pharmacodynamics", "N/A"))
            print("Pharmacokinetics:", info.get("pharmacokinetics", "N/A"))
            print("Dose:", info.get("dose", "N/A"))
            print("Adjustments:", info.get("adjustments", "N/A"))
            print("Side Effects:", ", ".join(info.get("side_effects", [])))
            print("Interactions:", ", ".join(info.get("interactions", [])))
        else:
            print(info)
