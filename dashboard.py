from flask import Flask, render_template, jsonify
import psutil
import pandas as pd
import joblib
import os
import time

app = Flask(__name__)

model_file = "model/isolation_forest.pkl"
alert_file = "data/alerts.csv"

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

            if info["cmdline"]:
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

        return len(psutil.users())

    except:

        return 0


def get_process_data():

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

    file_activity = get_file_activity()

    process_count, command_activity = get_system_activity()

    login_activity = get_login_activity()

    results = []

    for item in processes:

        try:

            process = item["process"]

            cpu = process.cpu_percent()

            memory = item["memory"]

            data = pd.DataFrame([{

                "cpu_percent": cpu,

                "memory_percent": memory,

                "avg_cpu": cpu,

                "avg_memory": memory,

                "message_frequency": process_count,

                "file_activity": file_activity,

                "process_count": process_count,

                "command_activity": command_activity,

                "login_activity": login_activity

            }])

            prediction = model.predict(data)[0]

            if prediction == -1:

                status = "ANOMALY"

                risk = 80

                if cpu > 50:
                    risk += 10

                if memory > 50:
                    risk += 10

                if risk > 100:
                    risk = 100

            else:

                status = "NORMAL"

                risk = 0

            results.append({

                "pid": item["pid"],

                "name": item["name"],

                "cpu": round(cpu, 2),

                "memory": round(memory, 2),

                "status": status,

                "risk": risk

            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    return results


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/processes")
def processes():

    data = get_process_data()

    return jsonify(data)


@app.route("/api/alerts")
def alerts():

    if not os.path.exists(alert_file):

        return jsonify([])

    try:

        df = pd.read_csv(alert_file)

        df = df.tail(20)

        return jsonify(
            df.to_dict(orient="records")
        )

    except:

        return jsonify([])


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )