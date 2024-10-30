from openai import OpenAI
import streamlit as st
import json

import numpy as np

st.title("ChatGPT with increment-1 function")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Arbitrary function to demonstrate that we can use Python code in the chat
def get_number_plus_one(number: int) -> int:
    print(f"Function called with number = {number}")
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

# Read the tools from tools.json in rootworkdir
with open("tools.json", "r") as f:
    tools = json.load(f)

# We will ask the user for input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # We will send the messages to the OpenAI API
    with st.chat_message("assistant"):
        output = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            tools=tools,
            stream=False,
        )
        # Model gives a response
        if output.choices[0].message.content:
            response = output.choices[0].message.content
            st.markdown(response)
        # Model gives a tool call
        elif output.choices[0].message.tool_calls:
            # Save the tool call as message to system
            st.session_state.messages.append({
                "role": "system", 
                "content": f"Tool call = {output.choices[0].message.tool_calls[0].function.name}, with arguments = {output.choices[0].message.tool_calls[0].function.arguments}"})
            tool_call = output.choices[0].message.tool_calls[0]
            
            if tool_call.function.name == "get_number_plus_one":
                # Transform the function arguments from str to dict
                args = json.loads(tool_call.function.arguments)
                function_output = get_number_plus_one(args["number"])
            # elif tool_call.function.name == "another_function":
            # ...
            # Save the function output as message to system
            st.session_state.messages.append({"role": "system", "content": f"Function output = {function_output}"})

            # Generate text output
            output = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
            )
            response = output.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

