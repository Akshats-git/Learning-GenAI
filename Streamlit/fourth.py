import streamlit as st
import pandas as pd

st.title("Chai Sales Dashboard")

file = st.file_uploader("Upload your csv file",type=["csv"])
if file:
    df = pd.read_csv(file)
    st.subheader("Data Preview")
    st.dataframe(df)
    st.subheader("Summary Stats")
    st.write(df.describe())