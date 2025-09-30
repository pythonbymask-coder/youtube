import streamlit as st
import requests

API_URL = "https://coud-chemosynthetic-floy.ngrok-free.dev/generate" 
HEADERS = {"Authorization": "Bearer yj0pg3nRQLlFbu2LBRRBtt2pZGnTtLqDu3aswphj4t4"}

def query_api(prompt):
    r = requests.post(API_URL, json={"input": prompt}, headers=HEADERS, timeout=360)
    return r.json().get("text", "error")



st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot with Streamlit")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message, reply in st.session_state.messages:
    with st.chat_message("user"):
        st.markdown(message)
    with st.chat_message("assistant"):
        st.markdown(reply)

# User input box
if prompt := st.chat_input("Type your message..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    reply = query_api(prompt)

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save history
    st.session_state.messages.append((prompt, reply))

