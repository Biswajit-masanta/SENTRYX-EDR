import os
import platform
import socket
from datetime import datetime
def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os_name": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count() or 0,
        "python_version": platform.python_version(),
        "last_seen": str(datetime.now()) 
    }
