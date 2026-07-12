from database.operations import get_total_active_alerts

def extract_features(report , system_id):
    features = {}

    # -------------------------
    # Resource Features
    # -------------------------
    features["cpu_usage"] = report.resource_usage.cpu_usage
    features["memory_usage"] = report.resource_usage.memory_usage
    features["disk_usage"] = report.resource_usage.disk_usage

    # -------------------------
    # Process Features
    # -------------------------
    features["process_count"] = len(report.processes)

    browser_names = {
        "chrome.exe",
        "firefox.exe",
        "msedge.exe",
        "opera.exe",
        "brave.exe",
        "vivaldi.exe",
        "safari.exe"
    }

    features["browser_count"] = sum(
        1
        for process in report.processes
        if process.process_name.lower() in browser_names
    )

    python_names = {
        "python.exe",
        "python3.exe"
    }

    features["python_running"] = int(
        any(
            process.process_name.lower() in python_names
            for process in report.processes
        )
    )

    cmd_names = {
        "cmd.exe"
    }

    features["cmd_running"] = int(
        any(
            process.process_name.lower() in cmd_names
            for process in report.processes
        )
    )

    powershell_names = {
        "powershell.exe",
        "pwsh.exe"
    }

    features["powershell_running"] = int(
        any(
            process.process_name.lower() in powershell_names
            for process in report.processes
        )
    )

    # Unknown processes
    features["unknown_process_count"] = sum(
        1
        for process in report.processes
        if not process.exe_path
    )

    # High CPU processes (>20%)
    features["high_cpu_process_count"] = sum(
        1
        for process in report.processes
        if process.cpu_usage > 20
    )

    # High Memory processes (>10%)
    features["high_memory_process_count"] = sum(
        1
        for process in report.processes
        if process.memory_usage > 10
    )
    features["total_alerts"] = get_total_active_alerts(system_id)

    return features