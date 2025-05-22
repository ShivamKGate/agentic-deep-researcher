import streamlit as st
from agents import run_research
from dotenv import load_dotenv
import os

load_dotenv()
LINKUP_API_KEY = os.getenv("LINKUP_API_KEY")

st.set_page_config(page_title="Agentic Deep Researcher", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

def reset_chat():
    st.session_state.messages = []

# sidebar with chat history
with st.sidebar:
    st.markdown("## 💬 Chat History")
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            role_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
            st.markdown(f"{role_icon} **{message['role'].capitalize()}**: {message['content'][:60]}{'...' if len(message['content']) > 60 else ''}")
    else:
        st.info("No messages yet. Start chatting!")

# main chat interface header
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("<h2 style='color: #0066cc;'>Agentic Deep Researcher.</h2>", unsafe_allow_html=True)
    powered_by_html = """
    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
        <span style='font-size: 20px; color: #666;'>Powered by Agents with Internet Search.</span>
    </div>
    """
    st.markdown(powered_by_html, unsafe_allow_html=True)
with col2:
    st.button("Clear ↺", on_click=reset_chat)
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# displaying the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# accepting the user input and processing the research query
if prompt := st.chat_input("Ask to research about any topic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # finalizing whether the API key is set
    if not LINKUP_API_KEY:
        response = "API Key not found. Please set it in a `.env` file."
    else:
        os.environ["LINKUP_API_KEY"] = LINKUP_API_KEY
        with st.spinner("Researching... This may take a moment..."):
            try:
                result = run_research(prompt)
                response = result
            except Exception as e:
                response = f"An error occurred: {str(e)}"

    # displaying the response from the agent
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
