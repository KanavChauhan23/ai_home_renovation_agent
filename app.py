import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import time

# Initialize clients
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
HF_TOKEN = st.secrets["HUGGINGFACE_API_KEY"]

st.set_page_config(page_title="AI Home Renovation Planner", layout="wide", page_icon="🏠")

# Header
st.title("🏠 AI Home Renovation Planner")
st.markdown("**Professional renovation planning with AI-generated visualizations**")
st.markdown("---")

# Input section
col1, col2 = st.columns(2)

with col1:
    room_type = st.text_input(
        "🏡 Room Type",
        placeholder="e.g., Kitchen, Bedroom, Living Room, Bathroom...",
        help="Enter the type of room you want to renovate"
    )

with col2:
    budget = st.number_input(
        "💰 Budget (USD)",
        min_value=1000,
        max_value=1000000,
        value=7000,
        step=500,
        help="Enter your renovation budget"
    )

def generate_image_huggingface(prompt):
    """Generate image using Hugging Face Stable Diffusion XL"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # Enhanced prompt for better interior design images
        enhanced_prompt = f"Professional interior design photograph, {prompt}, high quality 8k, architectural digest magazine style, bright natural lighting, professionally staged, wide angle shot, photorealistic"
        
        payload = {
            "inputs": enhanced_prompt[:900],  # API has length limits
            "parameters": {
                "negative_prompt": "blurry, distorted, ugly, low quality, cartoon, drawing, sketch, rendering, 3d render",
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        
        if response.status_code == 503:
            st.warning("⏳ Model is waking up... This may take 20-30 seconds on first use.")
            time.sleep(20)
            # Retry once
            response = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"Image generation failed: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

# Generate button
if st.button("🚀 Generate Complete Renovation Plan", use_container_width=True, type="primary"):
    
    if not room_type or not room_type.strip():
        st.error("⚠️ Please enter a room type (e.g., Kitchen, Bedroom, Living Room)")
        st.stop()
    
    if budget < 1000:
        st.error("⚠️ Budget must be at least $1,000")
        st.stop()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # STEP 1: Generate renovation plan
    status_text.text("🤖 Creating your detailed renovation plan...")
    progress_bar.progress(20)
    
    try:
        detailed_prompt = f"""Create a comprehensive, professional renovation plan for a {room_type} with a budget of ${budget}.

Structure your response with these exact sections:

## 1. Design Vision & Concept
- Overall design style and theme
- Complete color palette (primary, secondary, accent - with specific color names)
- Key materials and textures
- Atmosphere and mood you're creating
- Unique design elements that make this special

## 2. Detailed Budget Breakdown
Break down the ${budget} into these categories with specific dollar amounts:
- Paint & Wall Preparation: $XXX
- Flooring: $XXX
- Lighting Fixtures: $XXX
- Furniture (list main pieces): $XXX
- Hardware & Fixtures: $XXX
- Decor & Accessories: $XXX
- Labor/Installation: $XXX
- Contingency (10%): $XXX
**TOTAL: ${budget}**

## 3. Implementation Timeline
Provide a week-by-week breakdown:
- **Week 1**: Planning, ordering, preparation
- **Week 2**: Demolition, painting, core updates
- **Week 3**: Installation of fixtures, furniture
- **Week 4**: Finishing touches, styling, completion

## 4. AI Visualization Prompt
Write a highly detailed, photorealistic description for AI image generation. Be extremely specific about:
- Camera angle and framing
- Every visible color (walls, floors, furniture)
- All furniture pieces and their exact materials/finishes
- Lighting sources and quality
- Textures visible (wood grain, fabric types, metal finishes)
- Decorative elements
- Overall atmosphere and mood
- Time of day and natural light

Make it vivid enough that someone could visualize the exact space.

