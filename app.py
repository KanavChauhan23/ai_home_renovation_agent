import streamlit as st
from agent import root_agent

st.set_page_config(page_title="AI Home Renovation", layout="wide")

st.title("🏠 AI Home Renovation Planner")

st.write("Ask me about renovating your home!")

user_input = st.text_input("Enter your question:")

if st.button("Submit"):
    if user_input:
        st.write("Processing...")
        response = root_agent.run(user_input)
        st.success("Response:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
