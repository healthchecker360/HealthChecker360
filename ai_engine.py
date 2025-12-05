# ai_engine.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from rag_engine import query_rag
from gtts import gTTS

load_dotenv()

# -------------------------
# API KEYS
# -------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# -------------------------
# System prompts
# -------------------------
SYSTEM_PROMPT_PATIENT = """
You are Health Checker 365.
Answer the question in simple, clear language for a patient.
Include key info, treatment, warnings, and common side effects.
Keep it short and professional.
"""

SYSTEM_PROMPT_PROFESSIONAL = """
You are Health Checker 365.
Answer the question in professional clinical language for healthcare professionals.
Include diagnosis, treatment options, mechanism, warnings, and references.
Keep it concise and targeted.
"""

# -------------------------
# Helper: Call Gemini
# -------------------------
def call_gemini(prompt, image=None):
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API key missing."
    try:
        model_name = "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"

# -------------------------
# Helper: Call Groq (example)
# -------------------------
def call_groq(prompt):
    if not GROQ_API_KEY:
        return "⚠️ Groq API key missing."
    try:
        # Example Groq API call (replace with your endpoint)
        url = "https://api.groq.ai/generate"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        payload = {"prompt": prompt, "max_tokens": 300}
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            return resp.json().get("text", "")
        else:
            return f"⚠️ Groq error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"⚠️ Groq exception: {str(e)}"

# -------------------------
# Generate TTS (optional)
# -------------------------
def generate_tts(text, filename="answer.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# -------------------------
# Main function: RAG + LLM
# -------------------------
def get_rag_answer(query, audience="patient", top_k=3, llm="gemini"):
    """
    query: user question
    audience: 'patient' or 'professional'
    top_k: number of RAG chunks to retrieve
    llm: 'gemini' or 'groq'
    """

    # Step 1: Retrieve relevant context
    context_chunks = query_rag(query, top_k=top_k)
    context_text = " ".join([c["text"] for c in context_chunks]) if context_chunks else ""

    # Step 2: Prepare prompt with context
    if audience.lower() == "patient":
        system_prompt = SYSTEM_PROMPT_PATIENT
    else:
        system_prompt = SYSTEM_PROMPT_PROFESSIONAL

    full_prompt = f"{system_prompt}\nContext: {context_text}\nQuestion: {query}"

    # Step 3: Call selected LLM
    if llm.lower() == "gemini":
        answer = call_gemini(full_prompt)
    else:
        answer = call_groq(full_prompt)

    return answer
