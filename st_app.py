"""This module chatbot interface where users can ask their questions. It is the
main file of this project.
"""

__file__ = "st_app.py"
__version__ = "0.1"
__author__ = "Martin Brossard"
__copyright__ = "Copyright (C) 2025 Martin Brossard"
__license__ = "Apache 2.0"

import streamlit as st
import rag

# Title and note field
st.title("Prototype chatbot for querying library data ")
st.caption("Note that this is a demo app.")


def init_chat_history():
    """Initialize the chat history. Support the history reset."""
    if "messages" not in st.session_state: 
        st.session_state.messages = [
            {"role": "system", "content": "Hello, how can I help you?"}
            ]     
    if st.button("Chat zurücksetzen"):
        rag.chat_history.clear()
        st.session_state.messages = []
        st.success("Chatverlauf wurde zurückgesetzt.")


def start_chat():
    '''Display the chat messages from history on app rerun with the
    corresponding role. Write down the new answer on the interface and secure it
    to the history'''
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Chatbot"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
            )
        with st.chat_message("user"):
            st.markdown(prompt)

        response = rag.query(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
                )

if __name__ == "__main__":
    init_chat_history()
    start_chat()

