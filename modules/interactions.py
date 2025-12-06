from modules.ai_engine import generate_clinical_answer
from config import TOP_K, DEBUG

def chat_diagnosis_module(query: str) -> str:
    """
    Main function to handle user query for diagnosis or medical info.
    1. Searches local FAISS index first.
    2. If not found, uses Gemini/Groq APIs as fallback.
    Returns a professional answer string.
    """
    if not query.strip():
        return "⚠️ Please enter a valid medical query."

    try:
        # Call AI engine which handles RAG + online fallback
        answer = generate_clinical_answer(query, top_k=TOP_K)

        if not answer or answer.strip() == "":
            # Fallback message if nothing is returned
            return (
                "No information found in local database. "
                "Attempted online search but could not fetch a result. "
                "Please consult a healthcare professional."
            )

        return answer

    except Exception as e:
        if DEBUG:
            return f"Error generating answer: {e}"
        return "⚠️ Something went wrong while fetching your answer."
