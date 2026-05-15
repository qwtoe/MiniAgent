import subprocess
from smolagents import tool

DANGEROUS_COMMANDS = ["rm", "mv", "dd", ">", "|", "curl", "wget"]


@tool
def run_command(command: str) -> str:
    """
    Run a shell command and return its output.
    If the command contains potentially dangerous operations,
    the user will be asked for confirmation before execution.

    Args:
        command: The shell command to execute.

    Returns:
        stdout and stderr of the command.
    """
    is_dangerous = any(cmd in command for cmd in DANGEROUS_COMMANDS)

    if is_dangerous:
        user_ok = input(f"⚠️  Potentially dangerous command: '{command}'. Run? [y/N] ")
        if user_ok.lower() != "y":
            return "Command cancelled by user."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = []
        if result.stdout:
            output.append(f"stdout:\n{result.stdout}")
        if result.stderr:
            output.append(f"stderr:\n{result.stderr}")
        return "\n".join(output) if output else "Command executed successfully (no output)."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error: {e}"
