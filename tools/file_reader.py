"""File reader tool for loading Python files."""

import os


def read_file(filepath: str) -> dict:
    """
    Read and return the content of a Python file.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        A dictionary with file content and path, or an error message
    """
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    
    if not filepath.endswith('.py'):
        return {"error": "Only Python files supported"}
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return {"content": content, "filepath": filepath}
    except Exception as e:
        return {"error": str(e)}
