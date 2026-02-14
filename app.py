import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Home Renovation", layout="wide", page_icon="🏠")

st.title("🏠 AI Home Renovation Planner")
st.markdown("Plan your renovation smartly using AI (FREE version)")

st.markdown("""
### 💡 Try These Examples:
- Kitchen renovation ideas under $5,000
- Modern bedroom makeover with minimalist design
- Small bathroom upgrade suggestions
- Living room renovation with eco-friendly materials
- Budget-friendly home office setup ideas
""")

st.markdown("---")

user_input = st.text_input(
    "Enter your renovation question:",
    placeholder="e.g., I want to renovate my kitchen with a $3000 budget"
)

if st.button("🚀 Generate Renovation Plan", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter a question first.")
        st.stop()
    
    with st.spinner("🤖 AI is planning your renovation..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful home renovation expert. Provide practical, budget-conscious renovation advice with specific suggestions."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            st.success("✅ Renovation Plan Generated!")
            
            st.markdown("### 📋 Your Renovation Plan")
            with st.container():
                st.write(response.choices[0].message.content)
            
            st.markdown("---")
            st.info("💡 **Tip:** Save this plan and consult with a professional contractor before starting work!")
            
        except Exception as e:
            st.error("❌ Oops! Something went wrong:")
            st.code(str(e))
            st.info("💡 Try again or check your API key in settings.")

with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. Enter your renovation question
    2. Include room type and budget
    3. Click 'Generate Plan'
    4. Get AI suggestions!
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 What You Can Ask")
    st.markdown("""
    - Design ideas
    - Budget estimates
    - Material suggestions
    - DIY vs professional advice
    - Timeline planning
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Powered By")
    st.markdown("OpenAI GPT-3.5 Turbo")

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ by Kanav Chauhan | 
    <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
    <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a>
    </p>
</div>
""", unsafe_allow_html=True)
