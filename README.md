# Code Review Agent

An AI-based code review assistant built with the Anthropic Claude API.

## Installation

1. Clone the repository
2. Create `.env` file from `.env.example`
3. Add your Anthropic API key to `.env`
4. Run `pip install -r requirements.txt`

## Usage

Review a Python file:
```bash
python main.py --file sample_code/good_code.py
```

Review inline code:
```bash
python main.py --code "def foo(): pass"
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Project Structure

- `agent/` - AI agent and tool orchestration
- `tools/` - Syntax and complexity analysis tools
- `tests/` - Unit tests
- `sample_code/` - Example Python files for testing
