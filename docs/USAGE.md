# Vipey Usage Guide

A comprehensive guide to using Vipey for algorithm visualization.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

## Installation

### Prerequisites

- Python 3.12 or higher
- Node.js 16+ and npm (only needed for frontend development)
- Poetry (for dependency management)

### Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Vipey

```bash
# Clone the repository
git clone <repository-url>
cd vipey

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Quick Start

Create a file `my_algorithm.py`:

```python
from vipey import Visualizer

def find_max(numbers):
    """Find the maximum number in a list."""
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# Create visualizer
viz = Visualizer()

# Wrap your function
captured_find_max = viz.capture(find_max)

# Run it
result = captured_find_max([3, 7, 2, 9, 1, 5])
print(f"Maximum: {result}")

# Save visualization
viz.save("find_max_visualization.html")
```

Run it:

```bash
poetry run python my_algorithm.py
```

Open `find_max_visualization.html` in your browser!

## Basic Usage

### 1. Import and Initialize

```python
from vipey import Visualizer

viz = Visualizer()
```

### 2. Capture a Function

There are two ways to capture function execution:

#### Method A: Wrapper Style

```python
def my_function(x, y):
    z = x + y
    return z

captured = viz.capture(my_function)
result = captured(5, 10)
```

#### Method B: Decorator Style

```python
viz = Visualizer()

@viz.capture
def my_function(x, y):
    z = x + y
    return z

result = my_function(5, 10)
```

### 3. Save the Visualization

```python
viz.save("output.html")
```

Or with a custom path:

```python
viz.save("/path/to/my_visualization.html")
```

## Advanced Features

### Custom Data Type Serialization

If you have custom data structures, you can register serializers:

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_serializer(node):
    """Serialize a binary tree node."""
    if not node:
        return None
    return {
        "type": "tree",
        "value": node.val,
        "left": tree_serializer(node.left),
        "right": tree_serializer(node.right)
    }

# Register the serializer
viz = Visualizer()
viz.register_serializer(TreeNode, tree_serializer)

@viz.capture
def tree_height(root):
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))

# Now TreeNode objects will be properly serialized
root = TreeNode(1, TreeNode(2), TreeNode(3))
height = tree_height(root)
viz.save("tree_visualization.html")
```

### Working with Complex Data Structures

#### Lists/Arrays

Already supported out of the box:

```python
@viz.capture
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

viz.save("sorting.html")
```

#### Dictionaries

Also supported by default:

```python
@viz.capture
def count_frequency(items):
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq
```

### Multiple Visualizations

You can create multiple visualizations in one script:

```python
viz1 = Visualizer()
captured1 = viz1.capture(algorithm1)
result1 = captured1(data1)
viz1.save("viz1.html")

viz2 = Visualizer()
captured2 = viz2.capture(algorithm2)
result2 = captured2(data2)
viz2.save("viz2.html")
```

## Examples

### Example 1: Linear Search

```python
from vipey import Visualizer

def linear_search(arr, target):
    """Find target in array using linear search."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

viz = Visualizer()
captured = viz.capture(linear_search)
result = captured([4, 2, 7, 1, 9, 5], 7)
print(f"Found at index: {result}")
viz.save("linear_search.html")
```

### Example 2: Factorial (Recursive)

```python
from vipey import Visualizer

def factorial(n):
    """Calculate factorial recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

viz = Visualizer()
captured = viz.capture(factorial)
result = captured(5)
print(f"Factorial: {result}")
viz.save("factorial.html")
```

### Example 3: Two Pointers

```python
from vipey import Visualizer

def two_sum(numbers, target):
    """Find two numbers that sum to target."""
    left = 0
    right = len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None

viz = Visualizer()
captured = viz.capture(two_sum)
result = captured([1, 2, 3, 4, 5, 6], 9)
print(f"Indices: {result}")
viz.save("two_sum.html")
```

### Example 4: Matrix Operations

```python
from vipey import Visualizer

def transpose_matrix(matrix):
    """Transpose a 2D matrix."""
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    
    return result

viz = Visualizer()
captured = viz.capture(transpose_matrix)
matrix = [[1, 2, 3], [4, 5, 6]]
result = captured(matrix)
print(f"Transposed: {result}")
viz.save("transpose.html")
```

## Troubleshooting

### Issue: "Nothing to save" Error

**Problem**: Calling `viz.save()` before running a captured function.

**Solution**:
```python
viz = Visualizer()
captured = viz.capture(my_function)
result = captured(args)  # Must run the function first!
viz.save("output.html")
```

### Issue: Function Returns None

**Problem**: The original return value is being lost.

