import os
import subprocess

from config import Config


TRUNCATED_MARKER = "...\n[TRUNCATED]"


def _truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + TRUNCATED_MARKER


def _secure_path(path: str, config: Config) -> str:
    base = os.path.abspath(config.workspace)
    target = os.path.abspath(os.path.join(base, path))
    if os.path.commonpath([base, target]) != base:
        raise ValueError(f"Path traversal outside workspace denied: {path}")
    return target


def tool_exec(cmd: str, config: Config) -> str:
    denylist = ["rm -rf", "mkfs", "> /dev/", "dd if="]
    if any(bad in cmd for bad in denylist):
        return "[ERROR] Command blocked by safety denylist."

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=config.workspace,
            capture_output=True,
            text=True,
            timeout=config.cmd_timeout,
            encoding="utf-8",
        )
        out = (result.stdout or "") + (result.stderr or "")
        if not out:
            return "Command executed successfully with no output."
        return _truncate(out, config.max_output_len)
    except subprocess.TimeoutExpired:
        return f"[ERROR] Command timed out after {config.cmd_timeout}s"
    except Exception as e:
        return f"[ERROR] {e}"


def read_file(path: str, config: Config) -> str:
    try:
        target = _secure_path(path, config)
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
        return _truncate(content, config.max_output_len)
    except Exception as e:
        return f"[ERROR] {e}"


def write_file(path: str, content: str, config: Config) -> str:
    try:
        target = _secure_path(path, config)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"[ERROR] {e}"


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "exec",
            "description": "Execute a shell command.",
            "parameters": {
                "type": "object",
                "properties": {"cmd": {"type": "string"}},
                "required": ["cmd"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
]
