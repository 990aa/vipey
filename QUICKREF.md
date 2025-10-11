# Vipey Quick Reference

## Installation
```bash
cd vipey
poetry install
poetry shell
```

## Basic Usage
```python
from vipey import Visualizer

viz = Visualizer()

@viz.capture
def my_function(data):
    # your code
    return result

result = my_function(test_data)
viz.save("output.html")
```

## Common Patterns

### Pattern 1: Wrapper Style
```python
viz = Visualizer()
captured = viz.capture(function)
result = captured(args)
viz.save("viz.html")
```

### Pattern 2: Decorator Style
```python
viz = Visualizer()

@viz.capture
def algorithm(data):
    # code
    return result

result = algorithm(data)
viz.save("viz.html")
```

### Pattern 3: Custom Serializer
```python
viz = Visualizer()

def my_serializer(obj):
    return {"type": "custom", "data": ...}

viz.register_serializer(MyClass, my_serializer)
```

## Commands

### Run Demo
```bash
poetry run python demo.py
```

### Run Tests
```bash
poetry run pytest tests/ -v
```

### Run Examples
```bash
poetry run python examples/binary_search.py
poetry run python examples/fibonacci.py
```

### Build Frontend
```bash
cd frontend
npm run build
cd ..
cp -r frontend/dist/* vipey/templates/
```

Or use:
```bash
./build_frontend.sh
```

## File Locations

- **Python package**: `vipey/`
- **Tests**: `tests/`
- **Examples**: `examples/`
- **Frontend**: `frontend/src/`
- **Templates**: `vipey/templates/`
- **Docs**: `*.md` files in root

## Common Issues

### "Nothing to save"
**Fix**: Run the captured function before calling save()

### Large HTML files
**Fix**: Use smaller test datasets

### Indentation errors
**Fix**: Already handled by textwrap.dedent()

## API Reference

### Visualizer Class
- `__init__()` - Create visualizer instance
- `capture(func)` - Wrap function for tracing
- `save(path)` - Save HTML visualization
- `register_serializer(type, func)` - Register custom serializer

### Output Structure
```python
{
    "frames": [
        {
            "line": int,
            "event_type": str,
            "locals": dict
        }
    ],
    "return_value": any,
    "source_code": str
}
```

## Frontend Components

- **App.tsx** - Main app, state management
- **CodePane.tsx** - Code display with highlighting
- **Controls.tsx** - Navigation controls
- **VisualizationPane.tsx** - Variable display
- **ArrayVisualizer.tsx** - Array visualization

## Links

- **README.md** - Overview
- **USAGE.md** - Complete guide
- **ARCHITECTURE.md** - Technical docs
- **CONTRIBUTING.md** - How to contribute
- **PROJECT_SUMMARY.md** - Project status

## Tips

1. Use small datasets for visualization
2. Meaningful variable names help readability
3. Add comments to explain algorithm logic
4. One algorithm per visualization
5. Test with edge cases

## Performance

- Tracing: 10-100x slower than normal
- Bundle: ~780KB
- Output: ~770-800KB per visualization
- Good for: <1000 frames

## Browser Support

- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Requires JavaScript enabled

---

**For detailed documentation, see USAGE.md**
