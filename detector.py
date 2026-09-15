import psutil
import pandas as pd
import joblib
import time
import os

from alert_engine import generate_alert

model_file = "model/isolation_forest.pkl"

model = joblib.load(model_file)

def get_file_activity():

    home = os.path.expanduser("~")

    folders = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads")
    ]

    file_count = 0

    for folder in folders:

        if os.path.exists(folder):

            try:

                for root, dirs, files in os.walk(folder):

                    file_count += len(files)

                    if file_count >= 1000:
                        return file_count

            except PermissionError:

                pass

    return file_count


def get_system_activity():

    process_count = 0

    command_count = 0

    for process in psutil.process_iter(
        ['pid', 'name', 'cmdline']
    ):

        try:

            info = process.info

            process_count += 1

            command = info["cmdline"]

            if command:
                command_count += 1

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    return process_count, command_count


def get_login_activity():

    try:

        users = psutil.users()

        return len(users)

    except:

        return 0


def get_processes():

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

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    time.sleep(1)

    results = []

    file_activity = get_file_activity()

    process_count, command_activity = get_system_activity()

    login_activity = get_login_activity()

    for item in processes:

        try:

            process = item["process"]

            cpu = process.cpu_percent()

            pid = item["pid"]

            name = item["name"]

            memory = item["memory"]

            avg_cpu = cpu

            avg_memory = memory

            message_frequency = process_count

            data = pd.DataFrame([{

                "cpu_percent": cpu,

                "memory_percent": memory,

                "avg_cpu": avg_cpu,

                "avg_memory": avg_memory,

                "message_frequency": message_frequency,

                "file_activity": file_activity,

                "process_count": process_count,

                "command_activity": command_activity,

                "login_activity": login_activity

            }])

            prediction = model.predict(data)[0]

            if prediction == -1:

                status = "ANOMALY"

                risk_score = 80

                if cpu > 50:
                    risk_score += 10

                if memory > 50:
                    risk_score += 10

                if risk_score > 100:
                    risk_score = 100

            else:

                status = "NORMAL"

                risk_score = 0

            process_data = {

                "pid": pid,

                "name": name,

                "cpu": round(cpu, 2),

                "memory": round(memory, 2),

                "status": status,

                "risk": risk_score

            }

            if status == "ANOMALY":

                alert = generate_alert({

                    "pid": pid,

                    "name": name,

                    "cpu": cpu,

                    "memory": memory,

                    "status": status

                })

                process_data["severity"] = alert["severity"]

            else:

                process_data["severity"] = "LOW"

            results.append(process_data)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    return results


print("\n" + "=" * 95)

print("IDENTITHING - REAL-TIME INSIDER THREAT DETECTOR")

print("=" * 95)

while True:

    print("\n")

    print(
        f"{'PID':<10}"
        f"{'PROCESS':<35}"
        f"{'CPU %':<10}"
        f"{'MEM %':<10}"
        f"{'STATUS':<15}"
        f"{'RISK':<10}"
    )

    print("-" * 95)

    results = get_processes()

    anomaly_count = 0

    high_risk_count = 0

    for result in results[:30]:

        print(
            f"{result['pid']:<10}"
            f"{result['name'][:33]:<35}"
            f"{result['cpu']:<10.2f}"
            f"{result['memory']:<10.2f}"
            f"{result['status']:<15}"
            f"{result['risk']:<10}"
        )

        if result["status"] == "ANOMALY":

            anomaly_count += 1

        if result["risk"] >= 80:

            high_risk_count += 1

    print("-" * 95)

    print("Total Processes:", len(results))

    print("Anomalies Detected:", anomaly_count)

    print("High Risk Processes:", high_risk_count)

    print("Monitoring... Press CTRL+C to stop.")

    time.sleep(5)