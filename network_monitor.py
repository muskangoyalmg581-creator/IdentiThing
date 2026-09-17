import psutil
import csv
import os
import time
from datetime import datetime

output_file = "advanced_data/network_behavior.csv"

os.makedirs("advanced_data", exist_ok=True)

while True:

    connections = 0

    established = 0

    remote_addresses = set()

    try:

        for connection in psutil.net_connections(
            kind="inet"
        ):

            connections += 1

            if connection.status == "ESTABLISHED":

                established += 1

            if connection.raddr:

                try:

                    remote_addresses.add(
                        connection.raddr.ip
                    )

                except:

                    pass

    except psutil.AccessDenied:

        pass

    network = psutil.net_io_counters()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "connections",
                "established_connections",
                "unique_remote_addresses",
                "bytes_sent",
                "bytes_received"
            ])

        writer.writerow([
            timestamp,
            connections,
            established,
            len(remote_addresses),
            network.bytes_sent,
            network.bytes_recv
        ])

    print(
        "Network Activity:",
        timestamp,
        "| Connections:",
        connections,
        "| Established:",
        established,
        "| Remote:",
        len(remote_addresses)
    )

    time.sleep(5)