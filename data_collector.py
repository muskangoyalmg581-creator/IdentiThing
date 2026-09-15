import psutil
import csv
import os
import time
from datetime import datetime


file_path = "data/process_data.csv"


def collect_process_data():

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "pid",
                "process_name",
                "cpu_percent",
                "memory_percent"
            ])

        processes = []

        for process in psutil.process_iter(
            ['pid', 'name', 'memory_percent']
        ):

            try:

                info = process.info

                memory = info["memory_percent"]

                if memory is None:
                    memory = 0.0

                process.cpu_percent()

                processes.append({
                    "process": process,
                    "pid": info["pid"],
                    "name": info["name"] or "Unknown",
                    "memory": memory
                })

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

                pass

        time.sleep(1)

        for item in processes:

            try:

                cpu = item["process"].cpu_percent()

                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    item["pid"],
                    item["name"],
                    cpu,
                    item["memory"]
                ])

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

                pass


while True:

    collect_process_data()

    print("Process data collected and saved.")

    time.sleep(3)