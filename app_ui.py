import streamlit as st
import google.generativeai as genai
import os

# Page setup for clean White Theme
st.set_page_config(page_title="Welvox Agent", layout="wide")

# Custom CSS for Claude look
st.markdown("""
    <style>
    .stApp {background-color: #ffffff; color: #000000;}
    [data-testid="stSidebar"] {background-color: #f7f7f5; border-right: 1px solid #e5e5e5;}
    .stChatInput {border: 1px solid #d1d1d1; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# 1. Sidebar Section
with st.sidebar:
    st.title("Welvox Agent")
    st.write("---")
    st.info("System Status: Online")
    if st.button("Reset Chat"):
        st.session_state.messages = []

# 2. Main Chat Section
st.title("Welcome to Welvox")
st.subheader("How can I help you today?")

# Gemini Logic - API Key environment variable se lega
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Message Welvox..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.error("API Key nahi mili! Render settings mein 'GEMINI_API_KEY' add karo.")

# 3. Footer Metrics
st.write("---")
col1, col2, col3 = st.columns(3)
col1.metric("Model", "Gemini Pro")
col2.metric("Theme", "Claude-Style")
col3.metric("Status", "Stable")
