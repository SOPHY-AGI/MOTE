import os
from dataclasses import dataclass


@dataclass
class Config:
    workspace: str = os.getenv("MOTE_WORKSPACE", "./workspace")
    model: str = os.getenv("MOTE_MODEL", "gpt-4o")
    api_key: str | None = os.getenv("OPENAI_API_KEY")
    max_iterations: int = 10
    max_history_msgs: int = 20
    cmd_timeout: int = 15
    max_output_len: int = 2000
