import psutil
import csv
import os
import time
from datetime import datetime

output_file = "advanced_data/session_behavior.csv"

os.makedirs("advanced_data", exist_ok=True)

previous_users = set()

while True:

    current_users = set()

    try:

        users = psutil.users()

        for user in users:

            current_users.add(
                (
                    user.name,
                    user.terminal,
                    user.host
                )
            )

    except:

        users = []

    new_sessions = len(
        current_users - previous_users
    )

    ended_sessions = len(
        previous_users - current_users
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "active_sessions",
                "new_sessions",
                "ended_sessions"
            ])

        writer.writerow([
            timestamp,
            len(current_users),
            new_sessions,
            ended_sessions
        ])

    print(
        "Session Activity:",
        timestamp,
        "| Active:",
        len(current_users),
        "| New:",
        new_sessions,
        "| Ended:",
        ended_sessions
    )

    previous_users = current_users

    time.sleep(5)