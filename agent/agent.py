from time import sleep
from modules_for_agents.sys_info import get_system_info
from modules_for_agents.resources import get_resource_usage
from modules_for_agents.sender import send_report

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
modules_for_agents = sys.path[0] + "/modules_for_agents"
sys.path.append(modules_for_agents)

from modules_for_agents.process_collector import collect_processes
while True:

    data = {
        "system_info": get_system_info(),
        "resource_usage": get_resource_usage(),
        "processes": collect_processes()
    }

    response = send_report(data)
    sleep(10)

    print("--------------------------------")
    print(response.status_code)
    print(response.text)



