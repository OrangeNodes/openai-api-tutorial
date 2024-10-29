# OpenAI API tutorial
This repo contains first steps of setting up your own OpenAI ChatGPT functionalities. 
It will give you a better understanding of how to ChatGPT works, and how you can integrate a chatbot in your own environment. 

## Usage
First, create a virtual environment and install the requirements:
```bash
conda create -n openai python=3.8
conda activate openai
pip install -r requirements.txt
```

Then, create a `./.streamlit/secrets.toml` file with your OpenAI API key:
If you are following a physical workshop, you will get this from your trainer. 

```toml
OPENAI_API_KEY = "xxx"
```

Finally, run the Streamlit app:
```bash
streamlit run chat.py
```

## Extra references
This repo is based on the tutorial which can be found over here: [link](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps).


