import streamlit as st

st.title("Chai taste poll")

col1,col2 = st.columns(2)
with col1:
    st.header("Masala Chai")
    vote1 = st.button("Vote for Masala Chai")

with col2:
    st.header("Ginger Chai")
    vote2 = st.button("Vote for Ginger Chai")

if vote1:
    st.success("Thanks for voting Masala Chai!")

if vote2:
    st.success("Thanks for voting Ginger Chai!")

name = st.sidebar.text_input("Enter your name")
tea = st.sidebar.selectbox("Select your favourite tea",["Masala","Kesar","Adrak"])
st.sidebar.write(f"Hello {name}, you like {tea} tea!")

with st.expander("Show Chai making instructions"):
    st.write("""
    1. Boil water
    2. Add tea leaves
    3. Add spices
    4. Add milk and sugar
    5. Strain and serve hot
    """)

st.markdown('### Enjoy your chai!')
st.markdown('> Blockquote ')