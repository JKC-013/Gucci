import streamlit as st
import os
from engine import NPCAgent, SimulationState
from personas import PERSONAS

st.set_page_config(page_title="Gucci AI Co-Worker", page_icon="👔", layout="wide")

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = "web-session-001"
    st.session_state.sim_state = SimulationState(session_id=st.session_state.session_id)
    st.session_state.messages = []
    st.session_state.agent = None

# Sidebar Configuration
st.sidebar.title("Simulation Setup")
persona_id = st.sidebar.selectbox(
    "Choose AI Co-worker:",
    options=list(PERSONAS.keys()),
    format_func=lambda x: PERSONAS[x].name
)

# Reset Button
if st.sidebar.button("Reset Simulation"):
    st.session_state.sim_state = SimulationState(session_id="web-session-002")
    st.session_state.messages = []
    st.session_state.agent = None
    st.rerun()

# Initialize Agent if needed or changed
if st.session_state.agent is None or st.session_state.agent.persona.id != persona_id:
    try:
        if not os.getenv("GEMINI_API_KEY"):
            st.error("Missing API Key! Please set GEMINI_API_KEY in .env")
        else:
            st.session_state.agent = NPCAgent(persona_id=persona_id)
            # Reset history when persona changes to keep context clean
            st.session_state.sim_state = SimulationState(session_id=st.session_state.session_id)
            st.sidebar.success(f"Connected to {PERSONAS[persona_id].name}")
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")

# Main Chat Interface
st.title("Gucci Leadership Simulation")
st.markdown(f"**Current Co-worker:** {PERSONAS[persona_id].name}")
st.markdown(f"*{PERSONAS[persona_id].style_guide}*")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Agent Response
    if st.session_state.agent:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Run Engine
                    result = st.session_state.agent.run(prompt, st.session_state.sim_state)
                    response = result["assistant_message"]
                    st.write(response)
                    
                    # Update History
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    if result.get("context_used"):
                        with st.expander("View RAG Context"):
                            st.info(result["context_used"])

                except Exception as e:
                    st.error(f"Error generating response: {e}")
