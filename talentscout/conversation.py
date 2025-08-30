# Conversation flow management
"""
Utilities for managing conversation and session state inside Streamlit.
"""

from typing import Dict, Any, List
import streamlit as st

END_KEYWORDS = {"quit", "exit", "done", "bye", "thank you", "thanks"}

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # list of (role, text)
    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = {}
    if "generated_questions" not in st.session_state:
        st.session_state.generated_questions = {}
    if "conversation_active" not in st.session_state:
        st.session_state.conversation_active = True

def add_message(role: str, text: str):
    st.session_state.messages.append((role, text))

def is_end_message(user_text: str) -> bool:
    ut = user_text.strip().lower()
    return ut in END_KEYWORDS

def reset_conversation():
    st.session_state.messages = []
    st.session_state.candidate_info = {}
    st.session_state.generated_questions = {}
    st.session_state.conversation_active = True
