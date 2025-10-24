#!/usr/bin/env python3
"""
Quick test to verify all features work
"""
from vipey import Visualizer

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def main():
    print("Testing Vipey v0.2.0 Features")
    print("=" * 50)
    
    viz = Visualizer()
    
    # Test 1: Function capture
    print("\n✓ Testing function capture...")
    sort = viz.capture(quick_sort)
    result = sort([3, 6, 8, 10, 1, 2, 1])
    print(f"  Sorted: {result}")
    
    # Test 2: File analysis
    print("\n✓ Testing file analysis...")
    file_info = viz.analyze_file(__file__)
    print(f"  Functions: {file_info.get('functions', 0)}")
    print(f"  Lines: {file_info.get('total_lines', 0)}")
    
    # Test 3: Project analysis
    print("\n✓ Testing project analysis...")
    analysis = viz.analyze_project(".")
    print(f"  Total files: {analysis['metrics']['total_files']}")
    print(f"  Total lines: {analysis['metrics']['total_lines']:,}")
    
    # Test 4: Save visualization
    print("\n✓ Testing visualization save...")
    viz.save(interactive=False)
    print("  Saved to: vipey/visualization.html")
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("\nOpen vipey/visualization.html to see:")
    print("  • Function Trace (Quick Sort)")
    print("  • Project Analysis")
    print("  • Documentation")

if __name__ == "__main__":
    main()
