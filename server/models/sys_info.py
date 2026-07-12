from pydantic import BaseModel, Field

class SystemInfo(BaseModel):
    hostname: str = Field(description="The hostname of the system")
    os_name: str = Field(description="The name of the Operating System")
    os_release: str = Field(description="The release version of the OS")
    architecture: str = Field(description="OS architecture (e.g., 64bit)")
    processor: str = Field(description="Processor type")
    cpu_count: int = Field(description="Number of physical CPU cores")
    python_version: str = Field(description="Python runtime version")
    last_seen: str = Field(description="Last online time")
