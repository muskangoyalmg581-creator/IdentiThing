import pandas as pd
import joblib

model = joblib.load("model/isolation_forest.pkl")

df = pd.read_csv("data/processed_data.csv")

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

normal = df[features].sample(n=1, random_state=42).iloc[0]

tests = []

tests.append({
    "Test": "Normal Behavior",
    "cpu_percent": normal["cpu_percent"],
    "memory_percent": normal["memory_percent"],
    "avg_cpu": normal["avg_cpu"],
    "avg_memory": normal["avg_memory"],
    "message_frequency": normal["message_frequency"],
    "file_activity": normal["file_activity"],
    "process_count": normal["process_count"],
    "command_activity": normal["command_activity"],
    "login_activity": normal["login_activity"]
})

tests.append({
    "Test": "High CPU",
    "cpu_percent": 90,
    "memory_percent": normal["memory_percent"],
    "avg_cpu": 80,
    "avg_memory": normal["avg_memory"],
    "message_frequency": normal["message_frequency"],
    "file_activity": normal["file_activity"],
    "process_count": normal["process_count"],
    "command_activity": normal["command_activity"],
    "login_activity": normal["login_activity"]
})

tests.append({
    "Test": "High Memory",
    "cpu_percent": normal["cpu_percent"],
    "memory_percent": 90,
    "avg_cpu": normal["avg_cpu"],
    "avg_memory": 80,
    "message_frequency": normal["message_frequency"],
    "file_activity": normal["file_activity"],
    "process_count": normal["process_count"],
    "command_activity": normal["command_activity"],
    "login_activity": normal["login_activity"]
})

tests.append({
    "Test": "High File Activity",
    "cpu_percent": normal["cpu_percent"],
    "memory_percent": normal["memory_percent"],
    "avg_cpu": normal["avg_cpu"],
    "avg_memory": normal["avg_memory"],
    "message_frequency": normal["message_frequency"],
    "file_activity": 5000,
    "process_count": normal["process_count"],
    "command_activity": normal["command_activity"],
    "login_activity": normal["login_activity"]
})

tests.append({
    "Test": "High Command Activity",
    "cpu_percent": normal["cpu_percent"],
    "memory_percent": normal["memory_percent"],
    "avg_cpu": normal["avg_cpu"],
    "avg_memory": normal["avg_memory"],
    "message_frequency": 1000,
    "file_activity": normal["file_activity"],
    "process_count": normal["process_count"],
    "command_activity": 1000,
    "login_activity": normal["login_activity"]
})

tests.append({
    "Test": "Combined Suspicious Behavior",
    "cpu_percent": 90,
    "memory_percent": 85,
    "avg_cpu": 80,
    "avg_memory": 75,
    "message_frequency": 1000,
    "file_activity": 5000,
    "process_count": 1000,
    "command_activity": 1000,
    "login_activity": 5
})

results = pd.DataFrame(tests)

predictions = model.predict(results[features])

results["Expected"] = [
    "NORMAL",
    "ANOMALY",
    "ANOMALY",
    "ANOMALY",
    "ANOMALY",
    "ANOMALY"
]

results["Detected"] = [
    "NORMAL" if prediction == 1 else "ANOMALY"
    for prediction in predictions
]

results["Correct"] = results["Expected"] == results["Detected"]

print("\n" + "=" * 80)
print("IDENTITHING - EXPERIMENTAL EVALUATION")
print("=" * 80)

print(
    results[
        ["Test", "Expected", "Detected", "Correct"]
    ].to_string(index=False)
)

total = len(results)
correct = results["Correct"].sum()

accuracy = correct / total * 100

print("\nTotal Tests:", total)
print("Correct Predictions:", correct)
print("Accuracy:", round(accuracy, 2), "%")

print("=" * 80)