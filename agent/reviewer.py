"""AI-based code review agent using Claude API."""

import anthropic
import json
import os
from dotenv import load_dotenv
from tools.syntax_checker import check_syntax
from tools.complexity_checker import check_complexity
from tools.file_reader import read_file

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define available tools for Claude
TOOLS = [
    {
        "name": "check_syntax",
        "description": "Check if Python code has valid syntax and identify any syntax errors",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to check for syntax errors"
                }
            },
            "required": ["code"]
        }
    },
    {
        "name": "check_complexity",
        "description": "Analyze code complexity by counting functions, classes, and calculating metrics",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to analyze for complexity"
                }
            },
            "required": ["code"]
        }
    }
]


def run_tool(name: str, inputs: dict) -> str:
    """
    Execute a tool by name and return the result as a JSON string.
    
    Args:
        name: Name of the tool to execute
        inputs: Dictionary of inputs for the tool
        
    Returns:
        JSON string with the tool result
    """
    if name == "check_syntax":
        result = check_syntax(inputs.get("code", ""))
    elif name == "check_complexity":
        result = check_complexity(inputs.get("code", ""))
    else:
        result = {"error": "Unknown tool"}
    
    return json.dumps(result)


def review_code(code: str) -> str:
    """
    Review Python code using Claude AI with tool use.
    
    Args:
        code: Python code to review
        
    Returns:
        Code review with Summary, Issues Found, Suggestions, and Rating
    """
    system_prompt = """You are an expert Python code reviewer. Your task is to review Python code thoroughly.

Follow these steps:
1. First, use the check_syntax tool to validate the code syntax
2. Then, use the check_complexity tool to analyze the code structure
3. Finally, provide a comprehensive review with these sections:
   - Summary: Brief overview of the code
   - Issues Found: List specific problems (if any)
   - Suggestions: Recommendations for improvement
   - Rating: Rate the code quality out of 10

Be constructive and specific in your feedback."""

    messages = [
        {
            "role": "user",
            "content": f"Please review this Python code:\n\n```python\n{code}\n```"
        }
    ]

    # Tool use loop
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        # If Claude is done, extract and return the review
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "No review generated"

        # If Claude wants to use tools, process each tool call
        if response.stop_reason == "tool_use":
            # Add assistant response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Process each tool use block
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })

            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })
        else:
            # Unexpected stop reason
            break

    return "Review process completed"
