import requests
from config import GEMINI_API_KEY, GEMINI_API_URL, GROQ_API_KEY, GROQ_API_URL, TTS_LANG, VECTOR_STORE_PATH, TOP_K
from rag_engine import retrieve_relevant_chunks
from gtts import gTTS
from fpdf import FPDF
import os

# ------------------------------
# Helper: LLM call to Gemini
# ------------------------------
def query_gemini(prompt):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 300  # limit response to concise clinical info
    }
    response = requests.post(f"{GEMINI_API_URL}completions", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "")
    else:
        return f"[ERROR] Gemini API: {response.status_code} - {response.text}"


# ------------------------------
# Helper: LLM call to Groq
# ------------------------------
def query_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 300
    }
    response = requests.post(f"{GROQ_API_URL}completions", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "")
    else:
        return f"[ERROR] Groq API: {response.status_code} - {response.text}"


# ------------------------------
# Generate Concise Clinical Answer
# ------------------------------
def generate_clinical_answer(query, engine="gemini", top_k=TOP_K):
    """
    Steps:
    1. Retrieve top-k PDF chunks
    2. Create prompt for LLM emphasizing concise clinical answer
    3. Return text answer
    """
    chunks = retrieve_relevant_chunks(query, top_k=top_k)
    context_text = "\n\n".join(chunks)

    prompt = f"""
You are a professional clinical assistant. Provide a concise, targeted, evidence-based clinical answer to the following query using the context below. 
- Only include essential information. 
- If it's about drugs, include: Dose, MOA, Warnings, Side effects, Formulations. 
- If it's labs: include interpretation and next steps. 
- If calculations: include result and brief explanation.
- Do not add extra information.

Query: {query}

Context:
{context_text}
"""

    if engine.lower() == "gemini":
        answer = query_gemini(prompt)
    else:
        answer = query_groq(prompt)
    return answer.strip()


# ------------------------------
# Optional: Text-to-Speech
# ------------------------------
def text_to_speech(text, output_path="output.mp3"):
    tts = gTTS(text=text, lang=TTS_LANG)
    tts.save(output_path)
    return output_path


# ------------------------------
# Optional: PDF Generation
# ------------------------------
def text_to_pdf(text, output_path="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 7, line)
    pdf.output(output_path)
    return output_path


# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    query = "Paracetamol adult dose and side effects"
    answer = generate_clinical_answer(query, engine="gemini")
    print("----- Clinical Answer -----")
    print(answer)

    # Optional: generate TTS
    tts_file = text_to_speech(answer)
    print(f"TTS saved at: {tts_file}")

    # Optional: generate PDF
    pdf_file = text_to_pdf(answer)
    print(f"PDF saved at: {pdf_file}")
