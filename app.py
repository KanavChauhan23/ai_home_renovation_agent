import streamlit as st
from groq import Groq
import urllib.parse

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
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧞‍♂️ RoomGenie</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Renovation Planning & Visualization</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">"Professional renovation plans with AI-generated visuals"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., Modern kitchen, ₹50,000 budget, white cabinets, marble countertops, brass fixtures, pendant lights",
    height=120,
    help="Include: room type, budget, colors, materials, style"
)

# Generate button
if st.button("🚀 Generate My Dream Room", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    # Progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Two columns
    plan_col, image_col = st.columns([1.2, 1])
    
    # Generate plan
    with plan_col:
        status_text.text("🧞‍♂️ Creating renovation plan...")
        progress_bar.progress(20)
        
        try:
            system_prompt = """You are RoomGenie, an expert interior designer. Create detailed, practical renovation plans."""

            user_prompt = f"""{user_input}

Create a comprehensive renovation plan with:

## 1. Design Vision
- Style and theme
- **Color Palette** (specific colors with hex codes)
- **Key Materials** (wood types, metals, fabrics)
- Mood and atmosphere

## 2. Budget Breakdown
Itemized costs totaling the budget

## 3. Timeline
Week-by-week schedule (4 weeks)

## 4. Visual Description
Write ONE detailed paragraph (100-150 words) describing the finished room. Include:
- Exact colors of walls, furniture, accents
- All furniture pieces and materials
- Lighting (natural and artificial)
- Layout and spatial feel
- Textures and finishes
- Overall atmosphere

Make it vivid and photorealistic!"""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2500
            )
            
            plan = response.choices[0].message.content
            progress_bar.progress(50)
            
            st.success("✅ Renovation Plan Ready!")
            st.markdown(plan)
            
            # Extract visual description for image
            visual_desc = ""
            if "visual description" in plan.lower():
                lines = plan.split('\n')
                capture = False
                for line in lines:
                    if "visual description" in line.lower():
                        capture = True
                        continue
                    if capture and line.strip():
                        if line.strip().startswith('#'):
                            break
                        visual_desc += line.strip() + " "
                        if len(visual_desc) > 300:
                            break
            
            if len(visual_desc) < 50:
                visual_desc = user_input[:250]
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            st.stop()
    
    # Generate and display image
    with image_col:
        status_text.text("🎨 Generating visualization...")
        progress_bar.progress(70)
        
        try:
            # Create enhanced prompt for image
            image_prompt = f"professional interior design photography, {visual_desc.strip()}, high quality, well lit, modern, clean, architectural photography, magazine quality"
            
            # Encode for URL
            encoded_prompt = urllib.parse.quote(image_prompt[:500])
            
            # Generate Pollinations URL
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&model=flux&enhance=true"
            
            progress_bar.progress(100)
            status_text.empty()
            
            st.success("✅ Visualization Generated!")
            
            # Display image directly from URL
            st.image(image_url, caption="Your Dream Room (AI-Generated)", use_container_width=True)
            
            # Provide direct link as backup
            st.markdown(f"[🔗 Open full image in new tab]({image_url})")
            
            # Info about downloading
            st.caption("💡 Right-click the image above and select 'Save image as...' to download")
            
        except Exception as e:
            st.error(f"Image error: {str(e)}")
            st.info("Your renovation plan is ready above!")
    
    progress_bar.empty()
    
    st.markdown("---")
    st.info("💡 **Tip**: Screenshot or bookmark this page to save your plan and visualization!")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    AI-powered renovation planning with instant visualizations!
    
    **Features:**
    - 📋 Detailed design plans
    - 💰 Budget breakdowns
    - 📅 Timelines
    - 🎨 AI-generated images
    
    **100% FREE**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    **Include in your description:**
    - Room type
    - Budget (₹)
    - Colors you want
    - Materials (wood, marble, etc.)
    - Style (modern, rustic, etc.)
    
    **More details = better results!**
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Example")
    
    st.code("""
"Modern bedroom, ₹35,000 budget.
Soft white walls, warm oak bed
frame, minimalist design, sage
green accents, natural lighting,
cozy textiles"
    """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("""
    **Planning AI**: Groq (Llama 3.3)  
    **Images**: Pollinations AI  
    
    🟢 **Status**: Active
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>✨ Built with ❤️ by Kanav Chauhan ✨</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
        <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source</a>
    </p>
    <p style='font-size: 12px; margin-top: 10px;'>
        🧞‍♂️ RoomGenie - AI Renovation Planning & Visualization
    </p>
</div>
""", unsafe_allow_html=True)
