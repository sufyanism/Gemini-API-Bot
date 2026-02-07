import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- 1. API Configuration ---
load_dotenv() 

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 API Key not found! Please set GEMINI_API_KEY in .env or Streamlit Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. THE SYSTEM PROMPT ---
SYSTEM_PROMPT = (
    "You are an expert Senior Software Engineer and Academic Integrity Officer. "
    "CASE 1: If the user says 'Hello' or 'Hi', reply politely in exactly one sentence. "
    "CASE 2: If the user provides CODE, perform a deep forensic technical audit. "
    "Analyze the code for patterns of synthetic generation (LLM typicalities like overly perfect variable names, "
    "hallucinated comments, or standard 'GPT-style' logic structures).\n\n"
    "STRICT OUTPUT FORMAT:\n"
    "1. **Is this AI Content?**: [YES/NO/PARTIAL]\n"
    "2. **Forensic Probability Score (0-100%)**: [Score here]\n"
    "3. **Specific Synthetic Markers**: Identify 2-3 specific patterns or logic structures that suggest AI origin.\n"
    "4. **Dean's Verdict**: A brief, professional summary of the findings."
)

# --- 3. UI SETUP & CUSTOM HEADER ---
st.set_page_config(page_title="AI Code Checker | Zeba Academy", page_icon="🕵️")

# Custom CSS to hide the default Streamlit header/menu for a cleaner look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Custom Branding Header
st.markdown("# 🛡️ AI Code checker")
st.markdown("#### Powered by **Zeba Academy**")
st.caption("Advanced Forensic Analysis for Academic Integrity and Source Code Verification.")
st.divider()

# --- 4. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. Main Chat Logic ---
if user_input := st.chat_input("Paste code for forensic analysis..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        if len(user_input.split()) < 3 and len(user_input) < 15:
            st.markdown(user_input)
        else:
            st.code(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing code patterns..."):
            try:
                full_query = f"{SYSTEM_PROMPT}\n\nINPUT:\n{user_input}"
                response = model.generate_content(full_query)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
