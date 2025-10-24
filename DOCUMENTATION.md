# Vipey Documentation

**Version 0.2.0**

Vipey is a comprehensive Python visualization and analysis tool that combines algorithm execution tracing with advanced code intelligence and project analytics.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Configuration](#configuration)

---

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd vipey

# Install with uv
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
uv pip install -e ".[dev]"
```

---

## Quick Start

### Function Execution Tracing

Capture and visualize algorithm execution step-by-step:

```python
from vipey import Visualizer

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Create visualizer
viz = Visualizer()

# Capture execution
captured_sort = viz.capture(bubble_sort)

# Run with data
result = captured_sort([64, 34, 25, 12, 22, 11, 90])

# Save visualization
viz.save("visualization.html")
```

### Project Analysis

Analyze entire projects for comprehensive metrics:

```python
from vipey import Visualizer

viz = Visualizer()

# Analyze current project
analysis = viz.analyze_project()

# Save with interactive dashboard
viz.save("project_analysis.html", interactive=True)

# Or save as static HTML in vipey/ folder
viz.save(interactive=False)
```

---

## Core Features

### 1. **Function Execution Tracing**
- Step-by-step execution capture
- Variable state tracking
- Interactive timeline navigation
- Support for complex data structures

### 2. **Project Analytics**
- Comprehensive code metrics
- Language distribution analysis
- Complexity measurements
- Dependency tracking

### 3. **Git Integration**
- File churn analysis
- Commit history tracking
- Author statistics
- Change frequency metrics

### 4. **Code Intelligence**
- Call graph analysis
- Cyclomatic complexity
- Function and class counting
- Import dependency mapping

### 5. **Multi-Tab Visualization**
- Function trace view
- Project analysis dashboard
- Integrated documentation
- Interactive or static output

---

## API Reference

### Class: `Visualizer`

The main entry point for all vipey functionality.

#### Constructor

```python
viz = Visualizer()
```

Creates a new Visualizer instance.

---

### Method: `capture(func)`

Decorator to capture function execution.

**Parameters:**
- `func` (callable): The function to trace

**Returns:**
- Wrapped function that captures execution when called

**Example:**

```python
@viz.capture
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Or use it directly
captured_fib = viz.capture(fibonacci)
result = captured_fib(5)
```

---

### Method: `analyze_file(file_path)`

Analyze a single Python file for metrics and complexity.

**Parameters:**
- `file_path` (str): Path to the file to analyze

**Returns:**
- Dictionary containing file analysis results

**Example:**

```python
viz = Visualizer()
file_analysis = viz.analyze_file("my_script.py")
print(f"Functions: {file_analysis.get('functions', 0)}")
print(f"Classes: {file_analysis.get('classes', 0)}")
print(f"Complexity: {file_analysis.get('complexity_score', 0)}")
```

---

### Method: `analyze_project(project_path=None)`

Perform comprehensive project analysis.

**Parameters:**
- `project_path` (str, optional): Path to project directory. Defaults to current directory.

**Returns:**
- Dictionary containing comprehensive project analysis including:
  - File metrics
  - Language distribution
  - Dependencies
  - Git history
  - Call graph metrics

**Example:**

```python
viz = Visualizer()

# Analyze current directory
analysis = viz.analyze_project()

# Analyze specific project
analysis = viz.analyze_project("/path/to/project")

# Access metrics
print(f"Total files: {analysis['metrics']['total_files']}")
print(f"Total lines: {analysis['metrics']['total_lines']}")
print(f"Languages: {list(analysis['metrics']['language_distribution'].keys())}")
```

---

### Method: `save(output_path="visualization.html", interactive=False)`

Save visualization to HTML file.

**Parameters:**
- `output_path` (str): Path where HTML will be saved. Default: "visualization.html"
- `interactive` (bool): 
  - `True`: Opens local Flask server with interactive dashboard
  - `False`: Creates static HTML file in `vipey/` folder

**Behavior:**
- If `interactive=False` and using default output_path:
  - Creates `vipey/` folder in current directory
  - Saves as `vipey/visualization.html`
- If `interactive=True`:
  - Starts Flask server on `http://127.0.0.1:5000`
  - Opens browser automatically
  - Requires Flask to be installed

**Examples:**

```python
# Static HTML in vipey/ folder
viz.save(interactive=False)

# Static HTML with custom path
viz.save("my_analysis.html", interactive=False)

# Interactive dashboard
viz.save(interactive=True)

# Custom path with interactive server
viz.save("dashboard.html", interactive=True)
```

---

### Method: `register_serializer(data_type, serializer_func)`

Register custom serializer for complex data types.

**Parameters:**
- `data_type` (type): The type to serialize
- `serializer_func` (callable): Function that converts the type to JSON-serializable format

**Example:**

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def tree_serializer(node):
    if not node:
        return None
    return {
        "type": "tree",
        "value": node.val,
        "left": tree_serializer(node.left),
        "right": tree_serializer(node.right)
    }

viz = Visualizer()
viz.register_serializer(TreeNode, tree_serializer)
```

---

## Examples

### Example 1: Algorithm Visualization

```python
from vipey import Visualizer

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

viz = Visualizer()
search = viz.capture(binary_search)
result = search([1, 3, 5, 7, 9, 11, 13], 7)
viz.save("binary_search.html")
```

### Example 2: Quick Sort Visualization

```python
from vipey import Visualizer

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

viz = Visualizer()
sort = viz.capture(quick_sort)
result = sort([3, 6, 8, 10, 1, 2, 1])
viz.save("quick_sort.html")
```

### Example 3: Project Analysis

```python
from vipey import Visualizer

viz = Visualizer()

# Analyze your project
analysis = viz.analyze_project("./my_project")

# Print summary
metrics = analysis['metrics']
print(f"""
Project Analysis Summary:
------------------------
Total Files: {metrics['total_files']}
Total Lines: {metrics['total_lines']:,}
Code Lines: {metrics['code_lines']:,}
Functions: {metrics['total_functions']}
Classes: {metrics['total_classes']}
Average Complexity: {metrics['avg_complexity']:.2f}
""")

# Save interactive dashboard
viz.save(interactive=True)
```

### Example 4: File-Level Analysis

```python
from vipey import Visualizer

viz = Visualizer()

# Analyze a specific file
file_info = viz.analyze_file("complex_module.py")

print(f"File: {file_info['name']}")
print(f"Language: {file_info['language']}")
print(f"Functions: {file_info.get('functions', 0)}")
print(f"Classes: {file_info.get('classes', 0)}")
print(f"Complexity Score: {file_info.get('complexity_score', 0)}")
print(f"Comment Ratio: {file_info['comment_ratio']:.2%}")

# Save with project context
viz.save("file_analysis.html", interactive=False)
```

### Example 5: Combined Analysis

```python
from vipey import Visualizer

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

viz = Visualizer()

# Capture function execution
sort = viz.capture(merge_sort)
result = sort([38, 27, 43, 3, 9, 82, 10])

# Also analyze the project
viz.analyze_project()

# Save everything with all tabs
viz.save("complete_analysis.html", interactive=False)
```

---

## Advanced Usage

### Working with Complex Data Structures

```python
from vipey import Visualizer

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}

