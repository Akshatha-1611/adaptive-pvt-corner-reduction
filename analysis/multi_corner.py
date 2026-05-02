from analysis.correlation import compute_wns_correlation, find_redundant_corners
from analysis.correlation import compute_wns_correlation
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

            paths = parse_timing_report(file_path)
            metrics = compute_metrics(paths)

            corner_results[corner_name] = {
                "paths": paths,
                "metrics": metrics
            }

    return corner_results


if __name__ == "__main__":
    results = parse_all_corners()

    for corner, data in results.items():
        print(f"\nCorner: {corner}")
        print("Metrics:", data["metrics"])

    # Correlation
    names, matrix = compute_wns_correlation(results)

    # Redundancy detection
    find_redundant_corners(names, matrix)