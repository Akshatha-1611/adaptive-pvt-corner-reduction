import streamlit as st
import tempfile

from analysis.multi_corner import main_pipeline
from ml_models.corner_predictor import train_model, predict_importance
from analysis.correlation import compute_vector_correlation, align_paths

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="PVT Corner Reduction", layout="wide")

# -------------------- SIDEBAR --------------------
st.sidebar.title(" Settings")
st.sidebar.write("Adaptive PVT Corner Reduction Dashboard")

# -------------------- TITLE --------------------
st.title(" Adaptive PVT Corner Reduction Tool")
st.markdown("Analyze and reduce redundant STA PVT corners using intelligent automation.")

# -------------------- FILE UPLOAD --------------------
uploaded_files = st.file_uploader(
    " Upload STA Reports",
    accept_multiple_files=True
)

if uploaded_files:

    temp_paths = []
    file_name_map = {}

    # -------------------- SAVE FILES --------------------
    for file in uploaded_files:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        temp_path.write(file.getvalue())
        temp_path.close()

        temp_paths.append(temp_path.name)

        key = temp_path.name.split("\\")[-1].split(".")[0]
        file_name_map[key] = file.name.replace(".txt", "")

    # -------------------- RUN PIPELINE --------------------
    results, selected = main_pipeline(temp_paths)

    # -------------------- FIX NAMES --------------------
    new_results = {}
    for key, data in results.items():
        original_name = file_name_map.get(key, key)
        new_results[original_name] = data

    results = new_results
    selected = [file_name_map.get(s, s) for s in selected]

    # -------------------- SUMMARY --------------------
    st.markdown("---")
    col1, col2 = st.columns(2)

    col1.metric("Total Corners", len(results))
    col2.metric("Selected Corners", len(selected))

    # -------------------- SELECTED CORNERS --------------------
    st.markdown("###  Selected Corners")
    cols = st.columns(len(selected))

    for i, c in enumerate(selected):
        cols[i].success(c)

    # -------------------- METRICS TABLE --------------------
    st.markdown("###  Corner Metrics")

    corners = list(results.keys())
    wns = [results[c]["metrics"]["WNS"] for c in corners]
    tns = [results[c]["metrics"]["TNS"] for c in corners]

    # -------------------- INTERACTIVE BAR CHART --------------------
    st.markdown("###  WNS vs TNS (Interactive)")

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=corners,
        y=wns,
        name="WNS"
    ))

    fig_bar.add_trace(go.Bar(
        x=corners,
        y=tns,
        name="TNS"
    ))

    fig_bar.update_layout(
        barmode='group',
        title="Corner Timing Metrics",
        xaxis_title="Corners",
        yaxis_title="Slack Values"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------- CORRELATION HEATMAP --------------------
    st.markdown("###  Correlation Heatmap (Interactive)")

    aligned_vectors = align_paths(results)
    names, matrix = compute_vector_correlation(aligned_vectors)

    matrix_np = np.array(matrix)

    fig_heatmap = px.imshow(
        matrix_np,
        x=names,
        y=names,
        text_auto=True,
        aspect="auto",
        title="Corner Correlation Matrix"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # -------------------- DETAILED VIEW --------------------
    st.markdown("###  Detailed Corner Data")

    for corner, data in results.items():
        with st.expander(f"{corner}"):
            st.write("Metrics:", data["metrics"])
            st.write("Paths:", data["paths"])
    
    # -------------------- ML PREDICTION --------------------
    st.markdown("###  ML-Based Corner Importance Prediction")

    model, _ = train_model(results, selected)
    predictions = predict_importance(model, results)

    for corner, pred in predictions.items():
        decision = pred["decision"]
        confidence = pred["confidence"]

        if decision == "KEEP":
            st.success(f"{corner} → {decision} (Confidence: {confidence})")
        else:
            st.warning(f"{corner} → {decision} (Confidence: {confidence})")

    # -------------------- FOOTER --------------------
    st.markdown("---")
    st.caption("Built with Python + Streamlit | VLSI STA Optimization Project")