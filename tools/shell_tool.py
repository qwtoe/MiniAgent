import subprocess
from smolagents import tool

# Commands that can cause irreversible damage or exfiltrate data
DANGEROUS_COMMANDS = ["rm", "mv", "dd"]
SHELL_REDIRECTORS = [">", "|", "&&", ";", "$("]


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
    # Check for dangerous commands or shell operators
    is_dangerous = any(
        f" {cmd}" in command or command.startswith(cmd)
        for cmd in DANGEROUS_COMMANDS
    )
    has_redirector = any(op in command for op in SHELL_REDIRECTORS)

    if is_dangerous or has_redirector:
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
