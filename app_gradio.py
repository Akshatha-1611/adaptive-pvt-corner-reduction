import gradio as gr
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from analysis.multi_corner import main_pipeline
from analysis.correlation import (
    align_paths,
    compute_vector_correlation
)
from ml_models.corner_predictor import (
    train_model,
    predict_importance
)


# ------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ------------------------------------------------------
def run_analysis(files):

    if not files:
        return (
            pd.DataFrame(),
            None,
            None,
            "",
            ""
        )

    # ------------------------------------------------------
    # CREATE TEMP DIRECTORY
    # ------------------------------------------------------
    os.makedirs("temp_reports", exist_ok=True)

    temp_paths = []
    file_name_map = {}

    # ------------------------------------------------------
    # SAVE FILES
    # ------------------------------------------------------
    for file in files:

        file_name = os.path.basename(file.name)

        save_path = os.path.join(
            "temp_reports",
            file_name
        )

        with open(file.name, "rb") as src:
            content = src.read()

        with open(save_path, "wb") as dst:
            dst.write(content)

        temp_paths.append(save_path)

        clean_name = (
            file_name
            .replace(".txt", "")
            .replace(".rpt", "")
        )

        file_name_map[save_path] = clean_name

    # ------------------------------------------------------
    # RUN MAIN PIPELINE
    # ------------------------------------------------------
    results, selected = main_pipeline(temp_paths)

    # ------------------------------------------------------
    # CLEAN CORNER NAMES
    # ------------------------------------------------------
    renamed_results = {}

    for key, data in results.items():

        clean_name = file_name_map.get(key, key)

        renamed_results[clean_name] = data

    results = renamed_results

    selected = [
        file_name_map.get(s, s)
        for s in selected
    ]

    # ------------------------------------------------------
    # EXTRACT METRICS
    # ------------------------------------------------------
    corners = list(results.keys())

    wns = [
        results[c]["metrics"]["WNS"]
        for c in corners
    ]

    tns = [
        results[c]["metrics"]["TNS"]
        for c in corners
    ]

    # ------------------------------------------------------
    # CREATE METRICS TABLE
    # ------------------------------------------------------
    metrics_df = pd.DataFrame({
        "Corner": corners,
        "WNS": wns,
        "TNS": tns
    })

    # ------------------------------------------------------
    # BAR CHART
    # ------------------------------------------------------
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
        title="WNS vs TNS per Corner",
        barmode="group",
        height=500
    )

    # ------------------------------------------------------
    # CORRELATION HEATMAP
    # ------------------------------------------------------
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
        title="Corner Correlation Matrix"
    )

    fig_heatmap.update_layout(height=600)

    # ------------------------------------------------------
    # ML PREDICTION
    # ------------------------------------------------------
    model, _ = train_model(results, selected)

    predictions = predict_importance(
        model,
        results
    )

    prediction_text = ""

    for corner, pred in predictions.items():

        prediction_text += (
            f"{corner} → "
            f"{pred['decision']} "
            f"(Confidence: {pred['confidence']})\n"
        )

    # ------------------------------------------------------
    # SELECTED CORNERS TEXT
    # ------------------------------------------------------
    selected_text = "\n".join(selected)

    # ------------------------------------------------------
    # RETURN EVERYTHING
    # ------------------------------------------------------
    return (
        metrics_df,
        fig_bar,
        fig_heatmap,
        selected_text,
        prediction_text
    )


# ------------------------------------------------------
# GRADIO UI
# ------------------------------------------------------
with gr.Blocks(
    title="Adaptive PVT Corner Reduction"
) as demo:

    gr.Markdown(
        """
        # Adaptive PVT Corner Reduction Tool

        Upload STA timing reports to:

        - Perform correlation analysis
        - Detect redundant corners
        - Optimize corner selection
        - Run ML-based prediction
        """
    )

    # ------------------------------------------------------
    # FILE INPUT
    # ------------------------------------------------------
    file_input = gr.File(
        file_count="multiple",
        label="Upload STA Reports"
    )

    analyze_button = gr.Button(
        "Run Analysis"
    )

    # ------------------------------------------------------
    # OUTPUTS
    # ------------------------------------------------------
    gr.Markdown("## Selected Optimal Corners")

    selected_output = gr.Textbox(
        lines=5,
        label="Selected Corners"
    )

    gr.Markdown("## Corner Metrics")

    metrics_output = gr.Dataframe(
        label="Timing Metrics"
    )

    gr.Markdown("## WNS vs TNS")

    bar_output = gr.Plot()

    gr.Markdown("## Correlation Heatmap")

    heatmap_output = gr.Plot()

    gr.Markdown("## ML Predictions")

    prediction_output = gr.Textbox(
        lines=10,
        label="ML Corner Prediction"
    )

    # ------------------------------------------------------
    # BUTTON ACTION
    # ------------------------------------------------------
    analyze_button.click(
        fn=run_analysis,
        inputs=file_input,
        outputs=[
            metrics_output,
            bar_output,
            heatmap_output,
            selected_output,
            prediction_output
        ]
    )


# ------------------------------------------------------
# RUN APP
# ------------------------------------------------------
if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )