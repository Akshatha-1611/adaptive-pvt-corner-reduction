def compute_global_metrics(corner_results, selected_corners=None):
    """
    Compute worst-case WNS and total TNS
    """
    if selected_corners:
        corners = selected_corners
    else:
        corners = corner_results.keys()

    all_wns = []
    total_tns = 0

    for c in corners:
        metrics = corner_results[c]["metrics"]

        all_wns.append(metrics["WNS"])
        total_tns += metrics["TNS"]

    global_wns = min(all_wns)

    return global_wns, total_tns


def validate_results(corner_results, selected_corners):
    print("\n--- Validation Phase ---\n")

    # Full set
    full_wns, full_tns = compute_global_metrics(corner_results)

    # Reduced set
    red_wns, red_tns = compute_global_metrics(corner_results, selected_corners)

    print("Full Set Metrics:")
    print(f"WNS: {full_wns}, TNS: {full_tns}")

    print("\nReduced Set Metrics:")
    print(f"WNS: {red_wns}, TNS: {red_tns}")

    # Differences
    delta_wns = abs(full_wns - red_wns)
    delta_tns = abs(full_tns - red_tns)

    print("\nDifferences:")
    print(f"ΔWNS: {delta_wns}")
    print(f"ΔTNS: {delta_tns}")

    # Simple validation check
    if delta_wns < 0.05:
        print("\n VALIDATION PASSED")
    else:
        print("\n VALIDATION FAILED")

    return delta_wns, delta_tns

def get_validation_results(corner_results, selected_corners):
    full_wns, full_tns = compute_global_metrics(corner_results)
    red_wns, red_tns = compute_global_metrics(corner_results, selected_corners)

    delta_wns = abs(full_wns - red_wns)
    delta_tns = abs(full_tns - red_tns)

    return {
        "full": {"WNS": full_wns, "TNS": full_tns},
        "reduced": {"WNS": red_wns, "TNS": red_tns},
        "delta": {"WNS": delta_wns, "TNS": delta_tns}
    }