Be practical, specific, and professional in all recommendations."""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert interior designer with 20 years of experience. Provide detailed, realistic, and budget-conscious renovation plans. Be specific with costs, materials, and visual descriptions. Write in a professional but accessible tone."
                },
                {
                    "role": "user",
                    "content": detailed_prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=3000
        )
        
        renovation_plan = chat_completion.choices[0].message.content
        progress_bar.progress(50)
        
    except Exception as e:
        st.error(f"❌ Error generating plan: {str(e)}")
        st.stop()
    
    # STEP 2: Extract and generate image
    status_text.text("🎨 Generating AI visualization (this takes 20-40 seconds)...")
    progress_bar.progress(60)
    
    try:
        # Extract visualization prompt
        if "AI Visualization Prompt" in renovation_plan or "Visualization Prompt" in renovation_plan:
            lines = renovation_plan.split('\n')
            image_prompt = ""
            capture = False
            
            for i, line in enumerate(lines):
                if "visualization prompt" in line.lower() or "ai visualization" in line.lower():
                    capture = True
                    # Start capturing from next line
                    continue
                    
                if capture:
                    # Stop if we hit another section header (## or #)
                    if line.strip().startswith('#') and len(image_prompt) > 50:
                        break
                    # Collect the prompt text
                    if line.strip() and not line.strip().startswith('**'):
                        image_prompt += line.strip() + " "
                    # Break if we have enough
                    if len(image_prompt) > 400:
                        break
            
            # Clean up the prompt
            image_prompt = image_prompt.strip()
            
            # If extraction worked, use it
            if len(image_prompt) > 50:
                final_prompt = image_prompt
            else:
                # Fallback: create generic prompt
                final_prompt = f"beautiful modern {room_type}, professionally designed interior, high-end finishes, natural lighting, comfortable and inviting atmosphere"
        else:
            final_prompt = f"beautiful modern {room_type}, professionally designed interior, high-end finishes, natural lighting"
        
        progress_bar.progress(70)
        
        # Generate the image
        generated_image = generate_image_huggingface(final_prompt)
        progress_bar.progress(100)
        status_text.empty()
        
    except Exception as e:
        st.warning(f"⚠️ Could not generate visualization: {str(e)}")
        generated_image = None
    
    # Display Results
    st.success("✅ Complete Renovation Plan Generated!")
    st.markdown("---")
    
    # Show renovation plan
    st.markdown(renovation_plan)
    
    # Show generated image
    if generated_image:
        st.markdown("---")
        st.markdown("## 🎨 AI-Generated Visualization")
        st.image(generated_image, caption=f"Your Renovated {room_type.title()} - Budget: ${budget:,}", use_container_width=True)
        
        # Download button
        buf = BytesIO()
        generated_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="📥 Download Visualization (High Quality PNG)",
            data=byte_im,
            file_name=f"{room_type.lower().replace(' ', '_')}_renovation_${budget}.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("💡 Image generation unavailable, but your detailed renovation plan is above!")
    
    st.markdown("---")
    st.info("💡 **Next Steps**: Save this plan, discuss with contractors, and get detailed quotes before starting work!")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 How It Works")
    st.markdown("""
    **Step 1**: Enter room type and budget
    
    **Step 2**: Click Generate
    
    **Step 3**: Receive:
    - 📋 Complete renovation plan
    - 💰 Itemized budget
    - 📅 4-week timeline  
    - 🎨 AI-generated photo
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Budget Examples")
    st.markdown("""
    **Light Refresh**
    - $2,000 - $5,000
    - Paint, fixtures, decor
    
    **Medium Update**  
    - $5,000 - $15,000
    - New flooring, furniture
    
    **Full Renovation**
    - $15,000 - $50,000+
    - Complete transformation
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("""
    **Planning AI**  
    Groq (Llama 3.3 70B)
    
    **Image Generation**  
    Stable Diffusion XL
    
    **Status**: 🟢 Active
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Features")
    st.markdown("""
    ✅ Professional design advice
    ✅ Realistic budget breakdowns
    ✅ Detailed timelines
    ✅ AI visualization
    ✅ Downloadable images
    ✅ Unlimited usage
    ✅ 100% FREE
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Built with ❤️ by Kanav Chauhan</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a>
    </p>
    <p style='font-size: 12px; color: gray;'>
        Powered by Groq AI & Stable Diffusion XL | Free Professional Renovation Planning
    </p>
</div>
""", unsafe_allow_html=True)
