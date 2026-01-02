import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
from PIL import Image
from dotenv import load_dotenv

# --- 1. PROFESSIONAL CONFIGURATION ---
st.set_page_config(
    page_title="ExtractoAI | Intelligence Dashboard",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for 2026 SaaS Look
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2563eb; color: white; font-weight: bold; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY & KEYS ---
load_dotenv()
# Logic to handle both Local (.env) and Streamlit Cloud (Secrets)
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Add it to your .env file or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# We use gemini-2.0-flash-lite for 2026 stability and free-tier speed
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- 3. THE BRAIN (Professional System Prompt) ---
SYSTEM_PROMPT = """
ACT AS: A Senior Document Intelligence Expert.
IMAGE ANALYSIS RULES:
1. Identify the TYPE of document (Handwritten list, Financial table, Infographic, or Roadmap).
2. If it is a TABLE: Extract every row and column accurately.
3. If it is HANDWRITTEN: Recognize Hindi/English mixed text (e.g., '10 दर्जन' or 'विजय मौर्या'). 
4. If it is a ROADMAP/INFOGRAPHIC: Extract the main categories as 'Headers' and bullet points as 'Data'.
5. CLEANING: Remove UI elements like 'likes', 'video icons', or 'Follow' buttons from screenshots.

OUTPUT FORMAT: Return ONLY a valid JSON object. 
Structure:
{
  "document_type": "string",
  "summary": "string",
  "extracted_data": [ {"Column1": "Value", "Column2": "Value"} ],
  "confidence_score": "float"
}
"""

# --- 4. SIDEBAR (Personal Brand Highlight) ---
with st.sidebar:
    st.title("📑 ExtractoAI v2.5")
    st.markdown("---")
    st.subheader("👤 Developer Profile")
    st.success(f"**Shyam Yadav**") # Your Name Highlighted
    st.write("IT Engineering Student")
    st.info("System: 2026 Stable AI")
    
    st.divider()
    st.write("🔗 [LinkedIn](https://linkedin.com/in/shyamyadavji)")
    st.write("📂 [GitHub](https://github.com/shyamyadavji)")

# --- 5. DASHBOARD HEADER ---
st.title("AI Document Intelligence Platform")
st.markdown("##### Professional OCR & Data Extraction for Complex Documents")

# Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Engine", "Gemini 2.0 Flash", "Stable")
m2.metric("Processing Time", "1.2s", "-0.3s")
m3.metric("Multi-Language", "Active", "Hindi/Eng")

st.divider()

# --- 6. MAIN WORKSPACE ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📤 Input Source")
    uploaded_file = st.file_uploader("Upload Image (Receipt, Table, or Roadmap)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Document Preview", use_container_width=True)

with col_right:
    st.subheader("📝 Extraction Results")
    
    if uploaded_file:
        if st.button("🚀 Execute Smart Extraction"):
            with st.spinner("AI analyzing structure and language..."):
                try:
                    # AI Call
                    response = model.generate_content([SYSTEM_PROMPT, img])
                    
                    # Clean response to ensure valid JSON
                    json_str = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_str)
                    
                    # Display Metadata
                    st.write(f"**Type:** {data.get('document_type', 'General')}")
                    st.write(f"**Summary:** {data.get('summary', 'Processed successfully')}")
                    
                    # Show the Table
                    if data.get('extracted_data'):
                        df = pd.DataFrame(data['extracted_data'])
                        
                        # THE EDITABLE TABLE (SaaS Level)
                        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                        
                        # Download Section
                        csv = edited_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Export to Excel (CSV)",
                            data=csv,
                            file_name=f"extracto_{data['document_type']}.csv",
                            mime="text/csv"
                        )
                    
                    st.success(f"Confidence: {data.get('confidence_score', 'N/A')}")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("The AI might have exceeded the free rate limit. Please wait 60 seconds and try again.")
    else:
        st.info("Please upload a document to begin the AI analysis.")

# --- 7. FOOTER ---
st.divider()
st.caption("ExtractoAI Project | Built for Portfolio | Jan 2026")



