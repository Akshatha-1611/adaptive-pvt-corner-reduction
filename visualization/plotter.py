import matplotlib.pyplot as plt
import numpy as np


def plot_correlation_matrix(names, matrix):
    print("\n--- Generating Correlation Heatmap ---")

    matrix = np.array(matrix)

    plt.figure()
    plt.imshow(matrix)

    plt.xticks(range(len(names)), names, rotation=45)
    plt.yticks(range(len(names)), names)

    plt.title("Corner Correlation Heatmap")
    plt.colorbar()

    plt.tight_layout()
    plt.savefig("results/correlation_heatmap.png")
    plt.show()


def plot_metrics(corner_results):
    print("\n--- Plotting WNS and TNS ---")

    corners = list(corner_results.keys())
    wns = [corner_results[c]["metrics"]["WNS"] for c in corners]
    tns = [corner_results[c]["metrics"]["TNS"] for c in corners]

    x = np.arange(len(corners))

    plt.figure()
    plt.bar(x - 0.2, wns, 0.4, label="WNS")  
    plt.bar(x + 0.2, tns, 0.4, label="TNS")

    plt.legend()

    plt.xticks(x, corners)
    plt.title("WNS vs TNS per Corner")

    plt.tight_layout()
    plt.savefig("results/metrics_comparison.png")
    plt.show()