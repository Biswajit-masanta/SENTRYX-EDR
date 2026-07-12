from pydantic import BaseModel , Field

class ResourceUsage(BaseModel):
    cpu_usage: float = Field(description="Current CPU usage percentage")
    memory_usage: float = Field(description="Current Memory usage percentage")
    disk_usage: float = Field(description="Current Disk usage percentage")
    