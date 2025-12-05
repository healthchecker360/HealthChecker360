import requests
from config import GEMINI_API_KEY, GEMINI_API_URL, GROQ_API_KEY, GROQ_API_URL, TTS_LANG, TOP_K
from rag_engine import retrieve_relevant_chunks
from gtts import gTTS
from fpdf import FPDF
import os
import streamlit as st

# ------------------------------
# Helper: LLM call to Gemini
# ------------------------------
def query_gemini(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"prompt": prompt, "max_tokens": 300}
        response = requests.post(f"{GEMINI_API_URL}completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "")
    except Exception as e:
        return f"[ERROR] Gemini API: {str(e)}"

# ------------------------------
# Helper: LLM call to Groq
# ------------------------------
def query_groq(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"prompt": prompt, "max_tokens": 300}
        response = requests.post(f"{GROQ_API_URL}completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "")
    except Exception as e:
        return f"[ERROR] Groq API: {str(e)}"

# ------------------------------
# Generate Concise Clinical Answer
# ------------------------------
def generate_clinical_answer(query, engine="gemini", top_k=TOP_K):
    chunks = retrieve_relevant_chunks(query, top_k=top_k)
    if not chunks:
        return "[ERROR] No relevant context found in PDFs."

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
    try:
        tts = gTTS(text=text, lang=TTS_LANG)
        tts.save(output_path)
        return output_path
    except Exception as e:
        return f"[ERROR] TTS failed: {str(e)}"

# ------------------------------
# Optional: PDF Generation
# ------------------------------
def text_to_pdf(text, output_path="output.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split("\n"):
            pdf.multi_cell(0, 7, line)
        pdf.output(output_path)
        return output_path
    except Exception as e:
        return f"[ERROR] PDF generation failed: {str(e)}"

# ------------------------------
# Streamlit helper
# ------------------------------
def handle_query(query, engine="gemini"):
    with st.spinner("🔹 Generating clinical answer..."):
        answer = generate_clinical_answer(query, engine)
    st.success("✅ Clinical answer generated!")
    st.text_area("Answer:", answer, height=300)

    # TTS
    if st.button("🔊 Play TTS"):
        tts_file = text_to_speech(answer)
        if tts_file.endswith(".mp3"):
            audio_bytes = open(tts_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error(tts_file)

    # PDF download
    if st.button("📄 Download PDF"):
        pdf_file = text_to_pdf(answer)
        if pdf_file.endswith(".pdf"):
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name="clinical_answer.pdf")
        else:
            st.error(pdf_file)
