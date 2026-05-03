import streamlit as st
import tempfile
import os

from analysis.multi_corner import main_pipeline

st.title("Adaptive PVT Corner Reduction Tool")

st.write("Upload STA timing reports to analyze and reduce redundant corners.")

uploaded_files = st.file_uploader(
    "Upload STA Reports",
    accept_multiple_files=True
)

if uploaded_files:
    temp_paths = []

    # Save uploaded files temporarily
    for file in uploaded_files:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".rpt")
        temp_path.write(file.getvalue())   # 🔥 IMPORTANT FIX
        temp_path.close()

        temp_paths.append(temp_path.name)