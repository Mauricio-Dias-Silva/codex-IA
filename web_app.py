import streamlit as st
from codex_ia.core.agent import CodexAgent
from dotenv import load_dotenv
import os

# Load Environment
load_dotenv(override=True)

# Page Config
st.set_page_config(
    page_title="Codex-IA: Cyberpunk Edition",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for "Ostentation"
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #4a4a4a;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #1c2e4a;
        border: 1px solid #2e5a9e;
    }
    h1 {
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #00ff41;
    }
    div[data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = CodexAgent(".", auto_confirm=True)
    st.session_state.messages = []
    # Initial handshake (invisible in UI but needed for state)
    st.session_state.messages.append({"role": "assistant", "content": "Olá! Eu sou o Codex-IA. Estou pronto para codar."})

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("📂 Project Context")
    
    if st.button("Refresh Files"):
        files = st.session_state.agent.context_mgr.list_files()
        st.session_state.file_list = files
    
    if "file_list" not in st.session_state:
        st.session_state.file_list = st.session_state.agent.context_mgr.list_files()
        
    for f in st.session_state.file_list[:20]: # Limit to 20 to avoid clutter
        st.code(f, language="text")
    if len(st.session_state.file_list) > 20:
        st.write(f"... and {len(st.session_state.file_list)-20} more.")

# Main Chat Interface
st.title("🤖 Codex-IA // Terminal Mode")

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Digite sua ordem, Mestre..."):
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI Response
    with st.chat_message("assistant"):
        with st.status("Thinking...", expanded=True) as status:
            st.write("Analyzing Context...")
            response = st.session_state.agent.chat(prompt)
            status.update(label="Complete!", state="complete", expanded=False)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