def graph_serializer(graph):
    return {
        "type": "graph",
        "nodes": graph.nodes,
        "edges": graph.edges
    }

viz = Visualizer()
viz.register_serializer(Graph, graph_serializer)

@viz.capture
def build_graph():
    g = Graph()
    g.nodes = [1, 2, 3, 4]
    g.edges = {1: [2, 3], 2: [4], 3: [4], 4: []}
    return g

result = build_graph()
viz.save("graph_visualization.html")
```

### Analyzing Large Projects

```python
from vipey import Visualizer
import json

viz = Visualizer()

# Analyze large project
analysis = viz.analyze_project("/path/to/large/project")

# Export metrics to JSON for further processing
with open("metrics.json", "w") as f:
    json.dump(analysis['metrics'], f, indent=2)

# Find most complex files
files = analysis['files']
complex_files = sorted(
    files, 
    key=lambda x: x.get('complexity_score', 0), 
    reverse=True
)[:10]

print("Top 10 Most Complex Files:")
for f in complex_files:
    print(f"  {f['name']}: {f.get('complexity_score', 0)}")

# Save visualization
viz.save("large_project_analysis.html", interactive=True)
```

### Batch Processing Multiple Files

```python
from vipey import Visualizer
from pathlib import Path

viz = Visualizer()
results = {}

