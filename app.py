import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page config
st.set_page_config(
    page_title="RoomGenie - AI Renovation Planner", 
    layout="wide", 
    page_icon="🧞‍♂️"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tagline {
        text-align: center;
        color: #888;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.8rem;
        border: none;
        border-radius: 12px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧞‍♂️ RoomGenie</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Renovation Planning</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">"Professional renovation plans in seconds"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., I want to renovate my kitchen with ₹50,000 budget. Modern white design with wooden countertops and brass hardware.",
    height=120,
    help="Be specific! Include: room type, budget, style preferences, colors, materials"
)

# Examples in expander
with st.expander("💡 See Example Prompts"):
    col1, col2 = st.columns(2)
    with col1:
        st.code("""
"Modern bedroom, ₹30,000,
minimalist white & light wood,
need good storage solutions"
        """, language=None)
        st.code("""
"Cozy living room, ₹45,000,
warm earthy tones, lots of plants,
comfortable seating for family"
        """, language=None)
    with col2:
        st.code("""
"Small bathroom, ₹25,000,
clean white tiles, chrome fixtures,
maximize storage space"
        """, language=None)
        st.code("""
"Home office, ₹40,000,
productivity-focused, good lighting,
ergonomic furniture, cable management"
        """, language=None)

# Generate button
if st.button("🚀 Generate My Dream Room Plan", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    with st.spinner("🧞‍♂️ RoomGenie is working its magic..."):
        try:
            system_prompt = """You are RoomGenie, an expert AI interior designer with 20 years of experience. You create detailed, practical, and inspiring renovation plans that are realistic and budget-conscious.

Your plans should be:
- Professional yet approachable
- Specific with costs and materials
- Realistic and achievable
- Inspiring and creative
- Well-organized and easy to follow

Always provide actionable advice that the user can actually implement."""

            user_prompt = f"""{user_input}

Create a comprehensive, professional renovation plan with these sections:

# 1. Project Overview
- Brief summary of the renovation
- Total budget allocation
- Estimated timeline

# 2. Design Vision & Concept
- Overall design style and theme (e.g., Scandinavian minimalist, modern industrial, rustic farmhouse)
- **Color Palette**: Primary, secondary, and accent colors with specific names (e.g., "Soft White (#F8F8F8)", "Warm Oak", "Sage Green (#B2C2A1)")
- **Key Materials**: Wood types, metal finishes, fabric textures, flooring materials
- **Atmosphere & Mood**: What feeling the space should evoke
- **Focal Points**: Main design features that draw the eye

# 3. Detailed Budget Breakdown
Break down the budget into specific categories with realistic costs:

**Paint & Wall Treatment**: ₹X,XXX
- Paint (brand, color, quantity)
- Primer and supplies
- Labor if needed

**Flooring**: ₹X,XXX
- Material type and quantity
- Installation costs

**Lighting**: ₹X,XXX
- Ceiling fixtures (specific type)
- Task lighting
- Ambient lighting

**Furniture**: ₹X,XXX
(List each piece with approximate cost)
- Main furniture items
- Storage solutions

**Fixtures & Hardware**: ₹X,XXX
- Door handles, drawer pulls
- Bathroom/kitchen fixtures

**Decor & Accessories**: ₹X,XXX
- Artwork
- Plants
- Textiles (curtains, rugs, cushions)

**Labor/Installation**: ₹X,XXX

**Contingency (10%)**: ₹X,XXX

**TOTAL**: ₹X,XXX

# 4. Implementation Timeline

**Week 1: Planning & Preparation**
- Finalize design choices
- Order materials with long lead times
- Clear and prep the space

**Week 2: Core Updates**
- Painting and wall treatments
- Flooring installation
- Major electrical work

**Week 3: Installation Phase**
- Furniture assembly and placement
- Fixture installation
- Lighting setup

**Week 4: Finishing Touches**
- Decor placement
- Final adjustments
- Styling and organization

# 5. Shopping List
Organize items by priority:

**Must-Haves** (essential items)
**Nice-to-Haves** (if budget allows)
**Future Upgrades** (for later)

# 6. Pro Tips & Recommendations
- Where to save money without compromising quality
- Brands or stores for best value
- DIY vs professional work guidance
- Maintenance and care advice

# 7. Visual Inspiration Keywords
(For the user to search online or use with AI image generators)
List 10-15 descriptive keywords/phrases that capture the final look, like:
"Scandinavian white oak bedroom", "minimalist floating nightstands", "soft gray linen bedding", etc.

Make the plan inspiring yet practical, detailed yet easy to follow!"""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=3500
            )
            
            plan = response.choices[0].message.content
            
            # Display results
            st.success("✅ Your Professional Renovation Plan is Ready!")
            st.markdown("---")
            
            # Display the plan
            st.markdown(plan)
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("💡 **Next Steps**\n\n1. Save this plan\n2. Get contractor quotes\n3. Start shopping!\n4. Execute your vision!")
            
            with col2:
                st.info("🎨 **Visualize It**\n\nUse the keywords in Section 7 with:\n- Pinterest searches\n- AI image tools\n- Interior design apps")
            
            with col3:
                st.info("📱 **Share It**\n\nShow this plan to:\n- Contractors\n- Interior designers\n- Family/friends\n- Get feedback!")
            
        except Exception as e:
            st.error(f"❌ Error generating plan: {str(e)}")
            st.info("Please check your internet connection and try again.")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    **RoomGenie** is your AI-powered renovation assistant. Get professional-quality renovation plans instantly!
    
    **What you get:**
    - ✅ Detailed design concepts
    - ✅ Complete budget breakdowns
    - ✅ Week-by-week timelines
    - ✅ Shopping lists
    - ✅ Pro tips & advice
    
    **100% FREE • Unlimited Use**
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Success Tips")
    st.markdown("""
    **Be specific!** Include:
    - 🏠 Room type
    - 💰 Budget amount
    - 🎨 Style preferences
    - 🔧 Special requirements
    
    **The more details you provide, the better your plan will be!**
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Powered By")
    st.markdown("""
    **AI Model**: Groq (Llama 3.3 70B)
    
    🟢 **Status**: Active
    
    Ultra-fast response times with professional-quality plans.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Perfect For")
    st.markdown("""
    - Homeowners planning renovations
    - Interior design students
    - Real estate professionals
    - DIY enthusiasts
    - Budget-conscious renovators
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>✨ Built with ❤️ by Kanav Chauhan ✨</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
        <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a> |
        <a href='https://www.linkedin.com/in/kanavchauhan23' target='_blank'>LinkedIn</a>
    </p>
    <p style='font-size: 12px; margin-top: 10px;'>
        🧞‍♂️ RoomGenie - Professional Renovation Planning Made Easy
    </p>
</div>
""", unsafe_allow_html=True)
