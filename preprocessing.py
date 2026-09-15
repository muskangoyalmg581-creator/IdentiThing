import pandas as pd
import os

process_file = "data/process_data.csv"
activity_file = "data/activity_data.csv"
output_file = "data/processed_data.csv"

process_data = pd.read_csv(process_file)
activity_data = pd.read_csv(activity_file)

process_data["timestamp"] = pd.to_datetime(process_data["timestamp"])
activity_data["timestamp"] = pd.to_datetime(activity_data["timestamp"])

process_data = process_data.drop_duplicates()
process_data = process_data.dropna()

process_data["cpu_percent"] = pd.to_numeric(
    process_data["cpu_percent"],
    errors="coerce"
)

process_data["memory_percent"] = pd.to_numeric(
    process_data["memory_percent"],
    errors="coerce"
)

process_data = process_data.dropna()

process_data["avg_cpu"] = process_data.groupby(
    "process_name"
)["cpu_percent"].transform("mean")

process_data["avg_memory"] = process_data.groupby(
    "process_name"
)["memory_percent"].transform("mean")

process_data["message_frequency"] = process_data.groupby(
    "process_name"
)["process_name"].transform("count")

process_data = process_data.sort_values("timestamp")
activity_data = activity_data.sort_values("timestamp")

merged_data = pd.merge_asof(
    process_data,
    activity_data,
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("10s")
)

merged_data = merged_data.dropna()

merged_data = merged_data[
    [
        "pid",
        "process_name",
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
]

os.makedirs("data", exist_ok=True)

merged_data.to_csv(
    output_file,
    index=False
)

print("Preprocessing completed.")
print("Total records:", len(merged_data))
print("Processed file:", output_file)
print("\nColumns:")
print(list(merged_data.columns))