import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import time

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
HF_TOKEN = st.secrets["HUGGINGFACE_API_KEY"]

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
st.markdown('<p class="tagline">"Make a wish, see your dream room come to life"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., I want to renovate my kitchen with ₹50,000 budget. Modern white design with wooden countertops.",
    height=120,
    help="Include: room type, budget, style, colors, and any special requirements"
)

def try_multiple_image_apis(prompt):
    """Try multiple image generation APIs until one works"""
    
    # Clean and enhance prompt
    enhanced_prompt = f"professional interior design photo, {prompt}, high quality, well lit, modern, clean, architectural photography"
    
    # Method 1: Try Black Forest Labs FLUX (newer, more reliable)
    try:
        st.info("🎨 Trying FLUX model...")
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": enhanced_prompt[:400]},
            timeout=60
        )
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        elif response.status_code == 503:
            st.info("⏳ FLUX model loading... trying next option...")
    except:
        pass
    
    # Method 2: Try Stable Diffusion 2.1
    try:
        st.info("🎨 Trying Stable Diffusion 2.1...")
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": enhanced_prompt[:400]},
            timeout=60
        )
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        elif response.status_code == 503:
            time.sleep(15)
            response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt[:400]}, timeout=60)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
    except:
        pass
    
    # Method 3: Try Dreamlike Photoreal
    try:
        st.info("🎨 Trying Dreamlike Photoreal...")
        API_URL = "https://api-inference.huggingface.co/models/dreamlike-art/dreamlike-photoreal-2.0"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": enhanced_prompt[:400]},
            timeout=60
        )
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass
    
    # Method 4: Fallback - Pollinations (no auth needed)
    try:
        st.info("🎨 Trying Pollinations.ai...")
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(enhanced_prompt[:300])}?width=1024&height=768&nologo=true"
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        pass
    
    return None

# Generate button
if st.button("🚀 Generate My Dream Room", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    # Two column layout
    plan_col, image_col = st.columns([1.2, 1])
    
    # Generate plan
    with plan_col:
        with st.spinner("🧞‍♂️ RoomGenie is working its magic..."):
            try:
                system_prompt = """You are RoomGenie, an expert AI interior designer. You create detailed, practical, and inspiring renovation plans.

For each request:
1. Understand the budget and room type
2. Create a cohesive design vision
3. Provide specific, realistic budget breakdown
4. Include a detailed timeline
5. End with a vivid visual description for AI image generation"""

                user_prompt = f"""{user_input}

Create a comprehensive renovation plan with:

**1. Design Vision**
- Overall style and theme
- Color palette (specific colors)
- Key materials and finishes
- Mood and atmosphere

**2. Budget Breakdown**
List specific items with costs

**3. Timeline**
Week-by-week schedule

**4. Visual Description**
Describe the finished room in vivid detail for AI visualization - include colors, furniture, lighting, layout, textures. Make it photorealistic and specific."""

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
                
                st.success("✅ Your Dream Room Plan is Ready!")
                st.markdown(plan)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # Generate image
    with image_col:
        with st.spinner("🎨 Visualizing your dream room..."):
            try:
                # Extract visual description
                visual_prompt = ""
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
                            visual_prompt += line.strip() + " "
                            if len(visual_prompt) > 250:
                                break
                
                if len(visual_prompt) < 50:
                    visual_prompt = user_input
                
                # Try multiple APIs
                image = try_multiple_image_apis(visual_prompt.strip())
                
                if image:
                    st.success("✅ Visualization Ready!")
                    st.image(image, caption="Your Dream Room", use_container_width=True)
                    
                    # Download
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="📥 Download Image",
                        data=buf.getvalue(),
                        file_name="roomgenie_visualization.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ Image generation is temporarily unavailable. Your renovation plan is ready!")
                    st.info("💡 Try again in a few minutes - the models may be loading.")
                    
            except Exception as e:
                st.warning(f"Image issue: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    RoomGenie uses AI to help you:
    - Plan renovations
    - Visualize results
    - Manage budgets
    - Create timelines
    
    **100% FREE** • **Unlimited Use**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Example Wishes")
    st.code("""
"Modern bedroom, ₹30,000,
minimalist white & wood"
    """, language=None)
    
    st.code("""
"Cozy living room, ₹50,000,
warm earthy tones, plants"
    """, language=None)
    
    st.code("""
"Luxury bathroom, ₹80,000,
marble & brass finishes"
    """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ AI Models")
    st.markdown("""
    **Planning**: Groq Llama 3.3
    **Images**: Multiple SD models
    
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
        🧞‍♂️ RoomGenie - Make a wish, see your dream room
    </p>
</div>
""", unsafe_allow_html=True)
