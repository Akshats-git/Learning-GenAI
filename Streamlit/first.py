import streamlit as st

st.title("My first app")
st.subheader("This is a subheader")
st.text("Welcome to your first interactive app")
st.write("Choose your variety of chai:")
chai = st.selectbox("Select your chai:", ["Masala Chai", "Ginger Chai", "Lemon Chai"])
st.write(f"You chose {chai}")
st.success("Enjoy your chai!")