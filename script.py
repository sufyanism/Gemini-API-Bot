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
    "Analyze the following code for patterns of synthetic generation (LLM typicalities "
    "like overly perfect variable names, hallucinated comments, or standard 'GPT-style' "
    "logic structures).\n\n"
    "STRICT OUTPUT FORMAT:\n"
    "1. **Is this AI Content?**: [YES/NO/PARTIAL]\n"
    "2. **Probability Score (0-100%)**: (Where 100% is definitely AI-generated)\n"
    "3. **Specific Synthetic Markers**: Re-display the suspicious parts of the code and wrap them in: "
    "<mark style='background-color: #FFFF00; color: black; padding: 2px; border-radius: 3px;'>CODE_HERE</mark>. "
    "Provide a technical explanation for each marker.\n"
    "4. **Final Verdict**: A clear summary of how much of the code is likely AI-generated."
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
