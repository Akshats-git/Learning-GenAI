from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt

load_dotenv()

st.header("Research Tool")

paper_input = st.selectbox("Select a paper", ["Attention is All you need","BERT"])
style_input = st.selectbox("Select a style", ["Beginner", "Technical","Mathematical","Code-Oriented"])
length_input = st.selectbox("Select a length", ["Short", "Medium", "Long"])

template = load_prompt('template.json')

model = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

if st.button("Summarize"):
    chain = template | model
    result = chain.invoke({
        "paper_input": paper_input,
        "style_input": style_input,
        "length_input": length_input
    })
    st.write(result.content)