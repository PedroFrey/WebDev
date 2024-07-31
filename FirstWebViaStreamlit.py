import streamlit as st

""""
On a CMD prompt i need the folowing code to run this Site
python -m streamlit run FirstWeb.py
"""

#Initial config of page

st.set_page_config(page_title="My First Web Page!", page_icon=":tada:",layout="wide")

#Header section

st.subheader("Hello! I'm a developer")
st.title("I Develop data visuals using PowerBI")
st.write("There are many other thing that I enjoy")
st.write("[Learn More>](https://www.google.com.br)")