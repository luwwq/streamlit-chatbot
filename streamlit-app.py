import streamlit as st
from langchain_community.llms import Ollama
import pandas as pd

llm = Ollama(model="llama2")

st.title("Data Analysis with PandasAI")

uploader_file = st.file_uploader("Upload a CSV file", type= ["csv"])

if uploader_file is not None:
    data = pd.read_csv(uploader_file)
    st.write(data.head(3))