import psutil

IGNORED_PROCESSES = {
    "System",
    "System Idle Process",
    "Registry",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "winlogon.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "fontdrvhost.exe",
    "dwm.exe",
    "sihost.exe",
    "RuntimeBroker.exe",
    "SearchHost.exe",
    "taskhostw.exe",
    "conhost.exe",
    "spoolsv.exe",
    "WUDFHost.exe",
    "SecurityHealthService.exe",
    "SecurityHealthSystray.exe",
    "ShellExperienceHost.exe",
    "StartMenuExperienceHost.exe",
    "ApplicationFrameHost.exe",
    "ctfmon.exe",
    "dllhost.exe",
    "audiodg.exe",
    "Memory Compression",
    "Idle",
}


def collect_processes():
    processes = []
    seen = set()

    for proc in psutil.process_iter(
        ['pid', 'name', 'exe', 'cpu_percent', 'memory_percent', 'status']
    ):
        try:
            info = proc.info
            name = info.get("name", "")
            exe = info.get("exe")

            # Ignore Windows/system processes
            if (
                not name
                or name in IGNORED_PROCESSES
                or not exe
            ):
                continue

            # Ignore duplicate processes (same executable)
            if exe in seen:
                continue
            seen.add(exe)

            processes.append({
                "pid": info["pid"],
                "process_name": name,
                "exe_path": exe,
                "cpu_usage": info["cpu_percent"],
                "memory_usage": info["memory_percent"],
                "status": info["status"]
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes


if __name__ == "__main__":
    processes = collect_processes()

    print("Total processes:", len(processes))
    print("Sample process:\n", processes[0])
    print(processes[:10])