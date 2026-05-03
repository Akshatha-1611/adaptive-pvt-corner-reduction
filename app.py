import streamlit as st
import tempfile

from analysis.multi_corner import main_pipeline
from visualization.plotter import plot_correlation_matrix, plot_metrics
from analysis.correlation import compute_vector_correlation, align_paths

st.title(" Adaptive PVT Corner Reduction Tool")

uploaded_files = st.file_uploader(
    "Upload STA Reports",
    accept_multiple_files=True
)

if uploaded_files:

    temp_paths = []
    file_name_map = {}

    #  STEP 1: Save files + create mapping
    for file in uploaded_files:
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        temp_path.write(file.getvalue())
        temp_path.close()

        temp_paths.append(temp_path.name)

        # IMPORTANT: match pipeline naming (tmpxxxx)
        key = temp_path.name.split("\\")[-1].split(".")[0]
        file_name_map[key] = file.name.replace(".txt", "")

    #  STEP 2: Run pipeline
    results, selected = main_pipeline(temp_paths)

    #  STEP 3: Fix names
    new_results = {}

    for key, data in results.items():
        original_name = file_name_map.get(key, key)
        new_results[original_name] = data

    results = new_results
    selected = [file_name_map.get(s, s) for s in selected]

    #  STEP 4: Display summary
    st.markdown("---")
    st.header(" Summary")

    col1, col2 = st.columns(2)
    col1.metric("Total Corners", len(results))
    col2.metric("Selected Corners", len(selected))

    #  STEP 5: Selected corners
    st.markdown("###  Selected Corners")
    for c in selected:
        st.success(c)

    #  STEP 6: Metrics
    st.markdown("###  Corner Metrics")
    for corner, data in results.items():
        with st.expander(corner):
            st.write(data["metrics"])

    #  STEP 7: Visualization (ONLY ONCE)
    aligned_vectors = align_paths(results)
    names, matrix = compute_vector_correlation(aligned_vectors)

    plot_correlation_matrix(names, matrix)
    plot_metrics(results)

    st.markdown("###  Correlation Heatmap")
    st.image("results/correlation_heatmap.png")

    st.markdown("###  WNS vs TNS")
    st.image("results/metrics_comparison.png")