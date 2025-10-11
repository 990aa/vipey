import inspect
from .tracer import Tracer
from .ast_parser import analyze_code
from .renderer import save_visualization

class Visualizer:
    def __init__(self):
        self.storyboard = None
        self.custom_serializers = {}

    def capture(self, func):
        """Decorator to capture the execution of a function."""
        def wrapper(*args, **kwargs):
            source_code = inspect.getsource(func)
            ast_map = analyze_code(source_code)
            tracer = Tracer(ast_map=ast_map, source_code=source_code)
            self.storyboard = tracer.trace_function(func, *args, **kwargs)
            return self.storyboard['return_value']
        return wrapper

    def save(self, output_path: str = "visualization.html"):
        """Save the captured execution as an HTML visualization."""
        if not self.storyboard:
            raise Exception("Nothing to save. Run a captured function first.")
        save_visualization(self.storyboard, output_path)

    def register_serializer(self, data_type, serializer_func):
        """Register a custom serializer for a data type."""
        self.custom_serializers[data_type] = serializer_func
