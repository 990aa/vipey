# ast_parser.py
import ast
import textwrap
from typing import Dict

def analyze_code(source_code: str) -> Dict[int, str]:
    """Analyze code and map line numbers to event types."""
    # Remove leading indentation that inspect.getsource() might include
    source_code = textwrap.dedent(source_code)
    
    tree = ast.parse(source_code)
    line_map = {}
    for node in ast.walk(tree):
        if hasattr(node, 'lineno'):
            if isinstance(node, ast.Assign):
                line_map[node.lineno] = 'assignment'
            elif isinstance(node, ast.Compare):
                line_map[node.lineno] = 'comparison'
            elif isinstance(node, ast.For):
                line_map[node.lineno] = 'loop'
            elif isinstance(node, ast.If):
                line_map[node.lineno] = 'condition'
            # Add more event types as needed
    return line_map
