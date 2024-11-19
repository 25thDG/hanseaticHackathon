import streamlit as st

st.title("Hello World")

# Create a text input for the user's name
name = st.text_input("Enter your name:")

# Create a button to trigger the greeting
button_clicked = st.button("Send")

# If the button is clicked,
# display a greeting
if button_clicked:
    st.write(f"Hello {name}!")
    st.balloons()

# start with `streamlit run hello_world.py`