**Solution**: The captured function preserves return values:
```python
result = captured_function(args)  # result has the original return value
```

### Issue: IndentationError

**Problem**: `inspect.getsource()` includes indentation from nested functions.

**Status**: Already handled by `textwrap.dedent()` in `ast_parser.py`. If you still see this, please file a bug report.

### Issue: Large HTML Files

**Problem**: Visualization files are very large (> 10MB).

**Causes**:
- Many iterations (1000+ frames)
- Large data structures in local variables
- Deep recursion

**Solutions**:
1. Limit iterations for visualization purposes
2. Use smaller test data
3. Remove unnecessary local variables before the traced section

### Issue: Variables Not Showing

**Problem**: Some variables don't appear in the visualization.

**Common Causes**:
1. Variables starting with `__` are filtered out (Python internals)
2. Variables might not be in the local scope
3. Serialization failed (check console for errors)

**Debug**:
```python
# Add print statements before calling capture
print(locals())  # See what variables exist
```

## Best Practices

### 1. Use Small Test Cases

For visualization purposes, use small datasets:

```python
# Good for visualization
test_data = [5, 2, 8, 1, 9]

# Too large for meaningful visualization
# test_data = list(range(10000))
```

### 2. Meaningful Variable Names

Use descriptive variable names for better visualization:

```python
# Good
def binary_search(sorted_array, target):
    left_index = 0
    right_index = len(sorted_array) - 1
    # ...

# Less clear
def binary_search(arr, t):
    l = 0
    r = len(arr) - 1
    # ...
```

### 3. Add Comments

Comments help understand the algorithm when viewing the visualization:

```python
def bubble_sort(arr):
    n = len(arr)
    # Outer loop: number of passes
    for i in range(n):
        # Inner loop: compare adjacent elements
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap if out of order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

### 4. One Algorithm Per Visualization

Create separate visualizations for each algorithm:

```python
# Good
viz1 = Visualizer()
selection_sort_result = viz1.capture(selection_sort)([5, 2, 8])
viz1.save("selection_sort.html")

viz2 = Visualizer()
insertion_sort_result = viz2.capture(insertion_sort)([5, 2, 8])
viz2.save("insertion_sort.html")
```

### 5. Document Your Code

Add docstrings to help viewers understand:

```python
def dijkstra(graph, start):
    """
    Find shortest paths from start node using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency list representation {node: [(neighbor, weight), ...]}
        start: Starting node
        
    Returns:
        Dictionary of shortest distances {node: distance}
    """
    # Implementation...
```

### 6. Handle Edge Cases

Test with edge cases to ensure complete visualization:

```python
# Empty array
result1 = captured_function([])

# Single element
result2 = captured_function([42])

# Already sorted
result3 = captured_function([1, 2, 3, 4, 5])

# Reverse sorted
result4 = captured_function([5, 4, 3, 2, 1])
```

## Tips and Tricks

### Tip 1: Viewing in Browser

Most browsers can open HTML files directly:
- **Chrome/Edge**: Drag and drop, or `Ctrl+O`
- **Firefox**: `Ctrl+O` or File → Open File
- **Safari**: File → Open File

### Tip 2: Sharing Visualizations

The HTML files are self-contained and can be:
- Emailed as attachments
- Uploaded to file sharing services
- Hosted on GitHub Pages (https://github.com/990aa/vipey)
- Embedded in documentation

### Tip 3: Comparing Algorithms

Generate visualizations for multiple algorithms with the same data:

```python
test_data = [64, 34, 25, 12, 22, 11, 90]

# Bubble sort
viz1 = Visualizer()
viz1.capture(bubble_sort)(test_data.copy())
viz1.save("bubble_sort.html")

# Selection sort
viz2 = Visualizer()
viz2.capture(selection_sort)(test_data.copy())
viz2.save("selection_sort.html")

# Compare them side by side in separate browser tabs!
```

### Tip 4: Educational Use

Great for:
- Teaching algorithms
- Code reviews
- Debugging complex logic
- Understanding legacy code
- Creating tutorials

### Tip 5: Performance Note

Remember that tracing adds overhead:
- 10-100x slower than normal execution
- Use small datasets
- Don't use in production code

## Next Steps

- Explore the `examples/` directory for more samples
- Read `ARCHITECTURE.md` to understand how it works
- Check `CONTRIBUTING.md` to add your own visualizers
- Report bugs and request features on GitHub (https://github.com/990aa/vipey)

## Getting Help

- Check the [README.md](README.md) for overview
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Open an issue on GitHub (https://github.com/990aa/vipey) for bugs or questions
- Look at existing examples for patterns

Happy Visualizing! 🎉
