#!/usr/bin/env python3
"""
Example: Fibonacci sequence visualization
"""
from vipey import Visualizer

def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        next_fib = fib[i-1] + fib[i-2]
        fib.append(next_fib)
    
    return fib

def main():
    viz = Visualizer()
    
    # Capture the fibonacci execution
    captured_fib = viz.capture(fibonacci)
    
    # Generate first 10 Fibonacci numbers
    n = 10
    print(f"Generating first {n} Fibonacci numbers...")
    result = captured_fib(n)
    print(f"Result: {result}")
    
    # Save the visualization
    viz.save("fibonacci_visualization.html")
    print("\nVisualization saved to: fibonacci_visualization.html")

if __name__ == "__main__":
    main()
