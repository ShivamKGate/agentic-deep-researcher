import streamlit as st
from agents import run_research
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("LINKUP_API_KEY")

st.title("Agentic Deep Researcher")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input("Ask a question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    if not API_KEY:
        response = "API key missing. Please set LINKUP_API_KEY in your .env file."
    else:
        response = run_research(prompt)        
    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
