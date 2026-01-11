import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
import io
from PIL import Image
from dotenv import load_dotenv
from supabase import create_client # NEW: Database Connector

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

# --- 2. API & DATABASE SETUP ---
load_dotenv()

# AI Keys
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ AI Key not found!")
    st.stop()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3-flash-preview')

# Supabase Keys (Connect to the table you just made)
sb_url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
sb_key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

if sb_url and sb_key:
    supabase = create_client(sb_url, sb_key)
else:
    st.warning("⚠️ Supabase keys missing. Database features disabled.")
    supabase = None

# --- 3. THE PROFESSIONAL BRAIN (System Prompt) ---
SYSTEM_PROMPT = """
ACT AS: A Senior Document Intelligence Expert and Data Analyst.
TASK: Extract every piece of data from the image into a clean, structured JSON format.

RULES:
1. IDENTIFY: Determine if the image is a table, a handwritten list, or an infographic.
2. HANDWRITING: Handle messy text and Hindi characters (Devanagari) with 100% precision.
3. OUTPUT: Return ONLY a valid JSON object.
{
  "document_type": "string",
  "summary": "string",
  "extracted_data": [ {"Description": "Value", "Amount": "Value"} ],
  "merchant": "string",
  "date": "string",
  "total": 0,
  "confidence_score": "float"
}
"""

# --- 4. SIDEBAR ---
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
m3.metric("Storage", "Supabase Cloud", "Connected" if supabase else "Offline")

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
                    response = model.generate_content([SYSTEM_PROMPT, img])
                    json_str = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_str)
                    
                    st.session_state['data'] = data # Store data to use in other buttons
                    
                    st.write(f"**Document Type:** {data.get('document_type', 'General')}")
                    st.write(f"**AI Summary:** {data.get('summary', 'Scan successful.')}")
                    
                    if data.get('extracted_data'):
                        df = pd.DataFrame(data['extracted_data'])
                        st.session_state['df'] = df
                        
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")

        # If data exists, show table and export buttons
        if 'df' in st.session_state:
            edited_df = st.data_editor(st.session_state['df'], use_container_width=True, num_rows="dynamic")
            
            # --- ACTION BUTTONS ---
            col_a, col_b = st.columns(2)
            
            with col_a:
                # EXCEL EXPORT
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    edited_df.to_excel(writer, index=False)
                st.download_button(
                    label="📥 Download Excel (.xlsx)",
                    data=buffer.getvalue(),
                    file_name="ExtractoAI_Export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            with col_b:
                # SUPABASE SAVE
                if st.button("💾 Save to Cloud History"):
                    if supabase:
                        try:
                            payload = {
                                "merchant_name": st.session_state['data'].get('merchant', 'Unknown'),
                                "date": st.session_state['data'].get('date', 'Unknown'),
                                "total_amount": float(st.session_state['data'].get('total', 0)),
                                "items_json": edited_df.to_dict(orient='records')
                            }
                            supabase.table("extractions").insert(payload).execute()
                            st.success("Saved to Supabase!")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Save Failed: {e}")
                    else:
                        st.error("Database not connected.")
    else:
        st.info("Upload a document on the left to begin.")

st.divider()
st.caption("ExtractoAI.online | Developed by Shyam Yadav | 2026")
