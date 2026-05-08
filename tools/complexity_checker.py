"""Complexity checker tool for analyzing code structure."""

import ast


def check_complexity(code: str) -> dict:
    """
    Analyze code complexity by counting functions, classes, and lines.
    
    Args:
        code: Python code string to analyze
        
    Returns:
        A dictionary with code metrics including function count, class count, and function names
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"error": "Cannot analyze - syntax error in code"}
    
    total_lines = len(code.split('\n'))
    function_count = 0
    class_count = 0
    function_names = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1
            function_names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            class_count += 1
    
    return {
        "total_lines": total_lines,
        "function_count": function_count,
        "class_count": class_count,
        "function_names": function_names
    }
