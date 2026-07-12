from pydantic import BaseModel, Field


class Process(BaseModel):
    pid: int = Field(description="Process ID")

    process_name: str = Field(description="Process name")

    exe_path: str | None = Field(
        default=None,
        description="Executable path"
    )

    cpu_usage: float = Field(description="CPU usage percentage")

    memory_usage: float = Field(description="Memory usage percentage")

    status: str = Field(description="Running status")