def select_optimal_corners(corner_results, corr_names, corr_matrix, threshold=0.95):
    print("\n--- Final Corner Selection ---\n")

    # Step 1: find worst-case corner
    worst_corner = min(
        corner_results,
        key=lambda c: corner_results[c]["metrics"]["WNS"]
    )

    print(f"Worst-case corner: {worst_corner}")

    selected = set([worst_corner])
    removed = set()

    # Step 2: remove highly correlated
    for i in range(len(corr_names)):
        for j in range(i + 1, len(corr_names)):
            if corr_matrix[i][j] >= threshold:
                c1 = corr_names[i]
                c2 = corr_names[j]

                if corner_results[c1]["metrics"]["WNS"] <= corner_results[c2]["metrics"]["WNS"]:
                    keep, drop = c1, c2
                else:
                    keep, drop = c2, c1

                selected.add(keep)
                removed.add(drop)

    # Step 3: include remaining
    for c in corner_results:
        if c not in removed:
            selected.add(c)

    print("Selected Corners:", list(selected))
    print("Removed Corners:", list(removed))

    return selected