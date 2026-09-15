import csv
import os
from datetime import datetime


alert_file = "data/alerts.csv"


def generate_alert(process):

    os.makedirs("data", exist_ok=True)

    risk_score = 0

    if process["status"] == "ANOMALY":

        risk_score = 80

        if process["cpu"] > 50:
            risk_score += 10

        if process["memory"] > 50:
            risk_score += 10

        if risk_score > 100:
            risk_score = 100

        severity = "HIGH"

        message = "Suspicious process behavior detected."

        file_exists = os.path.exists(alert_file)

        with open(alert_file, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "timestamp",
                    "pid",
                    "process_name",
                    "cpu_percent",
                    "memory_percent",
                    "risk_score",
                    "severity",
                    "message"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                process["pid"],
                process["name"],
                process["cpu"],
                process["memory"],
                risk_score,
                severity,
                message
            ])

        return {
            "risk_score": risk_score,
            "severity": severity,
            "message": message
        }

    return {
        "risk_score": 0,
        "severity": "LOW",
        "message": "Normal process behavior."
    }


if __name__ == "__main__":

    test_process = {
        "pid": 1234,
        "name": "SuspiciousProcess",
        "cpu": 85.0,
        "memory": 75.0,
        "status": "ANOMALY"
    }

    alert = generate_alert(test_process)

    print("\n" + "=" * 60)
    print("IDENTITHING ALERT ENGINE")
    print("=" * 60)

    print("Process:", test_process["name"])
    print("Risk Score:", alert["risk_score"])
    print("Severity:", alert["severity"])
    print("Message:", alert["message"])

    print("=" * 60) 