# Code Review Agent

An AI-based code review assistant built with the Anthropic Claude API.

## Installation

1. Clone the repository
2. Create `.env` file from `.env.example` and add your Anthropic API key
3. Run `pip install -r requirements.txt`

## Usage

Review a Python file:
```bash
python main.py --file sample_code/good_code.py
```

Review inline Python code:
```bash
python main.py --code "def foo(): pass"
```

## Testing

Run all unit tests:
```bash
pytest tests/
```

## Project Structure

- **agent/** - AI agent and tool orchestration
  - `reviewer.py` - Claude-based code reviewer with tool use loop
  - `__init__.py` - Package initialization

- **tools/** - Code analysis tools
  - `syntax_checker.py` - Validates Python syntax using AST
  - `complexity_checker.py` - Analyzes code structure and metrics
  - `file_reader.py` - Reads Python files safely
  - `__init__.py` - Package initialization

- **tests/** - Unit tests
  - `test_tools.py` - Pytest unit tests for all tools
  - `__init__.py` - Package initialization

- **sample_code/** - Example Python files
  - `good_code.py` - Well-written, documented code
  - `bad_code.py` - Code with poor practices and style issues

- **main.py** - CLI entry point
- **requirements.txt** - Python dependencies
- **.env.example** - Template for environment variables
- **.gitignore** - Git ignore patterns
- **README.md** - Project documentation
