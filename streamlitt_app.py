# -*- coding: utf-8 -*-
"""Streamlitt App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Apam84ca1w1J4DXapgiNhGhv3RAQiFfn
"""

import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="Enhanced Chatbot")

# Sidebar content
with st.sidebar:
    st.title('Enhanced Chatbot')
    st.write('Ask your finance-related queries here')
    ngrok_url = st.text_input('Enter the full URL', value="http://localhost:5000")

if not ngrok_url:
    st.warning('Please enter the full URL for ngrok', icon='⚠️')

# Function to generate response
def generate_response(prompt_input):
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt_input}
    response = requests.post(f"{ngrok_url}/generate", headers=headers, data=json.dumps(payload))
    try:
        response_json = response.json()
        return response_json['generated_text']
    except json.JSONDecodeError:
        st.error("Error decoding JSON response")
        st.write("Response text:", response.text)
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request: {str(e)}")
        return None

# Initialize chat messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Type your question here"}]

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history function
def clear_chat_history():
    st.session_state.chat_history = [{"role": "assistant", "content": "How may I assist you?"}]

# Sidebar button to clear chat history
st.sidebar.button('Clear History', on_click=clear_chat_history)

# Input field for the prompt
if user_input := st.chat_input("Enter your message:", disabled=not ngrok_url):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

# Generate response if the last message is from the user
if st.session_state.chat_history[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(user_input)
            if response:
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})