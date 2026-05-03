from visualization.plotter import plot_correlation_matrix, plot_metrics
from analysis.validation import validate_results
from optimizer.corner_selector import select_from_clusters
from analysis.clustering import cluster_corners
from analysis.correlation import align_paths
from analysis.correlation import (
    extract_slack_vectors,
    compute_vector_correlation,
    find_redundant_corners
)
from parser.timing_parser import parse_timing_report, compute_metrics
import os

def parse_all_corners():
    # Get project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    report_dir = os.path.join(BASE_DIR, "data", "reports")

    corner_results = {}

    for file in os.listdir(report_dir):
        if file.endswith(".txt"):
            corner_name = file.replace(".txt", "")
            file_path = os.path.join(report_dir, file)

            path_dict = parse_timing_report(file_path)

            # Convert dictionary → list for metrics function
            paths = [{"slack": v} for v in path_dict.values()]

            metrics = compute_metrics(paths)

            corner_results[corner_name] = {
            "paths": path_dict,   #  store dictionary
            "metrics": metrics
            }

    return corner_results


if __name__ == "__main__":
    results = parse_all_corners()

    for corner, data in results.items():
        print(f"\nCorner: {corner}")
        print("Metrics:", data["metrics"])

    # New flow
    aligned_vectors = align_paths(results)

    # Step 1: Clustering
    clusters = cluster_corners(aligned_vectors)

    # Step 2: Correlation
    names, matrix = compute_vector_correlation(aligned_vectors)

    # step 3: Visualization
    plot_correlation_matrix(names, matrix)
    plot_metrics(results)

    # Step 4: Optimization
    selected = select_from_clusters(clusters, results)

    # Step 5: Validation
    validate_results(results, selected)