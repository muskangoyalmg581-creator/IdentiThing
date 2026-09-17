from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
import csv

output_file = "advanced_data/file_events.csv"

os.makedirs("advanced_data", exist_ok=True)


class FileActivityHandler(FileSystemEventHandler):

    def log_event(self, event_type, path):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file_exists = os.path.exists(output_file)

        with open(output_file, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "timestamp",
                    "event_type",
                    "path"
                ])

            writer.writerow([
                timestamp,
                event_type,
                path
            ])

        print(
            "File Event:",
            event_type,
            "|",
            path
        )

    def on_created(self, event):

        if not event.is_directory:

            self.log_event(
                "CREATED",
                event.src_path
            )

    def on_modified(self, event):

        if not event.is_directory:

            self.log_event(
                "MODIFIED",
                event.src_path
            )

    def on_deleted(self, event):

        if not event.is_directory:

            self.log_event(
                "DELETED",
                event.src_path
            )

    def on_moved(self, event):

        if not event.is_directory:

            self.log_event(
                "MOVED",
                event.dest_path
            )


home = os.path.expanduser("~")

folders = [
    os.path.join(home, "Desktop"),
    os.path.join(home, "Documents"),
    os.path.join(home, "Downloads")
]

event_handler = FileActivityHandler()

observer = Observer()

for folder in folders:

    if os.path.exists(folder):

        observer.schedule(
            event_handler,
            folder,
            recursive=True
        )

observer.start()

print("=" * 60)
print("IDENTITHING - FILE ACTIVITY MONITOR")
print("=" * 60)

try:

    while True:

        pass

except KeyboardInterrupt:

    observer.stop()

observer.join()