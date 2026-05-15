from smolagents import tool


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
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"
