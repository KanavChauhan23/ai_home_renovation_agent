import streamlit as st
from google import genai

# Initialize client
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="AI Home Renovation", layout="wide")

st.title("🏠 AI Home Renovation Planner")
st.write("Ask me about renovating your home!")

user_input = st.text_input("Enter your question:")

if st.button("Submit"):

    if not user_input.strip():
        st.warning("Please enter a question.")
        st.stop()

    st.write("Processing...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )

        st.success("Response:")
        st.write(response.text)

    except Exception as e:
        st.error("API Error:")
        st.code(str(e))
