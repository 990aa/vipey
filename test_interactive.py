"""Test interactive mode with the new UI"""
from vipey import Vipey

viz = Vipey()

@viz.capture
def binary_search(arr, target):
    """Binary search algorithm - O(log n)"""
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

# Test
result = binary_search([1, 2, 3, 5, 8, 13, 21, 34], 13)
print(f"Found at index: {result}")

# Start interactive mode
print("\n🎯 Starting interactive mode...")
print("The server should start and display a clickable URL")
print("Press Ctrl+C in the terminal to stop the server\n")

viz.save(interactive=True)
