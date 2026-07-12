import psutil
import time


def get_processes():
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info

            process_data = {
                "pid": info['pid'],
                "process_name": info['name'],
                "exe_path": info.get('exe'),
                "cpu_usage": info['cpu_percent'],
                "memory_usage": info['memory_percent'],
                "status": info['status'],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            processes.append(process_data)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes