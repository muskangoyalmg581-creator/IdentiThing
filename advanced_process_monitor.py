import psutil
import time
import csv
import os
from datetime import datetime

output_file = "advanced_data/process_behavior.csv"

os.makedirs("advanced_data", exist_ok=True)

previous_pids = set()

while True:

    current_pids = set()

    process_count = 0
    total_cpu = 0
    total_memory = 0
    cpu_spikes = 0
    memory_spikes = 0

    rows = []

    for process in psutil.process_iter(
        ['pid', 'name', 'username', 'memory_percent']
    ):

        try:

            info = process.info

            pid = info["pid"]

            name = info["name"] or "Unknown"

            username = info["username"] or "Unknown"

            memory = info["memory_percent"] or 0

            process.cpu_percent()

            current_pids.add(pid)

            rows.append({
                "pid": pid,
                "name": name,
                "username": username,
                "memory": memory,
                "process": process
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    time.sleep(1)

    new_processes = len(current_pids - previous_pids)

    terminated_processes = len(previous_pids - current_pids)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "pid",
                "process_name",
                "username",
                "cpu_percent",
                "memory_percent",
                "new_processes",
                "terminated_processes",
                "process_count"
            ])

        for item in rows:

            try:

                cpu = item["process"].cpu_percent()

                memory = item["memory"]

                if cpu > 50:
                    cpu_spikes += 1

                if memory > 50:
                    memory_spikes += 1

                total_cpu += cpu

                total_memory += memory

                process_count += 1

                writer.writerow([
                    timestamp,
                    item["pid"],
                    item["name"],
                    item["username"],
                    cpu,
                    memory,
                    new_processes,
                    terminated_processes,
                    process_count
                ])

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):

                pass

    previous_pids = current_pids

    print(
        "Process behavior collected:",
        timestamp,
        "| Processes:",
        process_count,
        "| New:",
        new_processes,
        "| Terminated:",
        terminated_processes
    )

    time.sleep(3)
    