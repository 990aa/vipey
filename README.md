# Vipey 🎯

**Vipey** is a comprehensive Python visualization and analysis tool that combines algorithm execution tracing with advanced code intelligence and project analytics. Version 0.2.0 brings powerful new features including project-wide analysis, git integration, and multi-tab visualizations.

## Features

### Function Execution Tracing
- 🔍 **Step-by-step execution tracing** - Capture every line of code execution
- 📊 **Interactive visualization** - Navigate through execution with play/pause controls
- 🎨 **Syntax highlighting** - View your code with proper highlighting
- 📦 **Self-contained output** - Single HTML file with everything embedded
- 🔧 **Extensible** - Support for custom data structure serializers and visualizers

### Project Analytics (NEW in v0.2.0)
- � **Comprehensive code metrics** - Lines of code, functions, classes, complexity
- 🌐 **Language distribution** - Multi-language project analysis
- 📚 **Dependency tracking** - Python and Node.js dependency analysis
- 🔄 **Git integration** - File churn, commit history, and author statistics
- 🕸️ **Call graph analysis** - Function relationships and architectural metrics
- 📑 **Multi-tab visualization** - Function trace, project analysis, and documentation in one view

### Output Modes
- 🚀 **Interactive Mode** - Local Flask server with real-time dashboard
- 📄 **Static Mode** - Self-contained HTML files for easy sharing

## Installation

### Using uv (Recommended)

```bash
git clone <repository-url>
cd vipey
uv pip install -e .
```

### Using pip

```bash
git clone <repository-url>
cd vipey
pip install -e .
```

## Quick Start

### Function Execution Tracing

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

# Save visualization (creates vipey/visualization.html)
viz.save(interactive=False)
```

### Project Analysis

```python
from vipey import Visualizer

viz = Visualizer()

# Analyze entire project
analysis = viz.analyze_project()

# Print summary
metrics = analysis['metrics']
print(f"Total files: {metrics['total_files']}")
print(f"Total lines: {metrics['total_lines']:,}")
print(f"Functions: {metrics['total_functions']}")

# Save with interactive dashboard
viz.save(interactive=True)  # Opens browser at http://127.0.0.1:5000
```

### Combined Analysis

```python
from vipey import Visualizer

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

viz = Visualizer()

# Capture function execution
fib = viz.capture(fibonacci)
result = fib(5)

# Also analyze the project
viz.analyze_project()

# Save everything in multi-tab view
viz.save(interactive=False)  # Creates vipey/visualization.html
```

Open `vipey/visualization.html` in your browser to see:
- **Function Trace Tab**: Step-by-step execution visualization
- **Project Analysis Tab**: Comprehensive metrics and insights
- **Documentation Tab**: Complete API reference

## Structure

```
vipey/
├── pyproject.toml      # uv/pip configuration
├── README.md           # This file
├── DOCUMENTATION.md    # Complete API documentation
├── demo.py             # Demo script
├── tests/              # Pytest tests
│   └── test_tracer.py
├── examples/           # Example visualizations
│   ├── binary_search.py
│   └── fibonacci.py
├── frontend/           # React/TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArrayVisualizer.tsx
│   │   │   ├── CodePane.tsx
│   │   │   ├── Controls.tsx
│   │   │   └── VisualizationPane.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
└── vipey/              # Python library
    ├── __init__.py     # Public API (Visualizer class)
    ├── analyzer.py     # NEW: Project analysis engine
    ├── ast_parser.py   # Code structure analysis
    ├── tracer.py       # Execution tracing
    ├── renderer.py     # Multi-tab HTML generation
    └── templates/      # Built frontend assets
```

## How It Works

### Python Backend

1. **AST Parser** (`ast_parser.py`): Analyzes your code structure using Python's AST module
2. **Tracer** (`tracer.py`): Uses `sys.settrace()` to capture execution frame-by-frame
3. **Analyzer** (`analyzer.py`): Project-wide metrics, complexity analysis, and git integration
4. **Renderer** (`renderer.py`): Bundles everything into multi-tab HTML visualizations

### TypeScript Frontend

1. **App.tsx**: Main component managing state and navigation
2. **CodePane**: Displays source code with line highlighting
3. **VisualizationPane**: Shows variable states at each step
4. **Controls**: Play/pause and step navigation controls

## Examples

### Running Examples

```bash
# Demo: Bubble Sort + Project Analysis
python demo.py

# Demo with Interactive Dashboard
python demo.py --interactive

# Example: Binary Search
python examples/binary_search.py

# Example: Fibonacci
python examples/fibonacci.py
```

### API Reference

For complete API documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

#### Key Methods

- `viz.capture(func)` - Capture function execution
- `viz.analyze_file(file_path)` - Analyze single file metrics
- `viz.analyze_project(project_path)` - Analyze entire project
- `viz.save(output_path, interactive=False)` - Save visualization
- `viz.register_serializer(type, func)` - Custom data serializers

### Custom Serializers

For custom data structures, register a serializer:

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

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev  # Start dev server
npm run build  # Build for production
```

After building, copy assets to templates:

```bash
# Windows
xcopy /E /I frontend\dist vipey\templates

# Linux/Mac
cp -r frontend/dist/* vipey/templates/
```

### Running Tests

```bash
pytest tests/ -v
```

## What's New in v0.2.0

