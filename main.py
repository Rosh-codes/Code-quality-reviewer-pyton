"""CLI entry point for the code review agent."""

import argparse
from agent.reviewer import review_code
from tools.file_reader import read_file


def main():
    """Main CLI entry point for the code review agent."""
    parser = argparse.ArgumentParser(
        description="AI-based Python code review assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --file sample_code/good_code.py
  python main.py --code "def foo(): pass"
        """
    )

    # Create mutually exclusive group for file or code
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        type=str,
        help="Path to a Python file to review"
    )
    group.add_argument(
        "--code",
        type=str,
        help="Inline Python code to review"
    )

    args = parser.parse_args()

    # Get code content
    code = None
    if args.file:
        result = read_file(args.file)
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        code = result["content"]
    else:
        code = args.code

    # Print separator
    print("=" * 80)

    # Review the code
    review = review_code(code)
    print(review)

    # Print separator
    print("=" * 80)


if __name__ == "__main__":
    main()
