from openai import OpenAI
import streamlit as st
import json

import numpy as np

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Arbitrary function to demonstrate that we can use Python code in the chat
def get_number_plus_one(number: int) -> int:
    return number + 1

# If the user has not set the model, we will use the default one
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# If the user has not set the messages, we will set the default messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    # We will add a system message to introduce the chatbot
    st.session_state.messages.append({"role": "system", "content": """
    You are a chatbot assistant named TARS.
    Always be kind, and put your humor to 60%
    """})

# We will display the messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

# We will ask the user for input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # We will send the messages to the OpenAI API
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        # If there is the word "graph" in the response, we will plot a graph
        if "graph" in response:
            st.bar_chart(np.random.randn(30, 3))

    st.session_state.messages.append({"role": "assistant", "content": response})

