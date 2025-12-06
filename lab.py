import json
import os
from config import LAB_REFERENCE

# -----------------------------
# Load Lab Reference Ranges
# -----------------------------
def load_lab_reference():
    """
    Loads lab reference values from a JSON file.
    Example JSON structure:
    {
        "Hemoglobin": {"male": [13, 17], "female": [12, 15]},
        "WBC": [4.0, 11.0]
    }
    """
    if not os.path.exists(LAB_REFERENCE):
        print(f"⚠️ Lab reference file not found: {LAB_REFERENCE}")
        return {}

    with open(LAB_REFERENCE, "r") as f:
        data = json.load(f)
    return data


# -----------------------------
# Interpret Lab Results
# -----------------------------
def interpret_lab_result(test_name, value, gender=None):
    """
    Compares lab value against reference ranges.
    Returns interpretation string.
    """
    refs = load_lab_reference()

    if test_name not in refs:
        return f"No reference available for {test_name}."

    ref = refs[test_name]

    # Gender-specific reference
    if isinstance(ref, dict):
        if gender is None:
            return f"Reference range for {test_name} depends on gender."
        if gender.lower() not in ref:
            return f"Gender '{gender}' not recognized for {test_name}."
        low, high = ref[gender.lower()]
    else:
        low, high = ref

    # Interpretation
    if value < low:
        result = "Low"
    elif value > high:
        result = "High"
    else:
        result = "Normal"

    return f"{test_name}: {value} ({result}) — Reference: {low}-{high}"


# -----------------------------
# Example Lab Module UI
# -----------------------------
def lab_module_ui():
    """
    CLI-based lab module (can later integrate with Streamlit)
    """
    print("=== Lab Interpretation Module ===")
    test_name = input("Enter lab test name: ").strip()
    try:
        value = float(input("Enter test value: ").strip())
    except ValueError:
        print("⚠️ Invalid value entered!")
        return

    gender = input("Enter gender (optional): ").strip() or None
    result = interpret_lab_result(test_name, value, gender)
    print("\n" + result)
