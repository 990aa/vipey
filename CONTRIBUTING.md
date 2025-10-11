# Contributing to Vipey

Thank you for your interest in contributing to Vipey! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub (https://github.com/990aa/vipey)
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/990aa/vipey.git
   cd vipey
   ```

3. **Install dependencies**:
   ```bash
   # Python dependencies
   poetry install
   
   # Frontend dependencies
   cd frontend
   npm install
   cd ..
   ```

4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Python Backend Changes

1. Make your changes in the `vipey/` directory
2. Run tests:
   ```bash
   poetry run pytest tests/ -v
   ```
3. Ensure code quality:
   ```bash
   poetry run black vipey/  # Format code (if black is installed)
   poetry run pylint vipey/ # Lint code (if pylint is installed)
   ```

### Frontend Changes

1. Make your changes in `frontend/src/`
2. Test locally:
   ```bash
   cd frontend
   npm run dev  # Opens dev server at http://localhost:5173
   ```
3. Build and update templates:
   ```bash
   npm run build
   cd ..
   cp -r frontend/dist/* vipey/templates/
   ```
   Or use the build script:
   ```bash
   ./build_frontend.sh
   ```

### Testing Your Changes

1. Run the demo script:
   ```bash
   poetry run python demo.py
   ```

2. Run all tests:
   ```bash
   poetry run pytest tests/ -v
   ```

3. Test examples:
   ```bash
   poetry run python examples/binary_search.py
   poetry run python examples/fibonacci.py
   ```

## Types of Contributions

### 🐛 Bug Fixes

- Search existing issues to see if the bug is already reported
- Create a new issue if not found, describing the bug and steps to reproduce
- Submit a PR with the fix, referencing the issue number

### ✨ New Features

#### New Visualizers

To add a new data structure visualizer:

1. **Python side** (`vipey/tracer.py` or custom serializer):
   ```python
   def custom_serializer(obj):
       return {
           "type": "my_type",
           "data": {...}  # Your serialized data
       }
   ```

2. **TypeScript side** (`frontend/src/components/`):
   ```typescript
   // Create MyTypeVisualizer.tsx
   export const MyTypeVisualizer: React.FC<Props> = ({ data }) => {
       return <div>/* Your visualization */</div>;
   };
   ```

3. **Wire it up** in `VisualizationPane.tsx`:
   ```typescript
   if (variable.type === 'my_type') {
       return <MyTypeVisualizer data={variable.data} />;
   }
   ```

#### New AST Analysis Features

Add to `vipey/ast_parser.py`:
```python
elif isinstance(node, ast.NewNodeType):
    line_map[node.lineno] = 'new_event_type'
```

### 📚 Documentation

- Improve README.md, ARCHITECTURE.md, or code comments
- Add examples in the `examples/` directory
- Create tutorials or guides

### 🧪 Tests

- Add test cases in `tests/`
- Improve test coverage
- Add integration tests

## Code Style

### Python

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

Example:
```python
def analyze_code(source_code: str) -> Dict[int, str]:
    """
    Analyze code and map line numbers to event types.
    
    Args:
        source_code: The source code to analyze
        
    Returns:
        Dictionary mapping line numbers to event type strings
    """
    # Implementation
```

### TypeScript/React

- Use TypeScript for all components
- Define interfaces for props
- Use functional components with hooks
- Follow React best practices

Example:
```typescript
interface MyComponentProps {
    data: any[];
    onUpdate: (value: number) => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ data, onUpdate }) => {
    // Implementation
};
```

## Commit Messages

Use clear, descriptive commit messages:

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, etc.)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

Examples:
```
feat: add tree visualizer component
fix: handle empty arrays in ArrayVisualizer
docs: update README with new examples
test: add tests for binary search tracing
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** (if exists)
5. **Create a pull request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues
   - Screenshots (if UI changes)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test this?

## Screenshots (if applicable)

## Related Issues
Fixes #123
```

## Code Review Process

- PRs require at least one approval
- Address review comments
- Keep discussions respectful and constructive
- Be open to feedback

## Areas for Contribution

Looking for ideas? Here are some areas that need work:

### High Priority
- [ ] Tree/Graph visualizers
- [ ] Performance optimizations for large traces
- [ ] Better error handling and user feedback
- [ ] More comprehensive tests

### Medium Priority
- [ ] Additional algorithm examples
- [ ] Custom themes/styling
- [ ] Export to video/GIF
- [ ] Comparison mode (diff two executions)

### Low Priority
- [ ] VS Code extension
- [ ] Jupyter notebook integration
- [ ] Remote collaboration features
- [ ] Cloud storage for visualizations

## Questions?

- Open an issue with the `question` label
- Check existing issues and documentation first
- Be specific and provide context

## License

By contributing to Vipey, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make Vipey better for everyone. We appreciate your time and effort! 🎉
