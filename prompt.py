import datetime

from config import Config


def build_system_prompt(config: Config) -> dict:
    now = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    return {
        "role": "system",
        "content": (
            f"You are MOTE, a minimal, stable personal agent.\n"
            f"Current time: {now}\n"
            f"Workspace: {config.workspace}\n"
            f"RULES:\n"
            f"- Prefer workspace-relative paths.\n"
            f"- Do not run destructive commands.\n"
            f"- Keep actions minimal and reversible.\n"
            f"- Rely on your tools."
        ),
    }
