#!/usr/bin/env python3
"""
Example: Binary search visualization
"""
from vipey import Visualizer

def binary_search(arr, target):
    """Binary search algorithm."""
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def main():
    viz = Visualizer()
    
    # Capture the binary search execution
    captured_search = viz.capture(binary_search)
    
    # Test data
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11
    
    print(f"Searching for {target} in {sorted_array}")
    result = captured_search(sorted_array, target)
    print(f"Found at index: {result}")
    
    # Save the visualization
    viz.save("binary_search_visualization.html")
    print("\nVisualization saved to: binary_search_visualization.html")

if __name__ == "__main__":
    main()
