# Vipey Architecture Documentation

## Overview

Vipey is a dual-language project that combines Python for code tracing and TypeScript/React for visualization. The architecture is designed to be modular, extensible, and easy to understand.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      User Code                                    │
│  @viz.capture                                                     │
│  def algorithm():                                                 │
│      ...                                                          │
└────────────────┬────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Python Backend                                       │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ AST Parser     │  │   Tracer        │  │  Renderer      │     │
│  │                │  │                 │  │                │     │
│  │ Analyzes       │→ │ sys.settrace   │→ │ Generates      │     │
│  │ code           │  │ captures        │  │ HTML           │     │
│  │ structure      │  │ execution       │  │                │     │
│  └──────────────┘  └──────────────┘  └──────┬───────┘    │
│                                                      │            │
└──────────────────────────────────────────────┼──────────┘
                                               │
                                               ▼
                                    ┌──────────────────┐
                                    │  Storyboard         │
                                    │  JSON Data          │
                                    │  {                  │
                                    │    frames: [...],   │
                                    │    source: "..."    │
                                    │  }                  │
                                    └────────┬─────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────┐
│              TypeScript Frontend                                  │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐    │
│  │                   App.tsx                                 │    │
│  │  - Loads JSON data                                        │    │
│  │  - Manages current step                                   │    │
│  │  - Handles play/pause                                     │    │
│  └───┬────────────┬──────────────┬──────────────┬───┘    │
│       │              │                │                 │         │
│       ▼             ▼                ▼                ▼         │
│  ┌────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐      │
│  │CodePane │  │Controls   │  │Visualize   │  │  Other     │      │
│  │         │  │           │  │Pane        │  │Components  │      │
│  │Syntax   │  │Slider +   │  │Displays    │  │            │      │
│  │Highlight│  │Buttons    │  │Variables   │  │            │      │
│  └────────┘  └─────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Browser      │
                  │  (Output)     │
                  └─────────────┘
```

## Component Details

### Python Backend

#### 1. AST Parser (`ast_parser.py`)

**Purpose**: Analyze the source code structure to understand what's happening at each line.

**How it works**:
- Uses Python's `ast` module to parse source code into an Abstract Syntax Tree
- Walks the AST to identify node types (assignments, comparisons, loops, etc.)
- Creates a mapping: `{line_number: event_type}`
- This helps the tracer understand what kind of operation is happening

**Example Output**:
```python
{
    1: "function_def",
    2: "assignment",
    3: "loop",
    4: "comparison",
    5: "assignment"
}
```

#### 2. Tracer (`tracer.py`)

**Purpose**: Capture the execution of code line-by-line.

**How it works**:
- Uses `sys.settrace()` to hook into Python's execution
- For each line executed:
  - Captures line number
  - Captures local variables (serialized to JSON)
  - Records the event type from the AST map
  - Creates a "frame" object with all this data
- Stores all frames in a "storyboard" list

**Key Features**:
- Smart serialization (handles lists, dicts, primitives)
- Skips `__` variables
- Captures return values
- Includes source code in output

**Example Frame**:
```python
{
    "line": 5,
    "event_type": "assignment",
    "locals": {
        "x": 5,
        "y": 10,
        "arr": [1, 2, 3]
    }
}
```

#### 3. Renderer (`renderer.py`)

**Purpose**: Package everything into a single self-contained HTML file.

**How it works**:
1. Reads the built frontend HTML template
2. Finds all CSS and JS asset references
3. Inlines those assets (reads files and embeds content)
4. Injects the storyboard JSON data
5. Writes the final HTML file

**Why inline assets?**
- Creates a single, portable HTML file
- No external dependencies
- Easy to share and view anywhere

#### 4. Public API (`__init__.py`)

**Purpose**: Provide a simple, user-friendly interface.

**Key Class: Visualizer**

```python
class Visualizer:
    def capture(self, func):
        # Decorator that wraps a function
        # Returns a new function that traces execution
    
    def save(self, output_path):
        # Saves the captured execution as HTML
    
    def register_serializer(self, data_type, serializer_func):
        # Allows custom data type visualization
```

### TypeScript Frontend

#### 1. App.tsx (Main Component)

**Responsibilities**:
- Load storyboard data from injected JSON
- Manage application state (current step, play/pause)
- Coordinate child components
- Handle play animation (setInterval)

**State Management**:
```typescript
const [storyboard, setStoryboard] = useState<StoryboardData | null>(null);
const [currentStep, setCurrentStep] = useState(0);
const [isPlaying, setIsPlaying] = useState(false);
```

#### 2. CodePane.tsx

**Purpose**: Display source code with syntax highlighting.

**Features**:
- Uses `react-syntax-highlighter`
- Highlights current line (yellow background)
- Shows line numbers
- Python syntax highlighting

#### 3. Controls.tsx

**Purpose**: Navigation controls for stepping through execution.

**Features**:
- Previous/Next buttons
- Play/Pause button
- Slider for jumping to any step
- Shows current step count

#### 4. VisualizationPane.tsx

**Purpose**: Display variable values at the current step.

**Features**:
- Shows all local variables
- Detects array types → uses ArrayVisualizer
- Shows primitive types as JSON
- Extensible for custom visualizers

#### 5. ArrayVisualizer.tsx

**Purpose**: Visual representation of arrays.

**Features**:
- Shows each element in a box
- Displays index numbers
- Responsive layout
- Can be extended for highlighting, comparisons, etc.

## Data Flow

### 1. Capture Phase

```
User Function
    ↓
