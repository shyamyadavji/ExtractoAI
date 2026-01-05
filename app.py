import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
import io
from PIL import Image
from dotenv import load_dotenv

# --- 1. PROFESSIONAL SEO & DASHBOARD CONFIG ---
st.set_page_config(
    page_title="ExtractoAI Pro | Intelligence Dashboard",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# ExtractoAI by Shyam Yadav\nProfessional AI Data Extraction. [Visit extractoai.online](https://extractoai.online)"
    }
)

# Professional CSS for 2026 SaaS Dashboard Look
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%); 
        color: white; 
        font-weight: bold; 
        height: 3em;
        border: none;
    }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API SETUP ---
load_dotenv()
# Handles both Local and Streamlit Cloud
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Add it to your .env file or Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Using your confirmed working model
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- 3. THE PROFESSIONAL BRAIN (System Prompt) ---
SYSTEM_PROMPT = """
ACT AS: A Senior Document Intelligence Expert and Data Analyst.
TASK: Extract every piece of data from the image into a clean, structured JSON format.

RULES:
1. IDENTIFY: Determine if the image is a table, a handwritten list, or an infographic.
2. HANDWRITING: Handle messy text and Hindi characters (Devanagari) with 100% precision.
3. CONTEXT: Understand the relationship between items and prices (e.g., Qty x Rate = Total).
4. CLEANING: Ignore social media icons, 'Follow' buttons, or video UI elements.

OUTPUT FORMAT: Return ONLY a valid JSON object.
{
  "document_type": "string",
  "summary": "string",
  "extracted_data": [ {"Description": "Value", "Amount": "Value"} ],
  "confidence_score": "float"
}
"""

# --- 4. SIDEBAR (Personal Brand & SEO) ---
with st.sidebar:
    st.title("📑 ExtractoAI v2.5")
    st.markdown("---")
    st.subheader("👤 Developer Profile")
    st.success(f"**Shyam Yadav**") 
    st.write("IT Engineering Student")
    
    st.markdown("🌐 [Official: extractoai.online](https://extractoai.online)")
    
    st.divider()
    st.write("🔗 [LinkedIn](https://linkedin.com/in/shyamyadavji)")
    st.write("📂 [GitHub](https://github.com/shyamyadavji)")

# --- 5. DASHBOARD METRICS ---
st.title("AI Document Intelligence Platform")
st.markdown("##### High-Speed Extraction for 2026 Enterprises")

m1, m2, m3 = st.columns(3)
m1.metric("Current Engine", "Gemini 3 Flash", "Frontier")
m2.metric("Intelligence", "Multimodal", "Active")
m3.metric("Language", "Global (incl. Hindi)", "Enabled")

st.divider()

# --- 6. MAIN WORKSPACE ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📤 Source Image")
    uploaded_file = st.file_uploader("Upload Receipt, Table, or Roadmap", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Document Preview", use_container_width=True)

with col_right:
    st.subheader("📝 Extraction Results")
    
    if uploaded_file:
        if st.button("🚀 Execute Smart Extraction"):
            with st.spinner("Gemini 3 is thinking..."):
                try:
                    # AI Processing
                    response = model.generate_content([SYSTEM_PROMPT, img])
                    
                    # Ensure the response is valid JSON
                    json_str = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_str)
                    
                    # Show Result Summary
                    st.write(f"**Document Type:** {data.get('document_type', 'General')}")
                    st.write(f"**AI Summary:** {data.get('summary', 'Scan successful.')}")
                    
                    # Display the Table
                    if data.get('extracted_data'):
                        df = pd.DataFrame(data['extracted_data'])
                        
                        # THE EDITABLE TABLE (SaaS Feature)
                        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                        
                        # EXCEL DOWNLOAD LOGIC (.xlsx)
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            edited_df.to_excel(writer, index=False)
                        
                        st.download_button(
                            label="📥 Download Professional Excel (.xlsx)",
                            data=buffer.getvalue(),
                            file_name=f"ExtractoAI_{data['document_type']}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.success(f"AI Confidence: {data.get('confidence_score', 'N/A')}")
                    
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")
                    st.info("Try refreshing or check if your API key has enough quota.")
    else:
        st.info("Upload a document on the left to begin.")

# --- 7. FOOTER ---
st.divider()
st.caption("ExtractoAI.online | Developed by Shyam Yadav | 2026")