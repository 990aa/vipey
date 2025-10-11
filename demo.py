#!/usr/bin/env python3
"""
Demo script for vipey - Visualizes a bubble sort algorithm
"""
from vipey import Visualizer

def bubble_sort(arr):
    """Bubble sort algorithm to demonstrate vipey visualization."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def main():
    # Create a visualizer instance
    viz = Visualizer()
    
    # Capture the bubble sort execution
    captured_bubble_sort = viz.capture(bubble_sort)
    
    # Run the function with test data
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_array}")
    
    result = captured_bubble_sort(test_array.copy())
    print(f"Sorted array: {result}")
    
    # Save the visualization
    viz.save("bubble_sort_visualization.html")
    print("\nVisualization saved to: bubble_sort_visualization.html")
    print("Open this file in a web browser to see the interactive visualization!")

if __name__ == "__main__":
    main()
