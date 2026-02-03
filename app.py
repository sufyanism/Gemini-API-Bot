import streamlit as st
import google.generativeai as genai

# --- 1. Backend Configuration ---
# Replace with your actual key or use st.secrets for safety
genai.configure(api_key="AIzaSyDgeR51HDkoz3I3NIypOuyoAAKEQiLf-d0")
model = genai.GenerativeModel('gemini-2.5-flash')

# The "Hidden" Expert System Prompt
# The "Deep-Code" Forensic System Prompt
SYSTEM_PROMPT = (
    "You are an expert Senior Software Engineer and Academic Integrity Officer. "
    "Your response behavior depends on the user input:\n\n"
    "CASE 1: If the user says 'Hello', 'Hi', or similar greetings: "
    "Reply with a single, polite sentence acknowledging them and inviting code submission.\n\n"
    "CASE 2: If the user provides CODE: "
    "Perform a technical audit ONLY. Ignore all natural language text or student explanations. "
    "Provide a BRIEF report using this exact structure:\n"
    "1. Score: [0-100%]\n"
    "2. Markers: [Bullet list of 2-3 key technical synthetic patterns]\n"
    "3. Verdict: [One-sentence formal conclusion for a Dean]\n\n"
    "Strictly avoid conversational filler when analyzing code."
)

# --- 2. Streamlit UI Design ---
st.set_page_config(page_title="AI Code Forensic Lab", page_icon="🕵️")

st.title("🕵️ Code Origin Forensic Lab")
st.caption("Submit code snippets to check for synthetic (LLM) generation patterns.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. The AI Interaction ---
if user_code := st.chat_input("Paste the code you wish to analyze..."):
    
    # Display user code in chat
    st.session_state.messages.append({"role": "user", "content": user_code})
    with st.chat_message("user"):
        st.code(user_code, language="python")

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Conducting forensic audit..."):
            # Combine the expert persona with the user's specific code
            full_query = f"{SYSTEM_PROMPT}\n\nUSER CODE TO ANALYZE:\n{user_code}"
            
            try:
                response = model.generate_content(full_query)
                analysis_result = response.text
                
                st.markdown(analysis_result)
                st.session_state.messages.append({"role": "assistant", "content": analysis_result})
                
            except Exception as e:
                st.error(f"An error occurred with the Gemini API: {e}")