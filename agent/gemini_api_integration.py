"""AI-based code review agent using Gemini Flash API."""

import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

from tools.complexity_checker import check_complexity
from tools.syntax_checker import check_syntax

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def run_tool(name: str, inputs: dict) -> str:
    """Execute an analysis tool by name and return the result JSON string."""
    if name == "check_syntax":
        result = check_syntax(inputs.get("code", ""))
    elif name == "check_complexity":
        result = check_complexity(inputs.get("code", ""))
    else:
        result = {"error": "Unknown tool"}

    return json.dumps(result)


def review_code(code: str) -> str:
    """Review Python code with Gemini Flash using local analysis tool outputs."""
    if not api_key:
        return "Error: GEMINI_API_KEY is not set. Add it to your .env file."

    syntax_result = run_tool("check_syntax", {"code": code})
    complexity_result = run_tool("check_complexity", {"code": code})

    prompt = f"""
You are an expert Python code reviewer.

Use the analysis results below and provide a clear review with exactly these four sections:
1. Summary
2. Issues Found
3. Suggestions
4. Rating out of 10

Be constructive and specific.

Syntax Analysis:
{syntax_result}

Complexity Analysis:
{complexity_result}

Code to Review:
```python
{code}
```
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text or "No review generated"
