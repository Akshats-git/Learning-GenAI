import streamlit as st
st.title("Chai Maker App")
if st.button("Make Chai"):
    st.success("Your chai is being brewed!")

add_masala = st.checkbox("Add masala")

if add_masala:
    st.write("Masala added to your chai.")

tea_type = st.radio("Choose your tea type:", ("Black Tea", "Green Tea", "Herbal Tea"))
flavour = st.selectbox("Select a flavour:", ["Ginger", "Cardamom", "Lemon", "Mint"])
sugar = st.slider("Select sugar level (in tsp):", 0, 5, 2)
cups = st.number_input("Number of cups:", min_value=1,max_value=10, value=1, step=1)

name = st.text_input("Enter your name: ")
if name:
    st.write(f"Hello, Welcome {name}!")

dob = st.date_input("Select your date of birth:")
