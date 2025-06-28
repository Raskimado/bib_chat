import streamlit as st
from rag import query

#Title field
st.title("Streamlit with LangChain!")

#Note field
st.caption("Note that this is a demo app.")

# Initialize chat history
# session_state saves data from previous runs from the same session
def init_chat_history():
    if "messages" not in st.session_state: 
        st.session_state.messages = [{"role": "system", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
# chat_message looks for corresponding role
# markdown writes the history down
def start_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Chatbot"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        #Call function query() from rag.py
        response = query(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    init_chat_history()
    start_chat()
