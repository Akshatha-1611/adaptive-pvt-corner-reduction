import streamlit as st
import tempfile
import os

from analysis.multi_corner import main_pipeline
from ml_models.corner_predictor import (
    train_model,
    predict_importance
)

from analysis.correlation import (
    compute_vector_correlation,
    align_paths
)

import plotly.graph_objects as go
import plotly.express as px
import numpy as np


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Adaptive PVT Corner Reduction",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM DARK THEME + ANIMATIONS
# =====================================================
st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }

    /* TITLES */
    h1, h2, h3 {
        color: #58A6FF;
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 12px;
    }

    /* DATAFRAME */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }

    /* BUTTONS */
    .stButton > button {
        background-color: #238636;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #2EA043;
        transform: scale(1.02);
    }

    /* EXPANDERS */
    .streamlit-expanderHeader {
        background-color: #161B22;
        border-radius: 10px;
    }

    /* ANIMATION */
    .fadeIn {
        animation: fadeInAnimation 1s ease-in;
    }

    @keyframes fadeInAnimation {
        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title(" Dashboard Settings")

st.sidebar.markdown(
    """
    ### Features
    - Multi-Corner STA Analysis
    - Correlation-Based Reduction
    - ML-Assisted Prediction
    - Interactive Visualization
    - PVT Optimization
    """
)

st.sidebar.info(
    "Adaptive PVT Corner Reduction Framework"
)


# =====================================================
# HERO SECTION
# =====================================================
st.markdown(
    """
    <div class="fadeIn">

    #  Adaptive PVT Corner Reduction Tool

    ### Intelligent STA Corner Optimization Framework

    Analyze STA timing reports, detect redundant corners,
    visualize timing relationships, and perform ML-assisted
    corner selection.

    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# ARCHITECTURE DIAGRAM
# =====================================================
st.markdown("##  Framework Architecture")

architecture_html = """
<div style="
display:flex;
justify-content:center;
align-items:center;
gap:20px;
flex-wrap:wrap;
margin-top:20px;
margin-bottom:30px;
">

<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
width:180px;
text-align:center;
animation: fadeInAnimation 1s ease-in;
">
<h3> STA Reports</h3>
<p>Upload Timing Reports</p>
</div>

<div style="font-size:40px;">➡️</div>

<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
width:180px;
text-align:center;
animation: fadeInAnimation 1.3s ease-in;
">
<h3>🔍 Analysis Engine</h3>
<p>Path Correlation & Metrics</p>
</div>

<div style="font-size:40px;">➡️</div>

<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
width:180px;
text-align:center;
animation: fadeInAnimation 1.6s ease-in;
">
<h3> ML Prediction</h3>
<p>Corner Importance Estimation</p>
</div>

<div style="font-size:40px;">➡️</div>

<div style="
background:#161B22;
padding:20px;
border-radius:15px;
border:1px solid #30363D;
width:180px;
text-align:center;
animation: fadeInAnimation 1.9s ease-in;
">
<h3> Visualization</h3>
<p>Interactive Analytics Dashboard</p>
</div>

</div>
"""

st.markdown(
    architecture_html,
    unsafe_allow_html=True
)


# =====================================================
# FILE UPLOAD
# =====================================================
uploaded_files = st.file_uploader(
    " Upload STA Timing Reports",
    accept_multiple_files=True,
    type=["txt", "rpt"]
)


# =====================================================
# MAIN ANALYSIS
# =====================================================
if uploaded_files:

    temp_paths = []
    file_name_map = {}

    # -------------------------------------------------
    # SAVE FILES
    # -------------------------------------------------
    for file in uploaded_files:

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        )

        temp_file.write(file.getvalue())
        temp_file.close()

        temp_paths.append(temp_file.name)

        clean_name = (
            os.path.basename(file.name)
            .replace(".txt", "")
            .replace(".rpt", "")
        )

        temp_key = os.path.basename(temp_file.name).split(".")[0]

        file_name_map[temp_key] = clean_name

    # -------------------------------------------------
    # RUN PIPELINE
    # -------------------------------------------------
    results, selected = main_pipeline(temp_paths)

    # -------------------------------------------------
    # FIX CORNER NAMES
    # -------------------------------------------------
    renamed_results = {}

    for key, data in results.items():

        clean_key = os.path.basename(key).split(".")[0]

        original_name = file_name_map.get(
            clean_key,
            clean_key
        )

        renamed_results[original_name] = data

    results = renamed_results

    selected = [
        file_name_map.get(s, os.path.basename(s))
        for s in selected
    ]

    # =================================================
    # SUMMARY
    # =================================================
    st.markdown("---")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Corners",
        len(results)
    )

    col2.metric(
        "Selected Corners",
        len(selected)
    )

    # =================================================
    # SELECTED CORNERS
    # =================================================
    st.markdown("##  Selected Optimal Corners")

    cols = st.columns(max(len(selected), 1))

    for i, corner in enumerate(selected):
        cols[i].success(corner)

    # =================================================
    # METRICS
    # =================================================
    corners = list(results.keys())

    wns = [
        results[c]["metrics"]["WNS"]
        for c in corners
    ]

    tns = [
        results[c]["metrics"]["TNS"]
        for c in corners
    ]

    # =================================================
    # DATAFRAME
    # =================================================
    st.markdown("##  Corner Metrics")

    metrics_data = {
        "Corner": corners,
        "WNS": wns,
        "TNS": tns
    }

    st.dataframe(
        metrics_data,
        use_container_width=True
    )

    # =================================================
    # BAR CHART
    # =================================================
    st.markdown("##  WNS vs TNS Analysis")

    fig_bar = go.Figure()

    fig_bar.add_trace(
        go.Bar(
            x=corners,
            y=wns,
            name="WNS"
        )
    )

    fig_bar.add_trace(
        go.Bar(
            x=corners,
            y=tns,
            name="TNS"
        )
    )

    fig_bar.update_layout(
        title="Corner Timing Metrics",
        xaxis_title="Corners",
        yaxis_title="Slack Values",
        barmode="group",
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # =================================================
    # HEATMAP
    # =================================================
    st.markdown("##  Correlation Heatmap")

    aligned_vectors = align_paths(results)

    names, matrix = compute_vector_correlation(
        aligned_vectors
    )

    matrix_np = np.array(matrix)

    fig_heatmap = px.imshow(
        matrix_np,
        x=names,
        y=names,
        text_auto=True,
        aspect="auto",
        title="Corner Correlation Matrix",
        color_continuous_scale="Viridis"
    )

    fig_heatmap.update_layout(
        height=600,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

    # =================================================
    # DETAILED DATA
    # =================================================
    st.markdown("##  Detailed Corner Data")

    for corner, data in results.items():

        with st.expander(f" {corner}"):

            st.write(
                "### Metrics"
            )

            st.json(data["metrics"])

            st.write(
                "### Paths"
            )

            st.json(data["paths"])

    # =================================================
    # ML PREDICTIONS
    # =================================================
    st.markdown(
        "##  ML-Based Corner Importance Prediction"
    )

    model, _ = train_model(
        results,
        selected
    )

    predictions = predict_importance(
        model,
        results
    )

    for corner, pred in predictions.items():

        decision = pred["decision"]
        confidence = pred["confidence"]

        message = (
            f"{corner} → "
            f"{decision} "
            f"(Confidence: {confidence})"
        )

        if decision == "KEEP":
            st.success(message)
        else:
            st.warning(message)

    # =================================================
    # FOOTER
    # =================================================
    st.markdown("---")

    st.caption(
        "Built with Python + Streamlit | "
        "Adaptive STA PVT Corner Reduction Framework"
    )