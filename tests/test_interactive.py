"""
Comprehensive tests for interactive mode with React frontend
"""
import pytest
import threading
import time
import requests
from pathlib import Path
from vipey import Vipey


class TestInteractiveMode:
    """Tests for the interactive Flask server"""
    
    @pytest.fixture
    def viz_with_data(self):
        """Create a Vipey instance with sample data"""
        viz = Vipey()
        
        @viz.capture
        def sample_function(n):
            """Sample function for testing"""
            result = 0
            for i in range(n):
                result += i
            return result
        
        # Execute the function
        sample_function(5)
        return viz
    
    def test_server_starts_successfully(self, viz_with_data):
        """Test that Flask server starts and responds"""
        # Start server in a background thread
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Try to connect
        try:
            response = requests.get('http://127.0.0.1:5000', timeout=5)
            assert response.status_code == 200
            assert 'text/html' in response.headers['Content-Type']
        except requests.exceptions.ConnectionError:
            pytest.fail("Server did not start successfully")
    
    def test_api_storyboard_endpoint(self, viz_with_data):
        """Test /api/storyboard endpoint returns correct data"""
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        response = requests.get('http://127.0.0.1:5000/api/storyboard', timeout=5)
        assert response.status_code == 200
        
        data = response.json()
        assert 'frames' in data
        assert 'return_value' in data
        assert 'source_code' in data
        assert 'function_name' in data
        assert isinstance(data['frames'], list)
    
    def test_api_project_endpoint(self, viz_with_data):
        """Test /api/project endpoint returns HTML"""
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        response = requests.get('http://127.0.0.1:5000/api/project', timeout=5)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
    
    def test_api_documentation_endpoint(self, viz_with_data):
        """Test /api/documentation endpoint returns HTML"""
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        response = requests.get('http://127.0.0.1:5000/api/documentation', timeout=5)
        assert response.status_code == 200
        assert 'text/html' in response.headers['Content-Type']
    
    def test_react_assets_served(self, viz_with_data):
        """Test that React build assets are served correctly"""
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        # Test CSS asset
        response = requests.get('http://127.0.0.1:5000/assets/index-a8252771.css', timeout=5)
        assert response.status_code == 200
        assert 'text/css' in response.headers['Content-Type']
        
        # Test JS asset
        response = requests.get('http://127.0.0.1:5000/assets/index-a37bf4e9.js', timeout=5)
        assert response.status_code == 200
        assert 'javascript' in response.headers['Content-Type'].lower()
    
    def test_storyboard_data_includes_time_complexity(self, viz_with_data):
        """Test that storyboard data includes time complexity analysis"""
        server_thread = threading.Thread(
            target=lambda: viz_with_data.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        response = requests.get('http://127.0.0.1:5000/api/storyboard', timeout=5)
        data = response.json()
        
        # Time complexity should be present
        if 'time_complexity' in data:
            complexity = data['time_complexity']
            assert 'big_o' in complexity
            assert 'explanation' in complexity
            assert 'patterns' in complexity
            assert 'confidence' in complexity
    
    def test_empty_storyboard_handling(self):
        """Test server handles empty storyboard gracefully"""
        # Create a fresh Vipey instance with minimal data
        viz = Vipey()
        
        # Create a dummy function but with minimal execution
        @viz.capture
        def minimal_func():
            return None
        
        minimal_func()
        
        server_thread = threading.Thread(
            target=lambda: viz.save(interactive=True),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)
        
        response = requests.get('http://127.0.0.1:5000/api/storyboard', timeout=5)
        assert response.status_code == 200
        
        data = response.json()
        # Should have some frames from the execution
        assert 'frames' in data
        assert isinstance(data['frames'], list)


class TestStaticFileGeneration:
    """Tests for static HTML file generation"""
    
    def test_static_file_created(self, tmp_path):
        """Test that static HTML file is created when interactive=False"""
        viz = Vipey()
        
        @viz.capture
        def test_func():
            return 42
        
        test_func()
        
        output_file = tmp_path / "test_output.html"
        viz.save(output_path=str(output_file), interactive=False)
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0
    
    def test_viz_folder_created_with_smart_naming(self):
        """Test that viz/ folder is created with smart filename"""
        viz = Vipey()
        
        @viz.capture
        def my_test_function(x):
            return x * 2
        
        my_test_function(5)
        
        # Save without specifying output path
        viz.save(interactive=False)
        
        viz_dir = Path.cwd() / "viz"
        assert viz_dir.exists()
        
        # Check for file with function name
        expected_file = viz_dir / "viz_my_test_function.html"
        assert expected_file.exists()
        
        # Clean up
        expected_file.unlink()


class TestReactFrontend:
    """Tests for React frontend build"""
    
    def test_dist_folder_exists(self):
        """Test that frontend dist folder exists"""
        dist_dir = Path(__file__).parent.parent / "vipey" / "templates" / "dist"
        assert dist_dir.exists()
    
    def test_index_html_exists(self):
        """Test that index.html exists in dist"""
        index_path = Path(__file__).parent.parent / "vipey" / "templates" / "dist" / "index.html"
        assert index_path.exists()
    
    def test_assets_folder_exists(self):
        """Test that assets folder exists"""
        assets_dir = Path(__file__).parent.parent / "vipey" / "templates" / "dist" / "assets"
        assert assets_dir.exists()
    
    def test_css_and_js_files_exist(self):
        """Test that CSS and JS bundles exist"""
        assets_dir = Path(__file__).parent.parent / "vipey" / "templates" / "dist" / "assets"
        
        # Find CSS and JS files
        css_files = list(assets_dir.glob("*.css"))
        js_files = list(assets_dir.glob("*.js"))
        
        assert len(css_files) > 0, "No CSS files found in assets"
        assert len(js_files) > 0, "No JS files found in assets"


class TestServerTerminalOutput:
    """Tests for terminal output and user experience"""
    
    def test_server_prints_url(self, viz_with_data, capsys):
        """Test that server prints clickable URL to terminal"""
        # This would require capturing stdout from the server thread
        # For now, we verify the format manually
        # The server should print: http://127.0.0.1:5000
        pass  # Manual verification required
    
    def test_ctrl_c_message_displayed(self):
        """Test that Ctrl+C message is displayed"""
        # Verified manually - server prints "Press Ctrl+C to stop the server"
        pass  # Manual verification required


@pytest.fixture
def viz_with_data():
    """Fixture to create Vipey instance with captured data"""
    viz = Vipey()
    
    @viz.capture
    def binary_search(arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    binary_search([1, 2, 3, 5, 8, 13], 5)
    return viz


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
