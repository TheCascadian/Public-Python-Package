import os
import sys
import json
import argparse
import ast
from typing import List, Dict, Tuple

def read_python_file(file_path: str) -> str:
    """
    Reads the content of a Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        str: Content of the Python file as a single string.
    """
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

def parse_python_content(content: str) -> List[Tuple[str, int, int, str]]:
    """
    Parses the Python content and extracts functions and classes.

    Args:
        content (str): The content of the Python file.

    Returns:
        List[Tuple[str, int, int, str]]: A list of tuples containing
            (name, start_line, end_line, type), where type is 'function' or 'class'.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error while parsing the Python file: {e}")
        sys.exit(1)
    
    snippets = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            type_ = 'function'
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', None)
            if end_line is None:
                # Fallback if end_lineno is not available (Python < 3.8)
                end_line = find_end_line(content, node)
            snippets.append((name, start_line, end_line, type_))
        elif isinstance(node, ast.ClassDef):
            name = node.name
            type_ = 'class'
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', None)
            if end_line is None:
                end_line = find_end_line(content, node)
            snippets.append((name, start_line, end_line, type_))
    
    return snippets

def find_end_line(content: str, node: ast.AST) -> int:
    """
    Estimates the end line of a node if end_lineno is not available.

    Args:
        content (str): The full content of the Python file.
        node (ast.AST): The AST node.

    Returns:
        int: Estimated end line number.
    """
    lines = content.splitlines()
    start = node.lineno - 1  # 0-based index
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == '':
            continue
        current_indent = len(lines[start]) - len(lines[start].lstrip())
        next_indent = len(lines[i]) - len(lines[i].lstrip())
        if next_indent <= current_indent and not lines[i].startswith((' ', '\t')):
            return i
    return len(lines)

def extract_snippet_content(content: str, start_line: int, end_line: int) -> List[str]:
    """
    Extracts the lines corresponding to a snippet.

    Args:
        content (str): The full content of the Python file.
        start_line (int): The starting line number (1-based).
        end_line (int): The ending line number (1-based).

    Returns:
        List[str]: List of code lines for the snippet.
    """
    lines = content.splitlines()
    # Adjust for 0-based indexing and slicing (end_line is inclusive)
    snippet_lines = lines[start_line - 1:end_line]
    # Remove any leading/trailing empty lines
    while snippet_lines and snippet_lines[0].strip() == '':
        snippet_lines.pop(0)
    while snippet_lines and snippet_lines[-1].strip() == '':
        snippet_lines.pop()
    return snippet_lines

def create_snippet_dict(name: str, prefix: str, description: str, code_lines: List[str]) -> Dict:
    """
    Creates a dictionary representing a VS Code snippet.

    Args:
        name (str): The name of the snippet.
        prefix (str): The prefix to trigger the snippet.
        description (str): A description of the snippet.
        code_lines (List[str]): List of code lines.

    Returns:
        Dict: A dictionary representing the snippet.
    """
    # Escape backslashes and double quotes
    escaped_lines = [line.replace('\\', '\\\\').replace('"', '\\"') for line in code_lines]
    # Replace tabs with spaces for consistency
    escaped_lines = [line.replace('\t', '    ') for line in escaped_lines]
    # Remove any trailing whitespace
    escaped_lines = [line.rstrip() for line in escaped_lines]
    snippet = {
        name: {
            "prefix": prefix,
            "body": escaped_lines,
            "description": description
        }
    }
    return snippet

def generate_snippets(content: str) -> Dict:
    """
    Generates a dictionary of snippets from the Python content.

    Args:
        content (str): The content of the Python file.

    Returns:
        Dict: A dictionary containing all snippets.
    """
    snippets_info = parse_python_content(content)
    snippets = {}

    for name, start, end, type_ in snippets_info:
        snippet_name = f"{type_.capitalize()} - {name}"
        snippet_prefix = f"{type_}.{name}"
        snippet_description = f"Snippet for {type_} '{name}'"
        snippet_body = extract_snippet_content(content, start, end)
        snippet = create_snippet_dict(snippet_name, snippet_prefix, snippet_description, snippet_body)
        snippets.update(snippet)
    
    return snippets

def write_json_snippets(snippets: Dict, output_path: str):
    """
    Writes the snippets dictionary to a JSON file.

    Args:
        snippets (Dict): The snippets dictionary.
        output_path (str): Path to the output JSON file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, indent=4)
        print(f"Snippets successfully written to '{output_path}'.")
    except Exception as e:
        print(f"Error writing JSON to '{output_path}': {e}")
        sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Convert a Python file into multiple VS Code JSON snippets based on functions and classes.")
    parser.add_argument('input_file', help="Path to the input Python (.py) file.")
    parser.add_argument('output_file', help="Path to the output JSON snippet file (e.g., snippets.json).")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    input_file = args.input_file
    output_file = args.output_file

    content = read_python_file(input_file)
    snippets = generate_snippets(content)

    if not snippets:
        print("No functions or classes found to create snippets.")
        sys.exit(0)
    
    write_json_snippets(snippets, output_file)

if __name__ == '__main__':
    main()
