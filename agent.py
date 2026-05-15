import os
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

    # Step 1: No tools yet - just basic chat to understand the Agent loop
    agent = CodeAgent(tools=[], model=model, verbosity_level=2)

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
            print(response)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
