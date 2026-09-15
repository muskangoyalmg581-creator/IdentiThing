import psutil
import os
import time
import csv
from datetime import datetime


output_file = "data/activity_data.csv"


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


def get_process_activity():

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


def get_user_activity():

    try:

        users = psutil.users()

        return len(users)

    except:

        return 0


def collect_activity():

    file_count = get_file_activity()

    process_count, command_count = get_process_activity()

    user_count = get_user_activity()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "file_activity",
                "process_count",
                "command_activity",
                "login_activity"
            ])

        writer.writerow([
            timestamp,
            file_count,
            process_count,
            command_count,
            user_count
        ])

    print(
        "Activity collected:",
        timestamp,
        "| Files:",
        file_count,
        "| Processes:",
        process_count,
        "| Commands:",
        command_count,
        "| Users:",
        user_count
    )


while True:

    collect_activity()

    time.sleep(10)