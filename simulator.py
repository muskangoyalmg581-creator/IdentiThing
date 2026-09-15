import pandas as pd
import joblib

model_file = "model/isolation_forest.pkl"
data_file = "data/processed_data.csv"

model = joblib.load(model_file)

df = pd.read_csv(data_file)

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

normal_sample = df[features].sample(1, random_state=42)

suspicious_sample = normal_sample.copy()

suspicious_sample["cpu_percent"] = 85
suspicious_sample["memory_percent"] = 75
suspicious_sample["avg_cpu"] = 70
suspicious_sample["avg_memory"] = 60
suspicious_sample["message_frequency"] = 1000
suspicious_sample["file_activity"] = 2000
suspicious_sample["process_count"] = 1000
suspicious_sample["command_activity"] = 1000
suspicious_sample["login_activity"] = 10

normal_prediction = model.predict(normal_sample)[0]

suspicious_prediction = model.predict(suspicious_sample)[0]

print("\n" + "=" * 60)
print("IDENTITHING - BEHAVIOR SIMULATION")
print("=" * 60)

print("\nNORMAL BEHAVIOR")
print("-" * 60)

if normal_prediction == 1:
    print("Prediction: NORMAL")
else:
    print("Prediction: ANOMALY DETECTED")

print("\nSUSPICIOUS BEHAVIOR")
print("-" * 60)

if suspicious_prediction == -1:
    print("Prediction: ANOMALY DETECTED")
else:
    print("Prediction: NORMAL")

print("\nSuspicious Test Values:")
print("CPU:", suspicious_sample["cpu_percent"].iloc[0])
print("Memory:", suspicious_sample["memory_percent"].iloc[0])
print("File Activity:", suspicious_sample["file_activity"].iloc[0])
print("Process Count:", suspicious_sample["process_count"].iloc[0])
print("Command Activity:", suspicious_sample["command_activity"].iloc[0])

print("=" * 60)