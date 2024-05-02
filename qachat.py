# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:15:15 2024

@author: chuhuivoon
"""

#%%
# Pre-requisite 

# pip install streamlit
# pip3 install streamlit-extras
# pip install htbuilder

# To run the app use: streamlit run xxx.py
# To run the app while setting the base to dark use: streamli run xxx.py --theme.base='dark' 



#%%
# Imports 

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
from dotenv import load_dotenv
from typing import Optional


import logging
import sys
import time
import requests
import streamlit as st
import os
import pandas as pd
import tempfile


st.set_page_config(
    page_title=None,
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)



log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)



BASE_API_URL = "http://127.0.0.1:7860/api/v1/process"
FLOW_ID = "1a0e4633-c9d2-483f-ae0e-266d5c1f2ad0"

TWEAKS = {
  "PythonFunctionTool-ZaId1": {},
  "CSVAgent-N3azz": {},
  "AgentInitializer-CtDqy": {},
  "Calculator-SBo02": {},
  "CSVLoader-NeUdD": {},
  "Document-fvSCR": {},
  "OpenAIEmbeddings-DcHiB": {},
  "Chroma-krH0r": {},
  "CombineDocsChain-T4sIX": {},
  "ChatOpenAI-l98D8": {},
  "RetrievalQA-RZH8I": {}
}





load_dotenv()

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"
    payload = {"inputs": inputs}
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload)
    return response.json()

def generate_response(query, csv_filepath):
    logging.info(f"input: {query}, CSV_file_path={csv_filepath}")
    inputs = {"query": query, "CSV_file_path": csv_filepath}

    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    
    try:
        result = response.get("result", {})
        if "result" in result:
            result_text = result["result"]
            logging.info(f"answer: {result_text}")
            return result_text
        else:
            logging.error(f"Unexpected response format: {response}")
            return "Sorry, there was a problem finding an answer for you."
    except Exception as exc:
        logging.error(f"error: {exc}")
        return "Sorry, there was a problem finding an answer for you."
    




with st.sidebar:
    #st.image('msf-logo-2021.png', width=256, use_column_width="auto")
    st.title('🤗💬 MSF ChatBot')
    st.markdown('''
    ## Upload the file.
                
    ''')


    # Upload a CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type= ["csv"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            csv_filepath = tmp_file.name
        df = pd.read_csv(csv_filepath)
        st.success("File uploaded successfully!")
    else:
        st.warning("Please upload a CSV file.")


# main chatbox
def main(): 
    st.header("Welcome to MSF Chatbot! 🤖")
    st.markdown(''' :rainbow[Chat Application powered by Langflow] 🚀''')
    st.markdown(" ##### You may ask me information on GenAI training programs 📚📖📝 ")
    # st.markdown(""" <style>
    #     .reportview-container {
    #         margin-top: -2em; 
    #     }
    #     #MainMenu {visibility:hidden;}
    #     .stDeployButton {display:none;}
    #     footer {visibility: hidden;}
    #     #stDecoration {display:none;}
    # </style>""", unsafe_allow_html=True)


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if query := st.chat_input("You may start with what are the programs offered in MSF?"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",  # Emoji representation for user
            }
        )
        with st.chat_message(
            "user",
            avatar="💬",  # Emoji representation for user
        ):
            st.write(query)

        with st.chat_message(
            "assistant",
            avatar="🤖",  # Emoji representation for assistant
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(query, csv_filepath)
                message_placeholder.write(assistant_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji representation for assistant
            }
        )
        


if __name__ == "__main__":
    main()  # main function execution
