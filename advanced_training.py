import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

input_file = "advanced_data/master_features.csv"

df = pd.read_csv(input_file)

features = [
    "cpu_percent",
    "memory_percent",
    "cpu_mean",
    "cpu_std",
    "memory_mean",
    "memory_std",
    "process_frequency",
    "new_processes",
    "terminated_processes",
    "process_count",
    "connections",
    "established_connections",
    "unique_remote_addresses",
    "bytes_sent",
    "bytes_received",
    "active_sessions",
    "new_sessions",
    "ended_sessions",
    "cpu_spike",
    "memory_spike",
    "user_process_frequency"
]

df = df.dropna(
    subset=features
)

normal = df[
    features
].copy()

normal["label"] = 0

anomalies = normal.sample(
    frac=0.30,
    random_state=42
).copy()

anomalies["cpu_percent"] *= 4

anomalies["memory_percent"] *= 3

anomalies["new_processes"] += 20

anomalies["terminated_processes"] += 20

anomalies["connections"] *= 3

anomalies["established_connections"] *= 3

anomalies["unique_remote_addresses"] += 15

anomalies["bytes_sent"] *= 5

anomalies["bytes_received"] *= 5

anomalies["cpu_spike"] = 1

anomalies["memory_spike"] = 1

anomalies["label"] = 1

dataset = pd.concat(
    [normal, anomalies],
    ignore_index=True
)

dataset = dataset.replace(
    [np.inf, -np.inf],
    np.nan
)

dataset = dataset.fillna(0)

X = dataset[features]

y = dataset["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

isolation_forest = IsolationForest(
    n_estimators=300,
    contamination=0.30,
    random_state=42
)

isolation_forest.fit(
    X_train[y_train == 0]
)

random_forest = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

random_forest.fit(
    X_train,
    y_train
)

rf_prediction = random_forest.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    rf_prediction
)

precision = precision_score(
    y_test,
    rf_prediction,
    zero_division=0
)

recall = recall_score(
    y_test,
    rf_prediction,
    zero_division=0
)

f1 = f1_score(
    y_test,
    rf_prediction,
    zero_division=0
)

print("=" * 60)
print("IDENTITHING V2 - MODEL EVALUATION")
print("=" * 60)

print("Training records:", len(X_train))

print("Testing records:", len(X_test))

print("Accuracy:", round(accuracy * 100, 2), "%")

print("Precision:", round(precision * 100, 2), "%")

print("Recall:", round(recall * 100, 2), "%")

print("F1 Score:", round(f1 * 100, 2), "%")

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        rf_prediction
    )
)

os.makedirs(
    "advanced_model",
    exist_ok=True
)

joblib.dump(
    isolation_forest,
    "advanced_model/isolation_forest.pkl"
)

joblib.dump(
    random_forest,
    "advanced_model/random_forest.pkl"
)

joblib.dump(
    features,
    "advanced_model/features.pkl"
)

print("\nModels saved.")

print("=" * 60)