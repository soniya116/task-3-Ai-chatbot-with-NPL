import streamlit as st
from chatbot import get_response

# --- Page Setup ---
st.set_page_config(page_title="Smart Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Smart NLP Chatbot</h1>", unsafe_allow_html=True)

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Settings (moved out of form) ---
col1, col2 = st.columns(2)
with col1:
    rewrite_enabled = st.checkbox("Use LLM Summarizer", value=True)
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

# --- Chat History Rendering ---
st.markdown("### 💬 Chat")
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(
            f"""
            <div style='background-color:#DCF8C6;padding:10px 15px;border-radius:12px;margin-bottom:10px;
            max-width:80%;margin-left:auto;color:#000;box-shadow:1px 1px 5px rgba(0,0,0,0.1);'>
                <b>You:</b> {message}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style='background-color:#2E2E2E;padding:10px 15px;border-radius:12px;margin-bottom:10px;
            max-width:80%;margin-right:auto;color:#FFF;box-shadow:1px 1px 5px rgba(0,0,0,0.3);'>
                <b>Bot:</b> {message}
            </div>
            """, unsafe_allow_html=True)

# --- Input Form ---
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("Your message", placeholder="Ask something...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_query:
    bot_response = get_response(user_query, rewrite_enabled=rewrite_enabled)
    st.session_state.chat_history.append(("You", user_query))
    st.session_state.chat_history.append(("Bot", bot_response))
