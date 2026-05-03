#  Adaptive PVT Corner Reduction Framework for STA

A **Python-based intelligent framework** to reduce redundant **PVT (Process, Voltage, Temperature) corners** in **Static Timing Analysis (STA)** using data-driven techniques such as correlation, clustering, and optimization.

---

#  Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Solution Approach](#solution-approach)
* [Key Features](#key-features)
* [Project Flow](#project-flow)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Sample Output](#sample-output)
* [Results & Validation](#results--validation)
* [Visualization](#visualization)
* [Future Work](#future-work)
* [Applications](#applications)

---

#  Overview

Static Timing Analysis (STA) is a critical step in VLSI design used to verify timing performance across different operating conditions called **PVT corners**.

However, running STA across all corners:

* Increases runtime significantly
* Leads to redundant analysis
* Slows down design closure

 This project solves that by building an **adaptive system** that intelligently reduces unnecessary corners while preserving timing accuracy.

---

#  Problem Statement

Modern chips are analyzed across multiple PVT corners:

* Slow-Slow (SS)
* Typical-Typical (TT)
* Fast-Fast (FF)
* and many more...

### Issues:

* High computational cost
* Redundant timing analysis
* Increased turnaround time

 Many corners behave similarly and **do not need to be analyzed independently**

---

#  Solution Approach

This framework automates the reduction of redundant corners using:

###  1. Parsing

Extract timing paths and slack values from STA reports

###  2. Metrics Extraction

Compute:

* WNS (Worst Negative Slack)
* TNS (Total Negative Slack)

###  3. Path Alignment

Ensure comparison of **same timing paths across all corners**

###  4. Correlation Analysis

Identify similarity between corners

###  5. Feature Enhancement

Weight critical paths more heavily

###  6. Clustering

Group similar corners using machine learning

###  7. Optimization Engine

Select:

 Worst-case corner (always preserved)
 Representative corners from each cluster

###  8. Validation

Compare reduced set vs full set:

 ΔWNS
 ΔTNS

###  9. Visualization

Generate:

 Correlation heatmaps
 WNS vs TNS graphs

---

#  Key Features

✔ Automated STA report parsing
✔ Path-aligned correlation (accurate comparison)
✔ Feature-weighted analysis
✔ Machine learning-based clustering
✔ Optimization-driven corner selection
✔ Validation framework for accuracy
✔ Visualization support

---

#  Project Flow

```
1. Parse STA Reports
2. Extract Metrics (WNS, TNS)
3. Align Paths Across Corners
4. Compute Correlation
5. Apply Feature Weighting
6. Perform Clustering
7. Optimize Corner Selection
8. Validate Results
9. Generate Visualizations
```

---

#  Project Structure

```
pvt_project/
│
├── analysis/
│   ├── multi_corner.py        # Main pipeline
│   ├── correlation.py        # Correlation + alignment
│   ├── clustering.py         # KMeans clustering
│   ├── validation.py         # Accuracy validation
│
├── optimizer/
│   ├── corner_selector.py    # Optimization logic
│
├── parser/
│   ├── timing_parser.py      # STA report parser
│
├── visualization/
│   ├── plotter.py            # Graphs & plots
│
├── data/
│   ├── reports/              # Input STA reports
│
├── results/                  # Output plots
│
├── main.py
├── requirements.txt
└── README.md
```

---

#  Usage

```bash
python -m analysis.multi_corner
```

---

#  Sample Output

```
--- Clustering Corners ---

Cluster 0: ['corner_ss', 'corner_tt']
Cluster 1: ['corner_ff']

--- Optimization ---

Global worst-case corner: corner_ss

Final Optimized Corner Set:
['corner_ss', 'corner_ff']
```

---

#  Results & Validation

| Metric | Full Set | Reduced Set | Difference |
| ------ | -------- | ----------- | ---------- |
| WNS    | -0.20    | -0.20       | 0.00       |
| TNS    | -0.56    | -0.30       | 0.26       |

###  Observations:

 Worst-case timing preserved
 Minimal accuracy loss
 Significant reduction in corners

---

#  Visualization

Generated automatically:

 `results/correlation_heatmap.png`
 `results/metrics_comparison.png`

### Insights:

 Highly correlated corners → redundant
 Distinct corners → must retain

---

#  Future Work

 Integration with real STA tools (PrimeTime/OpenSTA)
 Machine learning model for prediction
 GUI dashboard
 Support for large industrial datasets
 Advanced clustering (DBSCAN, Hierarchical)

---

#  Applications

 VLSI Timing Closure
 Physical Design Optimization
 EDA Tool Development
 Research & Academic Projects

---

#  Key Contribution

This project introduces a **data-driven, automated approach** to PVT corner reduction using:

 Path-aware correlation
 Feature-weighted analysis
 Clustering-based grouping
 Optimization-driven selection

 Bridging the gap between **EDA workflows and intelligent automation**

---

#  Conclusion

The framework successfully:

 Reduces redundant PVT corners
 Preserves worst-case timing
 Improves efficiency of STA

 Demonstrates a scalable and practical solution for modern VLSI design challenges.

---

#  Author

Developed as a **core VLSI + Python automation project** for academic and research purposes.

---

#  License

This project is for educational and research use.

---

