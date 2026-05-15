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
    layout="wide"
)


# =====================================================
# CUSTOM DARK UI
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #0D1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #161B22;
}

h1, h2, h3, h4 {
    color: white;
}

.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #2EA043;
}

.metric-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #30363D;
}

.arch-box {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
    font-weight: 600;
}

.arch-box:hover {
    transform: scale(1.03);
    border-color: #58A6FF;
}

.arrow {
    text-align: center;
    font-size: 28px;
    color: #58A6FF;
    margin-top: -5px;
    margin-bottom: -5px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Configuration")
st.sidebar.write(
    "Adaptive PVT Corner Reduction Dashboard"
)


# =====================================================
# TITLE
# =====================================================

st.title("Adaptive PVT Corner Reduction Tool")

st.markdown(
    """
    Analyze and reduce redundant STA PVT corners
    using intelligent automation and ML-assisted
    corner selection.
    """
)


# =====================================================
# DEMO MODE PANEL
# =====================================================

st.markdown(
    """
    <div style="
        background-color:#161B22;
        padding:18px;
        border-radius:12px;
        border:1px solid #30363D;
        margin-bottom:20px;
    ">

    <h4 style="margin-bottom:5px;">
    No STA reports?
    </h4>

    <p style="color:#B0B0B0;">
    Launch the application using built-in
    sample timing reports.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

demo_mode = st.button("Run Demo Mode")


# =====================================================
# ARCHITECTURE VIEW
# =====================================================

st.markdown("## System Architecture")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="arch-box">
    STA Report Input
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="arch-box">
    Correlation Engine
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="arch-box">
    Corner Reduction
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="arch-box">
    ML Prediction
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='arrow'>↓</div>", unsafe_allow_html=True)


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_files = st.file_uploader(
    "Upload STA Reports",
    accept_multiple_files=True
)


# =====================================================
# MAIN EXECUTION
# =====================================================

if uploaded_files or demo_mode:

    temp_paths = []
    file_name_map = {}

    # =====================================================
    # DEMO MODE FILES
    # =====================================================

    if demo_mode:

        demo_files = [
            "temp_reports/ssg_wc.txt",
            "temp_reports/tt_nominal.txt",
            "temp_reports/ff_fast.txt",
            "temp_reports/low_voltage.txt"
        ]

        for path in demo_files:

            temp_paths.append(path)

            clean_name = (
                os.path.basename(path)
                .replace(".txt", "")
            )

            temp_key = (
                os.path.basename(path)
                .split(".")[0]
            )

            file_name_map[temp_key] = clean_name

    # =====================================================
    # USER UPLOAD FILES
    # =====================================================

    if uploaded_files:

        for file in uploaded_files:

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".txt"
            )

            temp_file.write(file.getvalue())
            temp_file.close()

            temp_paths.append(temp_file.name)

            clean_name = (
                file.name
                .replace(".txt", "")
                .replace(".rpt", "")
            )

            temp_key = (
                os.path.basename(temp_file.name)
                .split(".")[0]
            )

            file_name_map[temp_key] = clean_name

    # =====================================================
    # RUN PIPELINE
    # =====================================================

    results, selected = main_pipeline(temp_paths)

    # =====================================================
    # FIX FILE NAMES
    # =====================================================

    renamed_results = {}

    for key, data in results.items():

        clean_key = (
            os.path.basename(key)
            .split(".")[0]
        )

        original_name = file_name_map.get(
            clean_key,
            clean_key
        )

        renamed_results[original_name] = data

    results = renamed_results

    selected = [
        file_name_map.get(
            os.path.basename(s).split(".")[0],
            os.path.basename(s).split(".")[0]
        )
        for s in selected
    ]

    # =====================================================
    # SUMMARY
    # =====================================================

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Corners",
            len(results)
        )

    with col2:
        st.metric(
            "Selected Corners",
            len(selected)
        )

    # =====================================================
    # SELECTED CORNERS
    # =====================================================

    st.markdown("## Selected Optimal Corners")

    cols = st.columns(len(selected))

    for i, corner in enumerate(selected):
        cols[i].success(corner)

    # =====================================================
    # METRICS
    # =====================================================

    corners = list(results.keys())

    wns = [
        results[c]["metrics"]["WNS"]
        for c in corners
    ]

    tns = [
        results[c]["metrics"]["TNS"]
        for c in corners
    ]

    # =====================================================
    # BAR CHART
    # =====================================================

    st.markdown("## WNS vs TNS")

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
        barmode="group",
        title="Corner Timing Metrics",
        xaxis_title="Corners",
        yaxis_title="Slack Values",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # =====================================================
    # CORRELATION HEATMAP
    # =====================================================

    st.markdown("## Correlation Heatmap")

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
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )

    # =====================================================
    # DETAILED DATA
    # =====================================================

    st.markdown("## Detailed Corner Data")

    for corner, data in results.items():

        with st.expander(corner):

            st.write(
                "Metrics:",
                data["metrics"]
            )

            st.write(
                "Paths:",
                data["paths"]
            )

    # =====================================================
    # ML PREDICTION
    # =====================================================

    st.markdown(
        "## ML-Based Corner Importance Prediction"
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

        if decision == "KEEP":

            st.success(
                f"{corner} → {decision} "
                f"(Confidence: {confidence})"
            )

        else:

            st.warning(
                f"{corner} → {decision} "
                f"(Confidence: {confidence})"
            )

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("---")

    st.caption(
        "Built using Python, Streamlit, Plotly "
        "and ML-assisted STA analytics"
    )