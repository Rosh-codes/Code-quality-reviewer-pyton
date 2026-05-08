"""Unit tests for code review agent tools."""

import pytest
import tempfile
import os
from tools.syntax_checker import check_syntax
from tools.complexity_checker import check_complexity
from tools.file_reader import read_file


class TestSyntaxChecker:
    """Tests for syntax_checker module."""

    def test_syntax_valid_code(self):
        """Test that valid Python code passes syntax check."""
        code = "def foo():\n    return 42"
        result = check_syntax(code)
        assert result["status"] == "ok"
        assert result["errors"] == []

    def test_syntax_invalid_code(self):
        """Test that invalid Python code is caught."""
        code = "def foo(\n    return"
        result = check_syntax(code)
        assert result["status"] == "error"
        assert len(result["errors"]) > 0
        assert "line" in result["errors"][0]
        assert "message" in result["errors"][0]

    def test_syntax_empty_input(self):
        """Test that empty string is valid Python code."""
        code = ""
        result = check_syntax(code)
        assert result["status"] == "ok"
        assert result["errors"] == []


class TestComplexityChecker:
    """Tests for complexity_checker module."""

    def test_complexity_counts_functions(self):
        """Test that function count is correct."""
        code = """
def function_one():
    pass

def function_two():
    pass
"""
        result = check_complexity(code)
        assert result["function_count"] == 2
        assert "function_one" in result["function_names"]
        assert "function_two" in result["function_names"]

    def test_complexity_counts_classes(self):
        """Test that class count is correct."""
        code = """
class MyClass:
    def method(self):
        pass
"""
        result = check_complexity(code)
        assert result["class_count"] == 1

    def test_complexity_with_syntax_error(self):
        """Test that syntax errors are handled gracefully."""
        code = "def foo(\n    return"
        result = check_complexity(code)
        assert "error" in result
        assert result["error"] == "Cannot analyze - syntax error in code"


class TestFileReader:
    """Tests for file_reader module."""

    def test_file_reader_not_found(self):
        """Test that missing files are handled."""
        result = read_file("/nonexistent/path/to/file.py")
        assert "error" in result
        assert result["error"] == "File not found"

    def test_file_reader_wrong_extension(self):
        """Test that non-.py files are rejected."""
        # Create a temporary file with .txt extension
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            temp_path = f.name
            f.write(b"some content")

        try:
            result = read_file(temp_path)
            assert "error" in result
            assert result["error"] == "Only Python files supported"
        finally:
            os.unlink(temp_path)

    def test_file_reader_success(self):
        """Test successful file reading."""
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as f:
            temp_path = f.name
            f.write("def test_function():\n    pass")

        try:
            result = read_file(temp_path)
            assert "error" not in result
            assert "content" in result
            assert "filepath" in result
            assert result["filepath"] == temp_path
            assert "def test_function" in result["content"]
        finally:
            os.unlink(temp_path)
