from sklearn.ensemble import RandomForestClassifier
import numpy as np


def extract_features(results):
    features = []
    labels = []
    corner_names = []

    for corner, data in results.items():
        metrics = data["metrics"]
        slacks = list(data["paths"].values())

        if not slacks:
            continue

        wns = metrics["WNS"]
        tns = metrics["TNS"]
        mean_slack = np.mean(slacks)
        min_slack = min(slacks)

        features.append([wns, tns, mean_slack, min_slack])
        corner_names.append(corner)

    return np.array(features), corner_names


def train_model(results, selected):
    X, corner_names = extract_features(results)

    # Label: 1 if selected, else 0
    y = [1 if c in selected else 0 for c in corner_names]

    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)

    return model, corner_names


def predict_importance(model, results):
    X, corner_names = extract_features(results)

    preds = model.predict(X)
    probs = model.predict_proba(X)

    prediction_dict = {}

    for i, corner in enumerate(corner_names):
        prediction_dict[corner] = {
            "decision": "KEEP" if preds[i] == 1 else "REMOVE",
            "confidence": round(max(probs[i]), 2)
        }

    return prediction_dict