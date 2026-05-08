"""Syntax checker tool for Python code analysis."""

import ast


def check_syntax(code: str) -> dict:
    """
    Check if the given Python code has valid syntax.
    
    Args:
        code: Python code string to validate
        
    Returns:
        A dictionary with status and any syntax errors found
    """
    try:
        ast.parse(code)
        return {"status": "ok", "errors": []}
    except SyntaxError as e:
        return {
            "status": "error",
            "errors": [
                {
                    "line": e.lineno,
                    "message": e.msg,
                    "text": e.text
                }
            ]
        }
