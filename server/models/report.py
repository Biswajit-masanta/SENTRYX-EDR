from pydantic import BaseModel, Field

from .sys_info import SystemInfo
from .resource import ResourceUsage
from .processes import Process
class Report(BaseModel):
    system_info: SystemInfo = Field(description="System information details")
    resource_usage: ResourceUsage = Field(description="Current resource usage details")
    processes: list[Process] = Field(description="List of running processes")