inspect.getsource() → Source Code (string)
    ↓
analyze_code() → AST Map
    ↓
Tracer.trace_function()
    ↓ (for each line)
sys.settrace callback
    ↓
Create Frame {line, locals, event_type}
    ↓
Append to Storyboard
```

### 2. Render Phase

```
Storyboard (Python dict)
    ↓
json.dumps()
    ↓
Storyboard (JSON string)
    ↓
Inject into HTML template
    ↓
Replace %%VIPEY_STORYBOARD_DATA%%
    ↓
Single HTML file
```

### 3. Display Phase

```
Browser opens HTML
    ↓
React loads
    ↓
Read <script id="storyboard-data">
    ↓
JSON.parse()
    ↓
Storyboard (JavaScript object)
    ↓
App.tsx manages state
    ↓
Render current frame
    ↓
User interactions update currentStep
```

## Extensibility Points

### 1. Custom Data Type Serializers (Python)

```python
class MyDataStructure:
    pass

def my_serializer(obj):
    return {
        "type": "my_custom_type",
        "data": {...}
    }

viz.register_serializer(MyDataStructure, my_serializer)
```

### 2. Custom Visualizers (TypeScript)

```typescript
// In VisualizationPane.tsx
if (variable.type === 'my_custom_type') {
    return <MyCustomVisualizer data={variable.data} />;
}
```

### 3. Additional AST Analysis

```python
# In ast_parser.py
elif isinstance(node, ast.While):
    line_map[node.lineno] = 'while_loop'
elif isinstance(node, ast.FunctionDef):
    line_map[node.lineno] = 'function_def'
```

## Build Process

### Frontend Build

```bash
cd frontend
npm run build
```

**What happens**:
1. Vite bundles all React/TypeScript code
2. Minifies and optimizes
3. Creates `dist/` folder with:
   - `index.html`
   - `assets/index-[hash].js`
   - `assets/index-[hash].css`

### Asset Copy

```bash
cp -r frontend/dist/* vipey/templates/
```

**Why**:
- Python package needs the built assets
- Templates folder is included in distribution
- Renderer can find and inline them

## Performance Considerations

### Python Backend

- **sys.settrace overhead**: Tracing adds significant overhead (~10-100x slower)
- **Memory usage**: Each frame stores a copy of all locals
- **Serialization**: Deep copying objects can be expensive

**Optimizations**:
- Only serialize necessary variables
- Limit trace depth for recursive functions
- Option to sample (trace every Nth line)

### Frontend

- **Bundle size**: ~780KB (can be code-split)
- **Rendering**: React handles updates efficiently
- **Large traces**: Consider virtualization for 1000+ frames

## Security Considerations

- Visualization files contain source code (be careful with proprietary code)
- Local variables may contain sensitive data
- HTML is self-contained (no external requests, safe to share)

## Future Enhancements

1. **Tree/Graph Visualizers**: For hierarchical data structures
2. **Performance Profiling**: Show time spent on each line
3. **Memory Tracking**: Visualize memory allocation
4. **Comparison Mode**: Compare two executions side-by-side
5. **Export Options**: Save as video, GIF, or image sequence
6. **Collaborative Features**: Share and annotate visualizations
7. **IDE Integration**: VS Code extension for in-editor visualization

## Testing Strategy

### Python Tests

```python
# tests/test_tracer.py
- test_tracer_basic(): Verify basic tracing works
- test_tracer_with_array(): Test with array operations
- test_visualizer_save(): Ensure HTML generation works
```

### Frontend Tests (TODO)

- Component unit tests (Jest + React Testing Library)
- Integration tests (Playwright/Cypress)
- Visual regression tests

## Deployment

### As a Library

```bash
poetry build
poetry publish
```

### Standalone Examples

- Include pre-built visualizations in `examples/`
- Host on GitHub Pages (https://github.com/990aa/vipey)
- Include in documentation

## Contributing Guide

1. **Backend changes**: Update Python code, run tests
2. **Frontend changes**: 
   - Edit components in `frontend/src/`
   - Run `npm run dev` for hot reload
   - Build with `npm run build`
   - Copy to templates
3. **Documentation**: Update this file and README.md

## Conclusion

Vipey's architecture is designed to be:
- **Simple**: Clear separation between tracing and visualization
- **Extensible**: Easy to add new visualizers and serializers
- **Portable**: Single HTML file output
- **Educational**: Great for understanding algorithm behavior

The dual-language approach leverages Python's introspection capabilities and React's powerful UI framework to create an interactive learning tool.