import json

from config import Config
from prompt import build_system_prompt
from provider import Provider
from session import Session
from tools import TOOLS_SCHEMA, read_file, tool_exec, write_file


def agent_loop(user_input: str, session: Session, provider: Provider, config: Config) -> str:
    session.append({"role": "user", "content": user_input})

    for _ in range(config.max_iterations):
        messages = [build_system_prompt(config)] + session.get_legal_history(config.max_history_msgs)
        msg_obj = provider.chat(messages, TOOLS_SCHEMA)

        msg_dict = {"role": "assistant", "content": msg_obj.content or ""}
        if msg_obj.tool_calls:
            msg_dict["tool_calls"] = [
                {
                    "id": t.id,
                    "type": "function",
                    "function": {
                        "name": t.function.name,
                        "arguments": t.function.arguments,
                    },
                }
                for t in msg_obj.tool_calls
            ]
        session.append(msg_dict)

        if not msg_obj.tool_calls:
            return msg_obj.content or ""

        for tool in msg_obj.tool_calls:
            name = tool.function.name
            args = json.loads(tool.function.arguments)

            print(f"  [mote] ⚙️  {name}({json.dumps(args)})")

            if name == "exec":
                res = tool_exec(args["cmd"], config)
            elif name == "read_file":
                res = read_file(args.get("path", ""), config)
            elif name == "write_file":
                res = write_file(args.get("path", ""), args.get("content", ""), config)
            else:
                res = f"[ERROR] Unknown tool: {name}"

            session.append({"role": "tool", "tool_call_id": tool.id, "content": res})

    return "[ERROR] Max tool iterations reached."
