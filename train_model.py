import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest

input_file = "data/processed_data.csv"
model_file = "model/isolation_forest.pkl"

df = pd.read_csv(input_file)

features = [
    "cpu_percent",
    "memory_percent",
    "avg_cpu",
    "avg_memory",
    "message_frequency",
    "file_activity",
    "process_count",
    "command_activity",
    "login_activity"
]

X = df[features]

model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)

model.fit(X)

os.makedirs("model", exist_ok=True)

joblib.dump(model, model_file)

predictions = model.predict(X)

normal = sum(predictions == 1)
anomalies = sum(predictions == -1)

print("\n" + "=" * 60)
print("IDENTITHING - MODEL TRAINING")
print("=" * 60)

print("Total records:", len(X))
print("Features used:", len(features))
print("Normal records:", normal)
print("Anomalous records:", anomalies)
print("Model saved:", model_file)

print("=" * 60)