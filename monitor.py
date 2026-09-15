import psutil
import time


def get_process_data():

    processes = []

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):

        try:

            info = process.info

            cpu = info['cpu_percent']
            memory = info['memory_percent']

            if cpu is None:
                cpu = 0.0

            if memory is None:
                memory = 0.0

            processes.append({
                'pid': info['pid'],
                'name': info['name'] or 'Unknown',
                'cpu': cpu,
                'memory': memory
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

            pass

    return processes


while True:

    print("\n" + "=" * 70)
    print("REAL-TIME OS PROCESS MONITOR")
    print("=" * 70)

    print(f"{'PID':<10}{'PROCESS':<30}{'CPU %':<15}{'MEMORY %':<15}")
    print("-" * 70)

    processes = get_process_data()

    for process in processes[:20]:

        print(
            f"{process['pid']:<10}"
            f"{str(process['name'])[:28]:<30}"
            f"{process['cpu']:<15.2f}"
            f"{process['memory']:<15.2f}"
        )

    print("=" * 70)
    print("Monitoring... Press CTRL+C to stop.")

    time.sleep(3)