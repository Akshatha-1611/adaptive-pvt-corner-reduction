def compute_wns_correlation(corner_results):
    print("\nWNS Comparison Across Corners:\n")

    for corner, data in corner_results.items():
        print(f"{corner}: {data['metrics']['WNS']}")