def select_from_clusters(clusters, corner_results):
    print("\n--- Optimization: Cluster-Based Selection ---\n")

    selected = []

    # Step 1: Find global worst-case corner
    worst_corner = min(
        corner_results,
        key=lambda c: corner_results[c]["metrics"]["WNS"]
    )

    print(f"Global worst-case corner: {worst_corner}")

    # Step 2: Process each cluster
    for cluster_id, members in clusters.items():
        print(f"\nCluster {cluster_id}: {members}")

        # If worst corner is inside cluster → keep it
        if worst_corner in members:
            print(f"→ Keeping worst-case corner: {worst_corner}")
            selected.append(worst_corner)
            continue

        # Otherwise select representative (worst WNS in cluster)
        best = min(
            members,
            key=lambda c: corner_results[c]["metrics"]["WNS"]
        )

        print(f"→ Selected representative: {best}")
        selected.append(best)

    print("\nFinal Optimized Corner Set:", selected)

    return selected