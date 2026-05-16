import os
import sys

try:
    import readline  # Enable terminal line editing (backspace, arrow keys, history)
except ImportError:
    pass  # readline not available on all platforms

from smolagents import CodeAgent, OpenAIServerModel
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, TEMPERATURE, MAX_STEPS


def main():
    if not LLM_API_KEY:
        print("Error: LLM_API_KEY not found. Please set it in .env")
        return

    model = OpenAIServerModel(
        model_id=LLM_MODEL,
        api_base=LLM_BASE_URL,
        api_key=LLM_API_KEY,
    )

    from tools import read_file, write_file, run_command, web_search
    agent = CodeAgent(tools=[read_file, write_file, run_command, web_search], model=model, verbosity_level=2)

    print("🤖 Agent ready! Type 'exit' or 'quit' to leave.")
    print("-" * 40)

    while True:
        try:
            user_input = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break

        if not user_input.strip():
            continue

        try:
            response = agent.run(user_input)

            # Check if any step had a code parsing error (model forgot <code> format)
            has_parsing_error = False
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'steps'):
                for step in agent.memory.steps:
                    error = getattr(step, 'error', None)
                    if error and 'code parsing' in str(error).lower():
                        has_parsing_error = True
                        break

            # Fallback: if CodeAgent failed to parse, call model directly
            if response is None or has_parsing_error:
                chat_message = model([{"role": "user", "content": user_input}])
                response = chat_message.content
            print(response)
        except Exception as e:
            # If agent.run() crashes, also fall back to direct model call
            try:
                chat_message = model([{"role": "user", "content": user_input}])
                print(chat_message.content)
            except Exception:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
