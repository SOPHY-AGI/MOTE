import os

from config import Config
from loop import agent_loop
from provider import Provider
from session import Session


def main():
    config = Config()
    os.makedirs(config.workspace, exist_ok=True)

    session_path = os.path.join(config.workspace, "session.jsonl")
    session = Session(session_path)
    provider = Provider(config)

    print("MOTE: Minimal Personal Agent Runtime")
    print(f"Workspace: {os.path.abspath(config.workspace)}")
    print("------------------------------------")

    while True:
        try:
            user_input = input("\nUSER > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.strip():
                continue

            response = agent_loop(user_input, session, provider, config)
            print(f"\nMOTE > {response}")

        except KeyboardInterrupt:
            print("\n[Interrupted]")
            break
        except Exception as e:
            print(f"\n[FATAL ERROR] {e}")


if __name__ == "__main__":
    main()
