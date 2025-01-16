import streamlit as st
import requests
import uuid
from datetime import datetime

# Base URL for FastAPI
# API_BASE_URL = st.secrets("API_BASE_URL")
API_BASE_URL = "http://localhost:8081/crustdata"
st.set_page_config(page_title="Crustdata API Buddy", page_icon="🤖")

def create_new_session():
    """Create a new session ID and initialize session state"""
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id
    st.session_state.messages = []
    if 'active_sessions' not in st.session_state:
        st.session_state.active_sessions = {}
    st.session_state.active_sessions[session_id] = {
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'messages': 0
    }
    return session_id

def load_chat_history(session_id):
    """Load chat history for a given session ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/retrieve_chat_history/{session_id}")
        if response.status_code == 200:
            history = response.json()["history"]
            st.session_state.messages = []
            for msg in history:
                if "Human" in msg:
                    st.session_state.messages.append({"role": "user", "content": msg["Human"]})
                elif "AI" in msg:
                    st.session_state.messages.append({"role": "assistant", "content": msg["AI"]})
            return True
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load chat history: {e}")
        return False

def delete_session(session_id):
    """Delete a session and its chat history"""
    try:
        response = requests.delete(f"{API_BASE_URL}/delete_chat_history/{session_id}")
        if response.status_code == 200:
            if session_id in st.session_state.active_sessions:
                del st.session_state.active_sessions[session_id]
            st.success("Session deleted successfully!")
            return True
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete session: {e}")
        return False

def switch_session(session_id):
    """Switch to a different session"""
    if load_chat_history(session_id):
        st.session_state.session_id = session_id
        return True
    return False

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_sessions" not in st.session_state:
    st.session_state.active_sessions = {}

st.title("Crustdata API Buddy 🤖")
st.caption("🚀 Powered by FastAPI and Chroma")

# Sidebar for session management and settings
with st.sidebar:
    st.markdown("## Session Management")
    
    # New session button
    if st.button("Create New Session", key="new_session"):
        new_session_id = create_new_session()
        st.success(f"New session created! ID: {new_session_id}")

    # Display available sessions
    st.markdown("### Available Sessions")
    if st.session_state.active_sessions:
        for session_id, session_info in st.session_state.active_sessions.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                session_button = st.button(
                    f"Session {session_id[:8]}...",
                    key=f"session_{session_id}",
                    help=f"Created: {session_info['created_at']}"
                )
                if session_button:
                    switch_session(session_id)
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{session_id}", help="Delete session"):
                    if delete_session(session_id):
                        if session_id == st.session_state.session_id:
                            st.session_state.session_id = None
                            st.session_state.messages = []
                        st.rerun()
            
            with col3:
                if session_id == st.session_state.session_id:
                    st.markdown("✓ Active")

    else:
        st.info("No active sessions")

    st.divider()
    st.markdown("## How to use\n"
                "1. Create a new chat session\n"
                "2. Ask questions about the API documentation\n"
                "3. View chat history in the main window\n"
                "4. Switch between or delete sessions as needed")

# Main chat interface
if st.session_state.session_id is None:
    st.info("Please create a new session to start chatting!")
else:
    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_prompt = st.chat_input("Ask something about the API documentation")

    if user_prompt:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)
        
        # Update session message count
        st.session_state.active_sessions[st.session_state.session_id]['messages'] += 1

        # Get response from API
        with st.spinner("Thinking... 🤔"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/query/{st.session_state.session_id}",
                    params={"query": user_prompt}
                )
                response.raise_for_status()
                result = response.json()
                
                if "response" in result:
                    bot_response = result["response"]
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.chat_message("assistant").write(bot_response)
                else:
                    st.error("No response received from the server")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"Error during query: {e}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")