# Vipey 🎯

**Vipey** is a Python visualization tool that captures and visualizes algorithm execution step-by-step. It combines a Python backend that traces code execution with a React/TypeScript frontend for interactive visualization.

## Features

- 🔍 **Step-by-step execution tracing** - Capture every line of code execution
- 📊 **Interactive visualization** - Navigate through execution with play/pause controls
- 🎨 **Syntax highlighting** - View your code with proper highlighting
- 📦 **Self-contained output** - Single HTML file with everything embedded
- 🔧 **Extensible** - Support for custom data structure serializers and visualizers
- 🚀 **Easy to use** - Simple decorator-based API

## Installation

### Using Poetry (Recommended)

```bash
git clone <repository-url>
cd vipey
poetry install
poetry shell
```

### From Source

```bash
git clone <repository-url>
cd vipey
pip install -e .
```

## Quick Start

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

Open `visualization.html` in your browser to see the interactive step-by-step execution!

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
