import streamlit as st
import google.generativeai as genai
import os

# Configure API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI Home Renovation", layout="wide")

st.title("🏠 AI Home Renovation Planner")
st.write("Ask me about renovating your home!")

user_input = st.text_input("Enter your question:")

if st.button("Submit"):
    if user_input:
        st.write("Processing...")

        try:
            response = model.generate_content(user_input)
            st.success("Response:")
            st.write(response.text)

        except Exception as e:
            st.error("Error occurred:")
            st.write(e)

    else:
        st.warning("Please enter a question.")
