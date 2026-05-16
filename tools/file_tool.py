import os
from smolagents import tool

# Prevent writing to critical system paths
BLOCKED_PATHS = ["/etc", "/usr", "/sys", "/proc", "/dev", "/boot", "/root"]


def _is_blocked_path(path: str) -> bool:
    """Check if path is in a blocked system directory."""
    abs_path = os.path.abspath(path)
    for blocked in BLOCKED_PATHS:
        if abs_path.startswith(blocked + os.sep) or abs_path == blocked:
            return True
    return False


@tool
def read_file(path: str) -> str:
    """
    Read and return the contents of a file at the given path.

    Args:
        path: Absolute or relative path to the file.

    Returns:
        The file contents as a string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to a file at the given path. Overwrites if exists.

    Args:
        path: Absolute or relative path to the file.
        content: The content to write.

    Returns:
        Confirmation message.
    """
    if _is_blocked_path(path):
        return f"Error: Writing to system path '{path}' is not allowed."

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"
