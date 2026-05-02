import numpy as np

def extract_slack_vectors(corner_results):
    vectors = {}
    
    for corner, data in corner_results.items():
        slacks = [p["slack"] for p in data["paths"]]
        vectors[corner] = np.array(slacks)
    
    return vectors


def compute_vector_correlation(vectors):
    print("\n--- Path-Aligned Correlation Matrix ---\n")

    corner_names = list(vectors.keys())
    matrix = []

    for i in range(len(corner_names)):
        row = []
        for j in range(len(corner_names)):
            v1 = vectors[corner_names[i]]
            v2 = vectors[corner_names[j]]

            # Handle unequal lengths
            min_len = min(len(v1), len(v2))
            v1_trim = v1[:min_len]
            v2_trim = v2[:min_len]

            if len(v1_trim) == 0:
                corr = 0
            else:
                corr = np.corrcoef(v1_trim, v2_trim)[0, 1]

            row.append(float(round(corr, 3)))
        matrix.append(row)

    print("Corners:", corner_names)
    for i, row in enumerate(matrix):
        print(corner_names[i], ":", row)

    return corner_names, matrix


def find_redundant_corners(corner_names, matrix, threshold=0.95):
    print("\n--- Redundant Corners (Advanced) ---\n")

    redundant = set()

    for i in range(len(corner_names)):
        for j in range(i + 1, len(corner_names)):
            if matrix[i][j] >= threshold:
                print(f"{corner_names[i]} ≈ {corner_names[j]} (corr: {matrix[i][j]})")
                redundant.add(corner_names[j])

    print("\nSuggested removal:", list(redundant))
    return redundant

def align_paths(corner_results):
    print("\n--- Aligning Paths Across Corners ---")

    # Step 1: collect all path sets
    path_sets = []
    for data in corner_results.values():
        path_sets.append(set(data["paths"].keys()))

    # Step 2: find common paths
    common_paths = set.intersection(*path_sets)

    print("Common paths:", common_paths)

    # Step 3: build aligned vectors
    aligned_vectors = {}

    for corner, data in corner_results.items():
        aligned_vectors[corner] = []

        for p in common_paths:
            aligned_vectors[corner].append(data["paths"][p])

    return aligned_vectors