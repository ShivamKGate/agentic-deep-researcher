import streamlit as st
from agents import run_research

st.title("Agentic Deep Researcher")
query = st.text_input("Enter your query")
if query:
    response = run_research(query)
    st.write(response)
