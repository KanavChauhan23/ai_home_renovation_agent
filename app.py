import streamlit as st
from groq import Groq
import urllib.parse

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page config
st.set_page_config(
    page_title="SmartGhar AI - Intelligent Home Renovation Planner", 
    layout="wide", 
    page_icon="🏡"
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 300;
    }
    
    .hindi-text {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 1rem;
        border: none;
        border-radius: 15px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .feature-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .gemini-button {
        background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .gemini-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏡 SmartGhar AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Intelligent Home Renovation Planning</p>', unsafe_allow_html=True)
st.markdown('<p class="hindi-text">आपके सपनों का घर, AI की मदद से</p>', unsafe_allow_html=True)

st.markdown("---")

# Main input
st.markdown("### 💭 Describe Your Dream Renovation")

user_input = st.text_area(
    "",
    placeholder="Example: I want to renovate my bedroom with ₹40,000 budget. Modern minimalist design with soft white walls, warm oak furniture, sage green accents, and plenty of natural light.",
    height=130,
    help="Be detailed! Include room type, budget, colors, materials, style preferences, and special requirements."
)

# Quick tips in expander
with st.expander("💡 Tips for Better Results"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Include These Details:**
        - 🏠 Room type and size
        - 💰 Your budget (in ₹)
        - 🎨 Preferred colors
        - 🪵 Materials (wood, marble, etc.)
        - ✨ Style (modern, rustic, etc.)
        """)
    with col2:
        st.markdown("""
        **Example Budgets:**
        - Light refresh: ₹20,000 - ₹50,000
        - Medium update: ₹50,000 - ₹1,50,000
        - Full renovation: ₹1,50,000+
        """)

# Generate button
if st.button("🚀 Generate Smart Renovation Plan", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your renovation project first!")
        st.stop()
    
    # Progress
    with st.spinner("🤖 SmartGhar AI is analyzing your requirements and creating a professional plan..."):
        
        try:
            system_prompt = """You are SmartGhar AI, an expert Indian interior designer and renovation consultant with 20+ years of experience. You understand Indian homes, local materials, vendors, and budget constraints.

Create comprehensive, practical, and inspiring renovation plans that are:
- Realistic for Indian markets and budgets
- Specific with Indian brands and materials where relevant
- Culturally appropriate and practical
- Professional yet approachable
- Actionable and well-organized"""

            user_prompt = f"""{user_input}

Create a COMPREHENSIVE renovation plan with these sections:

# 📋 Project Overview
- Brief project summary
- Total budget allocation
- Estimated timeline
- Difficulty level (DIY-friendly / Professional needed)

# 🎨 Design Vision & Concept
**Style & Theme:**
- Overall design style (e.g., Modern Minimalist, Contemporary Indian, Rustic, Industrial, etc.)
- Design philosophy and approach
- Key inspirations

**Color Palette:**
- Primary color: [Name] (#HexCode) - where to use
- Secondary color: [Name] (#HexCode) - accents
- Accent color: [Name] (#HexCode) - highlights
- Neutral base: [Name] (#HexCode) - backgrounds

**Materials & Finishes:**
- Flooring: [Specific material, brand if relevant]
- Walls: [Paint/wallpaper/texture]
- Furniture: [Wood types, metal finishes]
- Fixtures: [Chrome/Brass/Black/etc.]
- Fabrics: [Cotton/Linen/Velvet/etc.]

**Atmosphere:**
- Mood and feeling the space should evoke
- Lighting strategy (natural + artificial)
- Flow and functionality

# 💰 Detailed Budget Breakdown

Break down the total budget into specific categories with realistic costs for Indian market:

**1. Paint & Wall Treatment:** ₹X,XXX
   - Interior paint (Asian Paints/Berger/etc.): ₹X,XXX
   - Primer and supplies: ₹XXX
   - Labor for painting: ₹X,XXX

**2. Flooring:** ₹X,XXX
   - Material (specify type): ₹X,XXX
   - Installation: ₹XXX
   - Skirting/borders: ₹XXX

**3. Furniture:** ₹X,XXX
   - [Item 1]: ₹X,XXX
   - [Item 2]: ₹X,XXX
   - [Item 3]: ₹X,XXX

**4. Lighting:** ₹X,XXX
   - Ceiling lights: ₹X,XXX
   - Task lighting: ₹XXX
   - Ambient/decorative: ₹XXX

**5. Fixtures & Hardware:** ₹X,XXX
   - Door handles, drawer pulls: ₹XXX
   - [Room-specific fixtures]: ₹X,XXX

**6. Decor & Accessories:** ₹X,XXX
   - Curtains/blinds: ₹X,XXX
   - Artwork/wall decor: ₹XXX
   - Plants and planters: ₹XXX
   - Soft furnishings: ₹X,XXX

**7. Electrical Work:** ₹X,XXX
   - New points/switches: ₹XXX
   - Wiring upgrades: ₹XXX

**8. Labor & Installation:** ₹X,XXX
   - Carpenter: ₹XXX
   - Electrician: ₹XXX
   - Painter: ₹XXX
   - Miscellaneous: ₹XXX

**9. Contingency (10-15%):** ₹X,XXX

**TOTAL:** ₹X,XXX

# 📅 Implementation Timeline

**Week 1: Planning & Preparation**
- Finalize design choices and measurements
- Order items with long lead times (furniture, custom pieces)
- Purchase all materials (paint, fixtures, etc.)
- Clear the room and protect existing items

**Week 2: Core Structural Work**
- Any electrical work (new points, relocations)
- Wall preparation (filling, sanding, priming)
- Painting (ceiling first, then walls - 2 coats)
- Flooring installation (if replacing)

**Week 3: Installation & Assembly**
- Furniture delivery and assembly
- Fixture installation (lights, hardware)
- Curtain rod installation
- Any custom carpentry work

**Week 4: Finishing & Styling**
- Decor placement (artwork, mirrors)
- Soft furnishings (curtains, rugs, cushions)
- Plants and accessories
- Final touch-ups and adjustments
- Deep cleaning

# 🛒 Smart Shopping Guide

**Where to Buy (India):**

*Furniture:*
- Budget: IKEA, Pepperfry, Urban Ladder
- Mid-range: Fabindia, West Elm (online)
- Custom: Local carpenters (often best value!)

*Materials:*
- Paint: Asian Paints, Berger, Dulux showrooms
- Tiles/Flooring: Kajaria, Somany, local tile markets
- Hardware: D-Decor, Hafele, local hardware stores

*Decor:*
- HomeStop, Home Centre, Zara Home
- Local markets (Sarojini, Chor Bazaar, etc.)
- Online: Amazon, Flipkart

**Money-Saving Tips:**
- Buy during sale seasons (Diwali, End of Season)
- Mix high and low - splurge on key pieces, save on others
- Consider second-hand/upcycled furniture
- Local craftsmen often better value than brands

# 💪 DIY vs Professional

**You Can DIY:**
- Painting (with proper preparation)
- Simple furniture assembly
- Decor arrangement and styling
- Installing curtain rods, artwork
- Basic organization

**Hire Professionals For:**
- Electrical work (safety!)
- Complex carpentry
- Flooring installation
- Heavy furniture assembly
- Anything structural

# 🎯 Pro Tips & Recommendations

1. **Quality over Quantity:** Better to have fewer, quality pieces than many cheap items
2. **Lighting is Key:** Good lighting can transform a space - don't skip this
3. **Ventilation Matters:** Ensure proper air flow, especially in Indian climate
4. **Local is Often Better:** Indian wood (Sheesham, Teak) lasts longer than imports
5. **Plan for Maintenance:** Choose materials easy to clean and maintain
6. **Think Long-term:** Trends fade, classic designs last

# 🖼️ AI Image Generation Prompt

**COPY THIS PROMPT TO GENERATE YOUR ROOM VISUALIZATION:**

"Professional interior design photography of a [room type]. [Provide extremely detailed description including: exact wall colors with hex codes, all furniture pieces with materials and colors, flooring type and color, lighting fixtures and placement, window treatments, decorative elements, plants if any, overall atmosphere - warm/cool/bright/cozy, camera angle - wide shot from doorway/corner, time of day - afternoon with natural light, style - modern/rustic/minimalist etc.]. High quality, 8k, architectural photography, professionally staged, bright and inviting, photo-realistic."

**Example enhanced with your specific details:**
[Write a highly detailed, vivid paragraph describing EXACTLY what the finished room will look like, incorporating all the design elements, colors, and materials mentioned above. Make it so detailed that an AI can visualize it perfectly.]

# 📱 Generate Your Visualization

Click the button below to open Google Gemini and generate your room image for FREE!

**What to do:**
1. Click the "Generate Image in Gemini" button below
2. The AI image prompt will be automatically pasted
3. Click "Generate" in Gemini (it's FREE!)
4. Download your room visualization
5. Compare with your renovation to see how close you got!

Make this plan INSPIRING, PRACTICAL, and ACHIEVABLE. Use Indian context, brands, and budget realities!"""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=4000
            )
            
            plan = response.choices[0].message.content
            
            # Display success
            st.success("✅ Your Professional Renovation Plan is Ready!")
            st.balloons()
            
            st.markdown("---")
            
            # Display the plan
            st.markdown(plan)
            
            # Extract AI image prompt
            st.markdown("---")
            st.markdown("## 🎨 Generate Your Room Visualization")
            
            # Try to extract the image prompt from the plan
            image_prompt = ""
            if "AI Image Generation Prompt" in plan or "image generation prompt" in plan.lower():
                lines = plan.split('\n')
                capture = False
                for line in lines:
                    if "image generation prompt" in line.lower() or "COPY THIS PROMPT" in line:
                        capture = True
                        continue
                    if capture and line.strip():
                        if line.strip().startswith('#') and len(image_prompt) > 100:
                            break
                        if line.strip() and not line.strip().startswith('**') and not line.strip().startswith('#'):
                            image_prompt += line.strip() + " "
                        if len(image_prompt) > 600:
                            break
            
            # Fallback if extraction failed
            if len(image_prompt) < 100:
                image_prompt = f"Professional interior design photography of a beautifully renovated {user_input[:200]}, high quality, well lit, modern, clean, architectural photography, 8k, photorealistic"
            
            # Show the prompt in a copyable box
            st.markdown("### 📋 Your AI Image Prompt:")
            st.info("💡 **Tip:** Click inside the text box below to select all, then copy (Ctrl+C / Cmd+C)")
            
            # Display prompt in text area (easier to copy)
            st.text_area(
                "",
                value=image_prompt.strip(),
                height=150,
                key="image_prompt_area",
                label_visibility="collapsed"
            )
            
            # Alternative: Also show in code block with built-in copy button
            with st.expander("📄 View as formatted text"):
                st.code(image_prompt.strip(), language=None)
            
            # Create Gemini link with pre-filled prompt
            gemini_prompt = f"Generate an image: {image_prompt.strip()}"
            encoded_prompt = urllib.parse.quote(gemini_prompt)
            gemini_url = f"https://gemini.google.com/app?hl=en"
            
            # Buttons
            col1, col2 = st.columns(2)
            
            with col1:
                st.link_button(
                    "🎨 Generate Image in Google Gemini (FREE!)",
                    gemini_url,
                    use_container_width=True,
                    type="primary"
                )
                st.caption("Opens Gemini - paste the prompt above and click Generate")
            
            with col2:
                # Alternative: Direct Gemini Imagen link
                st.link_button(
                    "🖼️ Try ImageFX (Google's AI)",
                    "https://aitestkitchen.withgoogle.com/tools/image-fx",
                    use_container_width=True
                )
                st.caption("Google's dedicated image generator - paste prompt there")
            
            st.info("""
💡 **How to generate your visualization:**
1. Copy the AI Image Prompt above
2. Click one of the buttons to open Google's AI
3. Paste the prompt and click "Generate"
4. Download your FREE AI-generated room image!
5. Compare it with your actual renovation progress!
            """)
            
            st.markdown("---")
            
            # Final tips
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success("""
**💾 Save This Plan**
- Screenshot or bookmark this page
- Share link with contractors
- Print for reference during work
- Open renovation for quick guidance
                """)
            
            with col2:
                st.info("""
**📞 Next Steps**
- Get quotes from 2-3 contractors
- Visit showrooms for materials
- Start ordering long-lead items
- Create a project timeline
                """)
            
            with col3:
                st.warning("""
**⚠️ Important**
- Keep 10-15% buffer for unexpected costs
- Take clear before and after photos to track progress.
- Check material quality before buying.
                """)
            
        except Exception as e:
            st.error(f"❌ Error generating plan: {str(e)}")
            st.info("Please check your internet connection and try again.")

# Sidebar
with st.sidebar:
    st.markdown("### 🏡 About SmartGhar AI")
    st.markdown("""
    **SmartGhar AI** is your intelligent home renovation assistant, designed specifically for Indian homes and budgets.
    
    **What You Get:**
    - 📋 Detailed renovation plans
    - 💰 Realistic budget breakdowns
    - 📅 Week-by-week timelines
    - 🛒 Smart shopping guides
    - 🎨 AI image prompts
    - 💡 Pro tips from experts
    
    **100% FREE • Unlimited Use • Made in India 🇮🇳**
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌟 Perfect For")
    st.markdown("""
    - Homeowners planning renovations
    - Interior design enthusiasts
    - First-time renovators
    - Budget-conscious families
    - DIY lovers
    - Real estate investors
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Sample Projects")
    
    with st.expander("₹30,000 Bedroom Refresh"):
        st.code("""
"Bedroom renovation, ₹30,000 budget.
Soft white walls, warm oak furniture,
minimalist design, sage green accents,
natural lighting, cozy textiles"
        """, language=None)
    
    with st.expander("₹60,000 Kitchen Update"):
        st.code("""
"Modern kitchen, ₹60,000 budget.
White subway tiles, marble countertops,
brass fixtures, light wood cabinets,
open shelving, pendant lights"
        """, language=None)
    
    with st.expander("₹80,000 Living Room"):
        st.code("""
"Cozy living room, ₹80,000 budget.
Earthy tones, L-shaped sectional sofa,
indoor plants, warm LED lighting,
wooden coffee table, jute rug"
        """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Powered By")
    st.markdown("""
    **AI Model**: Groq (Llama 3.3 70B)  
    **Image Generation**: Google Gemini/ImageFX  
    
    🟢 **Status**: Active & Fast
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Why SmartGhar?")
    st.markdown("""
    - 🇮🇳 Built for Indian homes
    - 💰 Realistic Indian pricing
    - 🛒 Local vendor suggestions
    - 🌡️ Climate-appropriate advice
    - 🎨 Cultural design sensitivity
    - ⚡ Lightning-fast results
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p style='font-size: 1.2rem; font-weight: 600;'>✨ Built with ❤️ by Kanav Chauhan ✨</p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank' style='margin: 0 10px;'>GitHub</a> |
        <a href='https://linkedin.com/in/kanavchauhan23' target='_blank' style='margin: 0 10px;'>LinkedIn</a>
    </p>
    <p style='font-size: 0.9rem; margin-top: 1rem; color: #888;'>
        🏡 SmartGhar AI - Making Indian Homes Beautiful, One Room at a Time
    </p>
    <p style='font-size: 0.8rem; color: #aaa;'>
        आपके सपनों का घर, AI की मदद से | Your Dream Home, Powered by AI
    </p>
</div>
""", unsafe_allow_html=True)
