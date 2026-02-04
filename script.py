import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- 1. API Configuration (Hybrid Logic) ---
load_dotenv()  # Load local .env file if it exists

# Check Streamlit Secrets first (for Cloud), then Environment Variables (for Local)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🔑 API Key not found! Please set GEMINI_API_KEY in .env or Streamlit Secrets.")
    st.stop()

# Use 'gemini-1.5-flash' for stable performance
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. System Prompt & UI Setup ---
SYSTEM_PROMPT = (
    "You are an expert Senior Software Engineer and Academic Integrity Officer. "
    "CASE 1: If the user says 'Hello' or 'Hi', reply politely in exactly one sentence. "
    "CASE 2: If the user provides CODE, perform a deep forensic technical audit. "
    "Analyze the code for patterns of synthetic generation (LLM typicalities like overly perfect variable names, "
    "hallucinated comments, or standard 'GPT-style' logic structures). "
    "Your output must follow this format:\n\n"
    "1. **Forensic Probability Score (0-100%)**: (Where 100% is definitely AI-generated)\n"
    "2. **Specific Synthetic Markers**: (Identify 2-3 specific lines or patterns that suggest AI origin)\n"
    "3. **Dean's Verdict**: (A brief, professional summary of whether the code is AI-generated, human-written, or a hybrid.)"
)

st.set_page_config(page_title="AI Code Forensic Lab", page_icon="🕵️")
st.title("🕵️ Code Origin Forensic Lab")

# --- 3. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Main Chat Logic ---
if user_input := st.chat_input("Paste code or say hello..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        # Display as code if it looks like code, otherwise text
        if len(user_input.split()) < 3 and len(user_input) < 15:
            st.markdown(user_input)
        else:
            st.code(user_input)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing forensics..."):
            try:
                full_query = f"{SYSTEM_PROMPT}\n\nINPUT:\n{user_input}"
                response = model.generate_content(full_query)
                
                # Render and save response
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
