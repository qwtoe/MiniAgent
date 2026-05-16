import os
import sys

try:
    import readline  # Enable terminal line editing (backspace, arrow keys, history)
except ImportError:
    pass  # readline not available on all platforms

from smolagents import CodeAgent, OpenAIServerModel
from config import DEEPSEEK_API_KEY, MODEL_ID, API_BASE, TEMPERATURE, MAX_STEPS


def main():
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY not found. Please set it in .env")
        return

    model = OpenAIServerModel(
        model_id=MODEL_ID,
        api_base=API_BASE,
        api_key=DEEPSEEK_API_KEY,
    )

    from tools import read_file, write_file, run_command
    agent = CodeAgent(tools=[read_file, write_file, run_command], model=model, verbosity_level=2)

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
            # Fallback: if CodeAgent fails to parse model output (e.g., plain text instead of <code>),
            # directly call the model for a plain text response.
            if isinstance(response, str) and "Error in code parsing" in response:
                chat_message = model([{"role": "user", "content": user_input}])
                response = chat_message.content
            print(response)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
