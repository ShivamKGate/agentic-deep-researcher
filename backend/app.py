import streamlit as st

st.title("Agentic Deep Researcher")
query = st.text_input("Enter your query")
if query:
    st.write(f"You asked: {query}")
