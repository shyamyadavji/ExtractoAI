import streamlit as st
import google.generativeai as genai
import pandas as pd
import json, os
from dotenv import load_dotenv
from PIL import Image

# 1. Page Settings
st.set_page_config(page_title="ExtractoAI Pro", layout="wide")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# 2. Sidebar (Your Name Highlight)
with st.sidebar:
    st.title("📑 ExtractoAI")
    st.success("Developer: **[YOUR NAME]**") # Change this to your name!
    st.info("Status: Live & Professional")

# 3. Main UI
st.title("AI Document Intelligence")
col_left, col_right = st.columns(2)

with col_left:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col_right:
    if uploaded_file and st.button("🚀 Extract Data"):
        with st.spinner("AI is thinking..."):
            prompt = "Return ONLY JSON: {'merchant': '', 'date': '', 'total': 0, 'items': [{'name': '', 'price': 0}]}"
            response = model.generate_content([prompt, img])
            
            # Clean and Show Data
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            st.write(f"**Shop:** {data['merchant']} | **Date:** {data['date']}")
            df = pd.DataFrame(data['items'])
            edited_df = st.data_editor(df, use_container_width=True) # Editable Table
            
            # Download Button

            st.download_button("📥 Download Excel", edited_df.to_csv().encode('utf-8'), "data.csv")


