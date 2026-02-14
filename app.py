import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
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
st.markdown('<p class="sub-header">AI-Powered Renovation Planning & Visualization</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">"Professional renovation plans with AI-generated visuals"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., Modern bedroom with ₹30,000 budget. Minimalist white walls, light oak furniture, soft gray textiles, lots of natural light.",
    height=120,
    help="Be specific! Include: room type, budget, colors, materials, style"
)

def generate_image_pollinations(prompt):
    """Generate image using Pollinations.ai - free, no auth needed"""
    try:
        # Clean and enhance prompt for interior design
        clean_prompt = prompt.replace('\n', ' ').strip()
        enhanced_prompt = f"professional interior design photograph, {clean_prompt}, high quality, well lit, modern, clean, architectural photography, 8k"
        
        # Pollinations API - completely free
        encoded_prompt = urllib.parse.quote(enhanced_prompt[:800])
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&enhance=true"
        
        response = requests.get(url, timeout=90)
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            return None
            
    except Exception as e:
        st.error(f"Image generation error: {str(e)}")
        return None

# Generate button
if st.button("🚀 Generate My Dream Room", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Two column layout
    plan_col, image_col = st.columns([1.2, 1])
    
    # STEP 1: Generate renovation plan
    with plan_col:
        status_text.text("🧞‍♂️ Creating your renovation plan...")
        progress_bar.progress(20)
        
        try:
            system_prompt = """You are RoomGenie, an expert AI interior designer. Create detailed, practical renovation plans.

For each request:
1. Extract budget and room type
2. Create cohesive design vision
3. Provide realistic budget breakdown
4. Include timeline
5. End with detailed visual description"""

            user_prompt = f"""{user_input}

Create a comprehensive renovation plan with:

## 1. Design Vision
- Style and theme
- **Color Palette** (specific color names and hex codes if possible)
- **Key Materials** (wood types, metal finishes, fabrics)
- Mood and atmosphere

## 2. Budget Breakdown
Itemized costs that total the budget mentioned

## 3. Timeline
Week-by-week schedule

## 4. Detailed Visual Description
Describe the finished room in vivid detail for AI visualization. Include:
- Exact colors used (walls, furniture, accents)
- All furniture pieces and their materials/finishes
- Lighting (natural and artificial)
- Textures (wood grain, fabric, metal)
- Layout and spatial arrangement
- Decorative elements
- Overall atmosphere

Make it photorealistic and specific!"""

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
            
            # Display plan
            st.success("✅ Renovation Plan Ready!")
            st.markdown(plan)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            st.stop()
    
    # STEP 2: Generate visualization
    with image_col:
        status_text.text("🎨 Generating AI visualization (30-60 seconds)...")
        progress_bar.progress(60)
        
        try:
            # Extract visual description from plan
            visual_prompt = ""
            
            if "visual description" in plan.lower() or "detailed visual" in plan.lower():
                lines = plan.split('\n')
                capture = False
                
                for line in lines:
                    if "visual description" in line.lower() or "detailed visual" in line.lower():
                        capture = True
                        continue
                    
                    if capture:
                        # Stop at next section header
                        if line.strip().startswith('#') and len(visual_prompt) > 50:
                            break
                        
                        if line.strip() and not line.strip().startswith('**'):
                            visual_prompt += line.strip() + " "
                        
                        if len(visual_prompt) > 400:
                            break
            
            # Fallback if no description found
            if len(visual_prompt) < 50:
                visual_prompt = user_input[:300]
            
            progress_bar.progress(70)
            
            # Generate image
            st.info("⏳ Generating image... This may take up to 60 seconds. Please wait...")
            generated_image = generate_image_pollinations(visual_prompt.strip())
            
            progress_bar.progress(100)
            status_text.empty()
            
            if generated_image:
                st.success("✅ Visualization Generated!")
                st.image(
                    generated_image, 
                    caption="AI-Generated Visualization of Your Dream Room",
                    use_container_width=True
                )
                
                # Download button
                buf = BytesIO()
                generated_image.save(buf, format="PNG")
                
                st.download_button(
                    label="📥 Download High-Quality Image",
                    data=buf.getvalue(),
                    file_name="roomgenie_visualization.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Image generation didn't complete. Please try again.")
                
        except Exception as e:
            st.warning(f"Image generation issue: {str(e)}")
            st.info("Your renovation plan is ready in the left column!")
    
    progress_bar.empty()
    
    st.markdown("---")
    st.info("💡 **Next Steps**: Save this plan and visualization! Share with contractors for quotes.")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    Get professional renovation plans with AI-generated visualizations!
    
    **Features:**
    - 📋 Detailed design plans
    - 💰 Budget breakdowns
    - 📅 Week-by-week timelines
    - 🎨 AI-generated room images
    
    **100% FREE • Unlimited Use**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    **Be specific with:**
    - Room type & size
    - Budget amount
    - Color preferences
    - Material choices
    - Style (modern, rustic, etc.)
    
    The more details = better plan & image!
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Example Prompts")
    
    with st.expander("Bedroom Example"):
        st.code("""
Modern master bedroom, ₹40,000 budget.
Soft white walls, warm oak furniture,
sage green accents, minimalist design,
lots of natural light, cozy textiles.
        """, language=None)
    
    with st.expander("Kitchen Example"):
        st.code("""
Contemporary kitchen, ₹60,000 budget.
White subway tiles, marble countertops,
brass fixtures, pendant lights,
light wood cabinets, open shelving.
        """, language=None)
    
    with st.expander("Living Room Example"):
        st.code("""
Cozy living room, ₹35,000 budget.
Earthy tones, comfortable sectional,
indoor plants, warm lighting,
wooden coffee table, textured rugs.
        """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("""
    **Planning AI**  
    Groq (Llama 3.3 70B)
    
    **Image Generation**  
    Pollinations.ai
    
    🟢 **Status**: Active
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>✨ Built with ❤️ by Kanav Chauhan ✨</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
        <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a>
    </p>
    <p style='font-size: 12px; margin-top: 10px;'>
        🧞‍♂️ RoomGenie - Professional Renovation Planning with AI Visualization
    </p>
</div>
""", unsafe_allow_html=True)
