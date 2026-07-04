import streamlit as st
import requests

st.title("Welvox Agent 🤖")

user_input = st.text_input("Apna sawal yahan likho:")

if st.button("Send"):
    # Ye raha aapka API URL
    url = "https://welvox-agent-1.onrender.com/"
    response = requests.get(url)
    
    # Ye output dikhayega
    data = response.json()
    st.write("Agent ka jawab:", data["message"])
  
