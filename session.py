import json
import os


class Session:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.history = self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def append(self, msg: dict):
        self.history.append(msg)
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    def get_legal_history(self, max_msgs: int):
        if len(self.history) <= max_msgs:
            return self.history

        idx = len(self.history) - max_msgs
        while idx > 0:
            msg = self.history[idx]
            prev_msg = self.history[idx - 1]
            if msg.get("role") == "tool" or (
                prev_msg.get("role") == "assistant" and prev_msg.get("tool_calls")
            ):
                idx -= 1
            else:
                break
        return self.history[idx:]