### Major Features
- ✨ **Project-wide analysis** - Analyze entire codebases for metrics and insights
- 📊 **Multi-tab visualizations** - Function trace, project analysis, and docs in one view
- 🔄 **Git integration** - Track file churn, commits, and contributors
- 🌐 **Multi-language support** - Analyze Python, JavaScript, TypeScript, and more
- 📈 **Complexity metrics** - Cyclomatic complexity, function/class counts
- 🕸️ **Call graph analysis** - Understand function relationships
- 📚 **Dependency tracking** - Python and Node.js dependency analysis
- 🚀 **Interactive mode** - Flask-based live dashboard
- 📄 **Static mode** - Self-contained HTML in vipey/ folder

### Build System
- 🔧 **Migrated to uv** - Modern Python package management
- 📦 **Hatchling backend** - Faster, more reliable builds

### Documentation
- 📖 **Comprehensive DOCUMENTATION.md** - Complete API reference with examples
- 🎯 **Inline documentation** - Rendered in visualization tab

## Architecture

### Output Modes

#### Static Mode (Default)
```python
viz.save(interactive=False)  # Creates vipey/visualization.html
```

Creates a self-contained HTML file in the `vipey/` folder with all assets embedded.

#### Interactive Mode
```python
viz.save(interactive=True)  # Starts server at http://127.0.0.1:5000
```

Starts a Flask server with real-time dashboard and auto-opens browser.

## Dependencies

**Core**: No external dependencies for basic tracing

**Full Features**:
- `networkx` - Call graph analysis
- `pandas` - Data processing
- `numpy` - Numerical computations
- `plotly` - Visualizations
- `flask` + `flask-socketio` - Interactive mode
- `gitpython` - Git integration
- `markdown` + `pygments` - Documentation rendering
- `scikit-learn` - Complexity analysis
- `sentence-transformers` - AI insights

Install all:
```bash
pip install -e .  # All dependencies included
```

## Contributing

Contributions are welcome! Areas for improvement:

- Additional visualizers (graphs, trees, matrices)
- Performance optimizations for large traces
- More language support for analysis
- Enhanced AI-powered insights
- Custom themes and styling options
- Export options (video, gif, images)

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- Python 3.12+
- React 18
- TypeScript
- Vite
- Flask
- NetworkX
- Pandas
- And many other amazing open-source tools

---

**Happy Coding! 🎯**

## Structure

```
vipey/
├── pyproject.toml      # Poetry configuration
├── README.md           # This file
├── demo.py            # Demo script
├── tests/             # Pytest tests
│   └── test_tracer.py
├── examples/          # Example visualizations
│   ├── binary_search.py
│   └── fibonacci.py
├── frontend/          # React/TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArrayVisualizer.tsx
│   │   │   ├── CodePane.tsx
│   │   │   ├── Controls.tsx
│   │   │   └── VisualizationPane.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
└── vipey/             # Python library
    ├── __init__.py    # Public API (Visualizer class)
    ├── ast_parser.py  # Code structure analysis
    ├── tracer.py      # Execution tracing
    ├── renderer.py    # HTML generation
    └── templates/     # Built frontend assets
```

## How It Works

### Python Backend

1. **AST Parser** (`ast_parser.py`): Analyzes your code structure using Python's AST module
2. **Tracer** (`tracer.py`): Uses `sys.settrace()` to capture execution frame-by-frame
3. **Renderer** (`renderer.py`): Bundles the frontend and data into a single HTML file

### TypeScript Frontend

1. **App.tsx**: Main component managing state and navigation
2. **CodePane**: Displays source code with line highlighting
3. **VisualizationPane**: Shows variable states at each step
4. **Controls**: Play/pause and step navigation controls

## Examples

### Running Examples

```bash
# Demo: Bubble Sort
poetry run python demo.py

# Example: Binary Search
poetry run python examples/binary_search.py

# Example: Fibonacci
poetry run python examples/fibonacci.py
```

### Custom Serializers (Advanced)

For custom data structures, register a serializer:

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

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev  # Start dev server
npm run build  # Build for production
```

After building, copy assets to templates:

```bash
cp -r frontend/dist/* vipey/templates/
```

### Running Tests

```bash
poetry run pytest tests/ -v
```

## Architecture Details

### Phase 1: Project Setup ✅
- Poetry project initialization
- Directory structure
- Frontend and backend scaffolding

### Phase 2: TypeScript Frontend ✅
- Vite/React setup
- Component development (CodePane, Controls, VisualizationPane)
- State management in App.tsx

### Phase 3: Python Backend ✅
- AST parser for code analysis
- sys.settrace() based execution tracer
- Variable serialization

### Phase 4: The Bridge ✅
- Frontend build process
- Asset inlining in renderer
- Single-file HTML output

### Phase 5: Public API ✅
- Simple decorator-based interface
- Visualizer class
- Easy save functionality

### Phase 6: Extensibility 🚧
- Custom serializer registration (implemented)
- Pluggable visualizers (basic implementation)
- Additional data structure visualizers (in progress)

## Contributing

Contributions are welcome! Areas for improvement:

- Additional visualizers (graphs, trees, matrices)
- Performance optimizations for large traces
- More sophisticated AST analysis
- Custom themes and styling options
- Export options (video, gif, images)

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- Python 3.12+
- React 18
- TypeScript
- Vite
- react-syntax-highlighter
- Poetry for dependency management
