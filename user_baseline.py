import pandas as pd
import os
import joblib

input_file = "advanced_data/master_features.csv"

model_file = "advanced_model/user_baseline.pkl"

df = pd.read_csv(input_file)

features = [
    "cpu_percent",
    "memory_percent",
    "cpu_mean",
    "memory_mean",
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
    "cpu_spike",
    "memory_spike"
]

baseline = {}

for user in df["username"].unique():

    user_data = df[
        df["username"] == user
    ]

    baseline[user] = {}

    for feature in features:

        baseline[user][feature] = {
            "mean": user_data[feature].mean(),
            "std": user_data[feature].std()
        }

os.makedirs(
    "advanced_model",
    exist_ok=True
)

joblib.dump(
    baseline,
    model_file
)

print("=" * 60)
print("IDENTITHING - USER BASELINE")
print("=" * 60)

print("Users:", len(baseline))

print("Baseline saved:", model_file)

print("=" * 60)