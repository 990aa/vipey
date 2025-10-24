# Vipey v0.2.0 - Quick Reference Card

## Installation
```bash
pip install -e .
# or
uv pip install -e .
```

## Basic Usage

### 1. Function Tracing
```python
from vipey import Visualizer

viz = Visualizer()
captured = viz.capture(my_function)
result = captured(args)
viz.save()  # → vipey/visualization.html
```

### 2. File Analysis
```python
viz = Visualizer()
info = viz.analyze_file("script.py")
# Returns: {functions, classes, complexity, lines, ...}
viz.save()
```

### 3. Project Analysis
```python
viz = Visualizer()
analysis = viz.analyze_project()
# Returns: {metrics, dependencies, git_history, call_graph}
viz.save(interactive=True)  # Opens localhost:5000
```

### 4. Combined
```python
viz = Visualizer()
captured = viz.capture(func)
result = captured(data)
viz.analyze_project()
viz.save()  # All tabs: Trace + Analysis + Docs
```

## API Reference

### `Visualizer()`
Main class for all operations.

### `capture(func)` → wrapped_function
Decorator to trace function execution.

### `analyze_file(path)` → dict
Analyze single file metrics.
- Returns: functions, classes, complexity, lines

### `analyze_project(path=None)` → dict
Analyze entire project.
- Returns: metrics, dependencies, git_history, call_graph

### `save(output_path="visualization.html", interactive=False)`
Save visualization.
- `interactive=False`: Static HTML in vipey/ folder
- `interactive=True`: Flask server on localhost:5000

### `register_serializer(type, func)`
Custom data type serialization.

## Output Modes

### Static (Default)
```python
viz.save()  # → vipey/visualization.html
viz.save("custom.html")  # → custom.html
```

### Interactive
```python
viz.save(interactive=True)  # → http://127.0.0.1:5000
```

## Visualization Tabs

1. **Function Trace** - Step-by-step execution
2. **Project Analysis** - Metrics and insights
3. **Documentation** - API reference

## Example Scripts

```bash
python demo.py              # Static visualization
python demo.py --interactive # Interactive dashboard
python test_features.py     # Feature validation
```

## Metrics Provided

### File-Level
- Functions, classes, imports
- Cyclomatic complexity
- Lines (code, comment, blank)
- Comment ratio

### Project-Level
- Total files, lines, size
- Language distribution
- Dependencies (Python, Node.js)
- Git history (commits, churn)
- Call graph metrics

## Dependencies

**Core**: None (basic tracing works standalone)

**Full Features**:
```
networkx, pandas, numpy, plotly, flask, 
flask-socketio, gitpython, markdown, 
pygments, scikit-learn, sentence-transformers
```

## Common Patterns

### Trace + Analyze
```python
viz = Visualizer()
sort = viz.capture(bubble_sort)
sort([5,2,8,1])
viz.analyze_project()
viz.save()
```

### Multiple Functions
```python
viz = Visualizer()
func1 = viz.capture(function1)
func2 = viz.capture(function2)
func1(data1)
func2(data2)
viz.save()
```

### Custom Serialization
```python
def tree_serializer(node):
    return {"val": node.val, "left": ..., "right": ...}

viz.register_serializer(TreeNode, tree_serializer)
```

## Troubleshooting

**Import errors?** → `pip install networkx pandas numpy`  
**Interactive mode fails?** → `pip install flask flask-socketio`  
**Git analysis fails?** → `pip install gitpython`  
**Large file errors?** → Files > 10MB are automatically skipped

## File Locations

- Static HTML: `vipey/visualization.html`
- Documentation: `DOCUMENTATION.md`
- API Reference: Inside visualization
- Examples: `examples/` folder
- Tests: `tests/` folder

## Version Info

**Version**: 0.2.0  
**Build System**: uv/pip with hatchling  
**Python**: >=3.12  
**Status**: Production Ready ✅

---

For complete documentation, see `DOCUMENTATION.md`