# Analyze all Python files in a directory
for py_file in Path("./src").glob("**/*.py"):
    file_analysis = viz.analyze_file(str(py_file))
    results[str(py_file)] = file_analysis
    
# Find files with low comment ratio
low_comments = [
    (path, info['comment_ratio']) 
    for path, info in results.items() 
    if info['comment_ratio'] < 0.1
]

print("Files with < 10% comments:")
for path, ratio in low_comments:
    print(f"  {Path(path).name}: {ratio:.2%}")
```

---

## Configuration

### Output Modes

Vipey supports two output modes:

#### Static Mode (Default)
```python
viz.save(interactive=False)  # Creates vipey/visualization.html
viz.save("custom.html", interactive=False)  # Custom path
```

Creates a self-contained HTML file with all assets embedded. Perfect for:
- Sharing visualizations
- Offline viewing
- Version control
- Documentation

#### Interactive Mode
```python
viz.save(interactive=True)  # Starts server on http://127.0.0.1:5000
```

Starts a local Flask server with real-time updates. Best for:
- Development
- Live analysis
- Interactive exploration
- Team demos

### Directory Structure

When using static mode with defaults:
```
your-project/
├── your_script.py
├── vipey/
│   └── visualization.html  # Created here
└── ...
```

### Dependencies

**Core Dependencies** (always installed):
- No external dependencies for basic function tracing

**Optional Dependencies** (for full features):
- `networkx` - Call graph analysis
- `pandas` - Data processing
- `numpy` - Numerical computations
- `plotly` - Advanced visualizations
- `flask` - Interactive mode
- `flask-socketio` - Real-time updates
- `gitpython` - Git integration
- `markdown` - Documentation rendering
- `pygments` - Syntax highlighting
- `scikit-learn` - Complexity analysis
- `sentence-transformers` - AI-powered insights

Install all optional dependencies:
```bash
uv pip install -e ".[dev]"
```

---

## Tips & Best Practices

### 1. Performance Optimization

For large projects, limit analysis scope:
```python
# Analyze only specific directories
analysis = viz.analyze_project("/project/src")  # Just src/

# Use file-level analysis for single files
file_info = viz.analyze_file("large_file.py")
```

### 2. Memory Management

When tracing recursive functions, be mindful of memory:
```python
# Limit recursion depth for visualization
import sys
sys.setrecursionlimit(100)  # Adjust as needed

viz = Visualizer()
captured = viz.capture(recursive_function)
result = captured(small_input)  # Use smaller inputs
```

### 3. Custom Visualizations

Extend vipey with custom serializers for your data types:
```python
# Always provide meaningful structure in serializers
def custom_serializer(obj):
    return {
        "type": obj.__class__.__name__,
        "data": obj.to_dict(),  # Your custom method
        "metadata": {"timestamp": time.time()}
    }
```

### 4. Continuous Analysis

Integrate vipey into CI/CD:
```python
# ci_analysis.py
from vipey import Visualizer

viz = Visualizer()
analysis = viz.analyze_project()

# Check complexity threshold
avg_complexity = analysis['metrics']['avg_complexity']
if avg_complexity > 10:
    print(f"WARNING: High complexity: {avg_complexity}")
    exit(1)
```

---

## Troubleshooting

### Issue: Import errors for optional dependencies

**Solution:** Install optional dependencies:
```bash
uv pip install networkx pandas numpy flask markdown pygments
```

### Issue: Interactive mode doesn't start

**Solution:** Ensure Flask is installed:
```bash
uv pip install flask flask-socketio
```

### Issue: Git analysis fails

**Solution:** Ensure GitPython is installed and project has .git:
```bash
uv pip install gitpython
# Verify git repository
git status
```

### Issue: Large files cause memory issues

**Solution:** Vipey automatically skips files > 10MB. Adjust in analyzer.py if needed.

---

## Contributing

We welcome contributions! Areas for enhancement:
- Additional visualizers for data structures
- Performance optimizations
- More language support
- Enhanced AI-powered insights
- Custom themes

---

## License

MIT License - see LICENSE file for details.

---

## Support

For issues, questions, or contributions:
- GitHub Issues: [repository-url]/issues
- Documentation: This file
- Examples: `/examples` directory

---

**Happy Coding! 🎯**
