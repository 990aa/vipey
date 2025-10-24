#!/usr/bin/env python3
"""
Demo script for vipey - Comprehensive demonstration of all features
"""
from vipey import Visualizer
import sys

def bubble_sort(arr):
    """Bubble sort algorithm to demonstrate vipey visualization."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def main():
    print("=" * 60)
    print("Vipey v0.2.0 - Comprehensive Demo")
    print("=" * 60)
    print()
    
    # Create a visualizer instance
    viz = Visualizer()
    
    # Demo 1: Function execution tracing
    print("1. Capturing bubble sort execution...")
    captured_bubble_sort = viz.capture(bubble_sort)
    
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Original array: {test_array}")
    
    result = captured_bubble_sort(test_array.copy())
    print(f"   Sorted array: {result}")
    print("   ✓ Function execution captured")
    print()
    
    # Demo 2: Project analysis
    print("2. Analyzing current project...")
    try:
        analysis = viz.analyze_project(".")
        metrics = analysis['metrics']
        print(f"   Total files: {metrics['total_files']}")
        print(f"   Total lines: {metrics['total_lines']:,}")
        print(f"   Code lines: {metrics['code_lines']:,}")
        print(f"   Functions: {metrics.get('total_functions', 0)}")
        print(f"   Classes: {metrics.get('total_classes', 0)}")
        print("   ✓ Project analysis complete")
    except Exception as e:
        print(f"   ⚠ Project analysis failed: {e}")
    print()
    
    # Demo 3: Save visualization
    print("3. Saving multi-tab visualization...")
    
    # Check if user wants interactive mode
    interactive = '--interactive' in sys.argv
    
    if interactive:
        print("   Starting interactive dashboard...")
        print("   Server will open at http://127.0.0.1:5000")
        viz.save(interactive=True)
    else:
        print("   Creating static HTML file...")
        viz.save(interactive=False)
        print("   ✓ Visualization saved to: vipey/visualization.html")
        print()
        print("   The visualization includes:")
        print("   • Function Trace tab - Bubble sort execution")
        print("   • Project Analysis tab - Comprehensive metrics")
        print("   • Documentation tab - Full API reference")
        print()
        print("   Open vipey/visualization.html in your browser to view!")
    
    print()
    print("=" * 60)
    print("Demo complete!")
    print()
    print("Try these commands:")
    print("  python demo.py              # Static visualization")
    print("  python demo.py --interactive # Interactive dashboard")
    print("=" * 60)

if __name__ == "__main__":
    main()
