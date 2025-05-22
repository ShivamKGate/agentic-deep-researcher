import streamlit as st
from agents import run_research
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("LINKUP_API_KEY")

st.title("Agentic Deep Researcher")

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.text_input("Enter your query")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    response = run_research(query)
    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    st.markdown(f"**{msg['role']}**: {msg['content']}")