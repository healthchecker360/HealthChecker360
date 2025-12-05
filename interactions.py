# interactions.py
import streamlit as st
from ai_engine import get_rag_answer, generate_tts

# -------------------------
# Session State Initialization
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "audience_mode" not in st.session_state:
    st.session_state.audience_mode = "patient"  # default

# -------------------------
# Function to handle a new message
# -------------------------
def handle_user_message(user_msg, audience="patient", llm="gemini", tts=False):
    """
    user_msg: user input
    audience: 'patient' or 'professional'
    llm: 'gemini' or 'groq'
    tts: whether to generate voice output
    """
    if not user_msg.strip():
        return

    # Step 1: Get AI answer
    answer = get_rag_answer(user_msg, audience=audience, llm=llm)

    # Step 2: Append to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_msg
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    # Step 3: Optional: generate voice
    if tts:
        audio_file = generate_tts(answer)
        return answer, audio_file
    else:
        return answer, None

# -------------------------
# Function to display chat
# -------------------------
def display_chat():
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
