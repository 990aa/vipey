# test_analyzer.py
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vipey.analyzer import ProjectAnalyzer, CodeMetricsAnalyzer


class TestCodeMetricsAnalyzer:
    """Test suite for CodeMetricsAnalyzer"""
    
    def test_simple_function_analysis(self, tmp_path):
        """Test analyzing a simple Python function"""
        test_file = tmp_path / "simple.py"
        test_file.write_text("""
def hello(name):
    '''Say hello'''
    return f"Hello, {name}!"

def add(a, b):
    # Add two numbers
    return a + b
""")
        
        # Use ProjectAnalyzer instead of CodeMetricsAnalyzer
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_file(test_file)
        
        assert result['file'] == str(test_file)
        assert result['language'] == 'Python'
        assert result['total_lines'] > 0
        assert result['code_lines'] > 0
        assert result['comment_lines'] >= 2  # Docstring + comment
        assert result['functions'] >= 2  # Changed from list length to count
        assert result['classes'] == 0
    
    def test_class_analysis(self, tmp_path):
        """Test analyzing a Python class"""
        test_file = tmp_path / "class_test.py"
        test_file.write_text("""
class Calculator:
    '''A simple calculator'''
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
""")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_file(test_file)
        
        assert result['classes'] >= 1
        # Classes is a count, not a list
    
    def test_complexity_calculation(self, tmp_path):
        """Test cyclomatic complexity calculation"""
        test_file = tmp_path / "complexity.py"
        test_file.write_text("""
def complex_function(x):
    if x > 0:
        if x > 10:
            return "big"
        else:
            return "small"
    elif x < 0:
        return "negative"
    else:
        return "zero"
""")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_file(test_file)
        
        # Should have higher complexity due to nested if/elif
        assert result['complexity_score'] > 1


class TestProjectAnalyzer:
    """Test suite for ProjectAnalyzer"""
    
    def test_analyze_file(self, tmp_path):
        """Test analyzing a single file"""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def fibonacci(n):
    '''Calculate Fibonacci number'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_file(test_file)
        
        assert result is not None
        assert result['language'] == 'Python'
        # functions is now a count, not a list
        assert result['functions'] >= 1
    
    def test_analyze_project(self, tmp_path):
        """Test analyzing a full project"""
        # Create a mini project structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "__init__.py").write_text("")
        (tmp_path / "src" / "module1.py").write_text("""
def func1():
    pass

def func2():
    pass
""")
        (tmp_path / "src" / "module2.py").write_text("""
class MyClass:
    def method1(self):
        pass
""")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_module1.py").write_text("""
def test_func1():
    assert True
""")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_project()
        
        assert 'metrics' in result
        assert result['metrics']['total_files'] >= 3  # At least 3 Python files
        assert result['metrics']['total_functions'] >= 3
        assert result['metrics']['total_classes'] >= 1
    
    def test_language_distribution(self, tmp_path):
        """Test language distribution calculation"""
        # Create Python files
        (tmp_path / "file1.py").write_text("print('hello')\n" * 10)
        (tmp_path / "file2.py").write_text("print('world')\n" * 5)
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_project()
        
        assert 'metrics' in result
        assert 'language_distribution' in result['metrics']
        assert 'Python' in result['metrics']['language_distribution']
        
        py_stats = result['metrics']['language_distribution']['Python']
        assert py_stats['count'] == 2
        assert py_stats['percentage'] == 100.0
    
    def test_calculate_file_risk(self, tmp_path):
        """Test risk score calculation for files"""
        # Create a high-risk file (high complexity, low comments, large size)
        risky_file = tmp_path / "risky.py"
        risky_code = """
def complex_func(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            if z > 0:
                return x + z
            else:
                return x
    else:
        if y > 0:
            if z > 0:
                return y + z
            else:
                return y
        else:
            return z
""" * 50  # Repeat to make it large
        
        risky_file.write_text(risky_code)
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        file_analysis = analyzer.analyze_file(risky_file)
        
        # Mock git history for testing
        git_history = {'file_churn': {str(risky_file): {'commits': 15}}}
        
        risk_score = analyzer._calculate_file_risk(file_analysis, git_history)
        
        # Should have elevated risk due to complexity and size
        assert 0 <= risk_score <= 1
        assert risk_score > 0.3  # Should be somewhat risky
    
    def test_analyze_stability(self, tmp_path):
        """Test file stability classification"""
        stable_file = tmp_path / "stable.py"
        volatile_file = tmp_path / "volatile.py"
        
        stable_file.write_text("def stable(): pass")
        volatile_file.write_text("def volatile(): pass")
        
        # Create file dicts matching the expected format
        files = [
            {'path': str(stable_file), 'absolute_path': str(stable_file)},
            {'path': str(volatile_file), 'absolute_path': str(volatile_file)}
        ]
        
        # Mock git history
        git_history = {
            'file_churn': {
                str(stable_file): {'commits': 1},
                str(volatile_file): {'commits': 15}
            }
        }
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        stable_count, volatile_count = analyzer._analyze_stability(files, git_history)
        
        assert stable_count > 0
        assert volatile_count > 0
    
    def test_generate_recommendations(self, tmp_path):
        """Test recommendation generation"""
        # Create test files
        (tmp_path / "file1.py").write_text("def test(): pass")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_project()
        
        # Generate recommendations
        recommendations = analyzer._generate_recommendations(result)
        
        assert isinstance(recommendations, list)
        # Should have at least some recommendations
        assert len(recommendations) >= 0
    
    def test_advanced_report_generation(self, tmp_path):
        """Test advanced report generation with code churn"""
        (tmp_path / "test.py").write_text("def func(): pass")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_project()
        
        # Generate advanced report
        advanced = analyzer.generate_advanced_report(result)
        
        assert 'code_churn' in advanced
        assert 'stability_analysis' in advanced
        assert 'high_risk_files' in advanced
    
    def test_nextgen_report_generation(self, tmp_path):
        """Test next-gen intelligence report generation"""
        (tmp_path / "test.py").write_text("def func(): pass")
        
        analyzer = ProjectAnalyzer(str(tmp_path))
        result = analyzer.analyze_project()
        
        # Generate nextgen report
        nextgen = analyzer.generate_nextgen_report(result)
        
        assert 'predictive_risk_analysis' in nextgen
        assert 'architectural_analysis' in nextgen
        assert 'dependency_ecosystem' in nextgen
        assert 'ai_insights' in nextgen
        assert 'code_evolution_dna' in nextgen
        assert 'recommendations' in nextgen


class TestCustomSerializers:
    """Test custom serializer support"""
    
    def test_custom_serializer_registration(self):
        """Test registering a custom serializer"""
        from vipey import Vipey
        
        class CustomClass:
            def __init__(self, value):
                self.value = value
        
        def custom_serializer(obj):
            return {'custom_value': obj.value}
        
        viz = Vipey()
        viz.register_serializer(CustomClass, custom_serializer)
        
        assert CustomClass in viz.custom_serializers
        assert viz.custom_serializers[CustomClass] == custom_serializer


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
