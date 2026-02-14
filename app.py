import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import time

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
st.markdown('<p class="tagline">"Professional renovation plans with AI visualization"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., Modern kitchen with ₹50,000 budget. White cabinets, marble countertops, brass fixtures, pendant lights.",
    height=120,
    help="Include: room type, budget, colors, materials, style"
)

def generate_simple_image(room_description):
    """Generate image with simple, reliable method"""
    try:
        # Create very simple, focused prompt
        simple_prompt = f"beautiful modern interior design of {room_description}, professional photography, high quality, well lit"
        
        # Encode for URL
        encoded = urllib.parse.quote(simple_prompt[:300])
        
        # Pollinations URL with parameters for better quality
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=768&nologo=true&model=flux&enhance=true&safe=true"
        
        # Longer timeout and multiple retries
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=120)
                
                if response.status_code == 200 and len(response.content) > 1000:
                    return Image.open(BytesIO(response.content)), url
                
                # Wait between retries
                if attempt < 2:
                    time.sleep(5)
                    
            except:
                if attempt < 2:
                    time.sleep(5)
                continue
        
        return None, url
        
    except Exception as e:
        return None, None

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

Create a renovation plan with:

## 1. Design Vision
- Style and theme
- **Color Palette** (specific colors with hex codes)
- **Materials** (wood types, metals, fabrics)
- Mood

## 2. Budget Breakdown
Itemized costs

## 3. Timeline
Week by week

## 4. Visual Summary
One paragraph describing the finished room - colors, furniture, lighting, layout."""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2000
            )
            
            plan = response.choices[0].message.content
            progress_bar.progress(50)
            
            st.success("✅ Renovation Plan Ready!")
            st.markdown(plan)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            st.stop()
    
    # Generate image
    with image_col:
        status_text.text("🎨 Generating visualization...")
        progress_bar.progress(60)
        
        # Extract simple room description from user input
        room_desc = user_input.split('.')[0] if '.' in user_input else user_input[:200]
        
        st.info("⏳ Generating image... Please wait 30-60 seconds...")
        
        generated_image, image_url = generate_simple_image(room_desc)
        
        progress_bar.progress(100)
        status_text.empty()
        
        if generated_image:
            st.success("✅ Visualization Generated!")
            st.image(generated_image, caption="Your Dream Room", use_container_width=True)
            
            # Download button
            buf = BytesIO()
            generated_image.save(buf, format="PNG")
            st.download_button(
                label="📥 Download Image",
                data=buf.getvalue(),
                file_name="roomgenie.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Image generation is taking longer than expected.")
            
            if image_url:
                st.info("💡 **Alternative**: Click the link below to view your generated image:")
                st.markdown(f"[🖼️ View Generated Image]({image_url})")
                st.caption("(The image might take a few seconds to load)")
    
    progress_bar.empty()
    
    st.markdown("---")
    st.info("💡 **Tip**: Bookmark or screenshot this page to save your plan!")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    Professional AI renovation planning
    
    **What you get:**
    - 📋 Detailed design plan
    - 💰 Budget breakdown
    - 📅 Timeline
    - 🎨 AI visualization (when available)
    
    **100% FREE**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    **For best results include:**
    - Room type
    - Budget
    - Colors you want
    - Materials (wood, marble, etc.)
    - Style (modern, rustic, etc.)
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Examples")
    
    st.code("""
"Modern bedroom, ₹35,000,
white walls, oak furniture,
minimalist, natural light"
    """, language=None)
    
    st.code("""
"Cozy living room, ₹45,000,
warm tones, plants, 
comfortable seating"
    """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Tech")
    st.markdown("""
    **Planning**: Groq AI  
    **Images**: Pollinations AI
    
    🟢 Active
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>✨ Built with ❤️ by Kanav Chauhan ✨</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a>
    </p>
    <p style='font-size: 12px; margin-top: 10px;'>
        🧞‍♂️ RoomGenie - AI Renovation Planning
    </p>
</div>
""", unsafe_allow_html=True)
