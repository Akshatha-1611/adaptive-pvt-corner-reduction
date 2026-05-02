import numpy as np

def compute_wns_correlation(corner_results):
    print("\n--- WNS Correlation Matrix ---\n")

    corner_names = list(corner_results.keys())
    wns_values = [corner_results[c]["metrics"]["WNS"] for c in corner_names]

    # Convert to numpy array
    data = np.array(wns_values)

    # Since WNS is 1D, we compare differences manually
    correlation_matrix = []

    for i in range(len(data)):
        row = []
        for j in range(len(data)):
            diff = abs(data[i] - data[j])
            similarity = 1 / (1 + diff)  # simple similarity score
            row.append(round(similarity, 3))
        correlation_matrix.append(row)

    # Print matrix
    print("Corners:", corner_names)
    for i, row in enumerate(correlation_matrix):
        print(corner_names[i], ":", row)

    return corner_names, correlation_matrix

def find_redundant_corners(corner_names, corr_matrix, threshold=0.95):
    print("\n--- Redundant Corners ---\n")

    redundant = set()

    for i in range(len(corner_names)):
        for j in range(i + 1, len(corner_names)):
            if corr_matrix[i][j] >= threshold:
                print(f"{corner_names[i]} ≈ {corner_names[j]} (similarity: {corr_matrix[i][j]})")
                redundant.add(corner_names[j])

    print("\nSuggested corners to remove:", list(redundant))
    return redundant