import pandas as pd
import os

process_file = "advanced_data/process_behavior.csv"
network_file = "advanced_data/network_behavior.csv"
session_file = "advanced_data/session_behavior.csv"

output_file = "advanced_data/master_features.csv"

process_data = pd.read_csv(process_file)

network_data = pd.read_csv(network_file)

session_data = pd.read_csv(session_file)

process_data["timestamp"] = pd.to_datetime(
    process_data["timestamp"]
)

network_data["timestamp"] = pd.to_datetime(
    network_data["timestamp"]
)

session_data["timestamp"] = pd.to_datetime(
    session_data["timestamp"]
)

process_data = process_data.sort_values(
    "timestamp"
)

network_data = network_data.sort_values(
    "timestamp"
)

session_data = session_data.sort_values(
    "timestamp"
)

network_data = network_data.drop_duplicates(
    "timestamp"
)

session_data = session_data.drop_duplicates(
    "timestamp"
)

merged = pd.merge_asof(
    process_data,
    network_data,
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("10s")
)

merged = pd.merge_asof(
    merged.sort_values("timestamp"),
    session_data,
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("10s")
)

merged = merged.dropna()

merged["cpu_percent"] = pd.to_numeric(
    merged["cpu_percent"],
    errors="coerce"
)

merged["memory_percent"] = pd.to_numeric(
    merged["memory_percent"],
    errors="coerce"
)

merged = merged.dropna()

merged["cpu_mean"] = merged.groupby(
    "process_name"
)["cpu_percent"].transform("mean")

merged["cpu_std"] = merged.groupby(
    "process_name"
)["cpu_percent"].transform("std")

merged["memory_mean"] = merged.groupby(
    "process_name"
)["memory_percent"].transform("mean")

merged["memory_std"] = merged.groupby(
    "process_name"
)["memory_percent"].transform("std")

merged["process_frequency"] = merged.groupby(
    "process_name"
)["process_name"].transform("count")

merged["cpu_spike"] = (
    merged["cpu_percent"] > 50
).astype(int)

merged["memory_spike"] = (
    merged["memory_percent"] > 50
).astype(int)

merged["user_process_frequency"] = merged.groupby(
    "username"
)["process_name"].transform("count")

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

merged = merged.dropna(
    subset=features
)

merged[
    ["timestamp", "pid", "process_name", "username"] + features
].to_csv(
    output_file,
    index=False
)

print("=" * 60)
print("IDENTITHING - ADVANCED FEATURE ENGINEERING")
print("=" * 60)

print("Records:", len(merged))

print("Features:", len(features))

print("Saved:", output_file)

print("=" * 60)