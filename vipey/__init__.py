import inspect
import os
from pathlib import Path
from .tracer import Tracer
from .ast_parser import analyze_code
from .renderer import save_visualization, save_multi_tab_visualization
from .analyzer import ProjectAnalyzer

class Vipey:
    def __init__(self):
        self.storyboard = None
        self.custom_serializers = {}
        self.project_analysis = None
        self.file_analysis = None
        self.captured_function_name = None

    def capture(self, func):
        """Decorator to capture the execution of a function."""
        def wrapper(*args, **kwargs):
            # Store function name for filename generation
            self.captured_function_name = func.__name__
            
            source_code = inspect.getsource(func)
            ast_map = analyze_code(source_code)
            
            # Analyze time complexity
            from .analyzer import ProjectAnalyzer
            analyzer = ProjectAnalyzer(os.getcwd())
            complexity_info = analyzer.analyze_time_complexity(source_code)
            
            tracer = Tracer(ast_map=ast_map, source_code=source_code, custom_serializers=self.custom_serializers)
            self.storyboard, result = tracer.trace_function(func, *args, **kwargs)
            
            # Add time complexity to storyboard
            self.storyboard['time_complexity'] = complexity_info
            self.storyboard['function_name'] = func.__name__
            
            return result
        return wrapper

    def analyze_file(self, file_path: str) -> dict:
        """
        Analyze a single Python file for complexity and metrics.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary containing file analysis results
        """
        analyzer = ProjectAnalyzer(os.path.dirname(file_path))
        self.file_analysis = analyzer.analyze_file(Path(file_path))
        return self.file_analysis
    
    def analyze_project(self, project_path: str = None) -> dict:
        """
        Analyze an entire project for comprehensive metrics and insights.
        
        Args:
            project_path: Path to the project directory. If None, uses current directory.
            
        Returns:
            Dictionary containing comprehensive project analysis
        """
        if project_path is None:
            project_path = os.getcwd()
        
        analyzer = ProjectAnalyzer(project_path)
        self.project_analysis = analyzer.analyze_project()
        return self.project_analysis
    
    def save(self, output_path: str = "visualization.html", interactive: bool = False):
        """
        Save the visualization as an HTML file.
        
        Args:
            output_path: Path where the HTML file will be saved
            interactive: If True, opens a local server. If False, creates static HTML.
        """
        if not self.storyboard and not self.project_analysis:
            raise Exception("Nothing to save. Run a captured function or analyze a project first.")
        
        # Determine output filename and directory based on interactive mode
        if not interactive and output_path == "visualization.html":
            # Create viz/ folder in the current directory
            output_dir = Path.cwd() / "viz"
            output_dir.mkdir(exist_ok=True)
            
            # Generate filename based on what was analyzed
            if self.captured_function_name:
                # Use function name if a function was captured
                filename = f"viz_{self.captured_function_name}.html"
            elif self.file_analysis:
                # Use file name if a file was analyzed
                file_path = self.file_analysis.get('file', 'unknown')
                filename = f"viz_{Path(file_path).stem}.html"
            elif self.project_analysis:
                # Use project name if project was analyzed
                project_path = Path.cwd()
                filename = f"viz_{project_path.name}.html"
            else:
                filename = "viz_visualization.html"
            
            output_path = str(output_dir / filename)
        
        # Use multi-tab visualization if we have project analysis
        if self.project_analysis or self.file_analysis:
            save_multi_tab_visualization(
                storyboard_data=self.storyboard,
                project_data=self.project_analysis,
                file_data=self.file_analysis,
                output_path=output_path,
                interactive=interactive
            )
        else:
            # Even for simple function traces, use multi-tab visualization
            save_multi_tab_visualization(
                storyboard_data=self.storyboard,
                project_data=None,
                file_data=None,
                output_path=output_path,
                interactive=interactive
            )

    def register_serializer(self, data_type, serializer_func):
        """Register a custom serializer for a data type."""
        self.custom_serializers[data_type] = serializer_func


# Backward compatibility alias
Visualizer = Vipey
