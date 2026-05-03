from analysis.correlation import compute_vector_correlation
from visualization.plotter import plot_correlation_matrix, plot_metrics
from analysis.validation import validate_results
from optimizer.corner_selector import select_from_clusters
from analysis.clustering import cluster_corners
from analysis.correlation import align_paths

from parser.timing_parser import parse_timing_report, compute_metrics
import os


def compute_metrics_from_dict(path_dict):
    slacks = list(path_dict.values())

    if not slacks:
        print("WARNING: Empty slack list detected")
        return {"WNS": 0, "TNS": 0}

    wns = min(slacks)
    tns = sum(s for s in slacks if s < 0)

    return {
        "WNS": wns,
        "TNS": tns
    }


def parse_all_corners():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_dir = os.path.join(BASE_DIR, "data", "reports")

    corner_results = {}

    for file in os.listdir(report_dir):
        if file.endswith(".txt"):
            corner_name = file.replace(".txt", "")
            file_path = os.path.join(report_dir, file)

            path_dict = parse_timing_report(file_path)
            metrics = compute_metrics_from_dict(path_dict)

            corner_results[corner_name] = {
                "paths": path_dict,
                "metrics": metrics
            }

    return corner_results


def main_pipeline(file_paths):
    results = {}

    for file_path in file_paths:
        corner_name = file_path.split("\\")[-1].split(".")[0]

        path_dict = parse_timing_report(file_path)

        metrics = compute_metrics_from_dict(path_dict)

        results[corner_name] = {
            "paths": path_dict,
            "metrics": metrics
        }

    aligned_vectors = align_paths(results)
    clusters = cluster_corners(aligned_vectors)
    selected = select_from_clusters(clusters, results)

    return results, selected


if __name__ == "__main__":
    results = parse_all_corners()

    aligned_vectors = align_paths(results)
    clusters = cluster_corners(aligned_vectors)

    names, matrix = compute_vector_correlation(aligned_vectors)

    plot_correlation_matrix(names, matrix)
    plot_metrics(results)

    selected = select_from_clusters(clusters, results)

    validate_results(results, selected)