# Placeholder for tracer tests
import sys
import os

# Add parent directory to path so we can import vipey
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vipey import Visualizer

def test_tracer_basic():
    """Test basic tracer functionality."""
    viz = Visualizer()
    
    def simple_function():
        x = 5
        y = 10
        z = x + y
        return z
    
    captured = viz.capture(simple_function)
    result = captured()
    
    assert result == 15
    assert viz.storyboard is not None
    assert 'frames' in viz.storyboard
    assert len(viz.storyboard['frames']) > 0

def test_tracer_with_array():
    """Test tracer with array operations."""
    viz = Visualizer()
    
    def array_sum(arr):
        total = 0
        for num in arr:
            total += num
        return total
    
    captured = viz.capture(array_sum)
    result = captured([1, 2, 3, 4, 5])
    
    assert result == 15
    assert viz.storyboard is not None

def test_visualizer_save():
    """Test that visualizer can save HTML output."""
    import tempfile
    
    viz = Visualizer()
    
    def simple_function():
        return 42
    
    captured = viz.capture(simple_function)
    captured()
    
    # Use tempfile for cross-platform compatibility
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        output_path = f.name
    
    try:
        viz.save(output_path)
        assert os.path.exists(output_path)
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)
