import streamlit as st
import google.generativeai as genai

# Securely load key from secrets.toml
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("API Key missing! Ensure .streamlit/secrets.toml exists.")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')

SYSTEM_PROMPT = (
    "You are an expert Senior Software Engineer and Academic Integrity Officer. "
    "CASE 1: If user says 'Hello/Hi', reply politely in one sentence. "
    "CASE 2: If user provides CODE, perform a technical audit ONLY. "
    "Provide: 1. Score (0-100%), 2. 2-3 Technical Markers, 3. Brief Verdict for a Dean."
)

st.set_page_config(page_title="AI Code Forensic Lab", page_icon="🕵️")
st.title("🕵️ Code Origin Forensic Lab")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Paste code or say hello..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        # Display as code if it looks like code, otherwise text
        if " " not in user_input and len(user_input) < 10:
            st.markdown(user_input)
        else:
            st.code(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            full_query = f"{SYSTEM_PROMPT}\n\nINPUT:\n{user_input}"
            response = model.generate_content(full_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
