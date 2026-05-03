import numpy as np
from sklearn.cluster import KMeans


def prepare_data(vectors):
    corner_names = list(vectors.keys())
    data = np.array([vectors[c] for c in corner_names])
    return corner_names, data


def find_optimal_clusters(data, max_k=5):
    from sklearn.metrics import silhouette_score

    n_samples = len(data)

    #  Handle small datasets safely
    if n_samples <= 2:
        print("Not enough samples for clustering. Using 1 cluster.")
        return 1

    best_k = 2
    best_score = -1

    #  STRICT LIMIT: k < n_samples
    max_possible_k = min(max_k, n_samples - 1)

    for k in range(2, max_possible_k + 1):
        try:
            kmeans = KMeans(n_clusters=k, random_state=0)
            labels = kmeans.fit_predict(data)

            #  Skip invalid cases
            if len(set(labels)) == n_samples:
                continue

            score = silhouette_score(data, labels)

            if score > best_score:
                best_score = score
                best_k = k

        except Exception as e:
            print(f"Skipping k={k} due to error: {e}")
            continue

    return best_k


def cluster_corners(vectors):
    print("\n--- Clustering Corners ---\n")

    corner_names, data = prepare_data(vectors)

    k = find_optimal_clusters(data)
    print(f"Optimal clusters: {k}")

    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(data)

    clusters = {}

    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(corner_names[i])

    for cid, members in clusters.items():
        print(f"Cluster {cid}: {members}")

    return clusters