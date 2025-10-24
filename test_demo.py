# test_demo.py - Simple test to verify all features work
from vipey import Vipey

# Test 1: Function tracing with time complexity
print("=" * 60)
print("Test 1: Binary Search with Time Complexity Analysis")
print("=" * 60)

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

# Execute the function
result = binary_search([1, 3, 5, 7, 9, 11, 13, 15], 7)
print(f"Found at index: {result}")

# Save visualization
viz.save(interactive=False)
print("Visualization saved to viz/ folder!")
print()

# Test 2: Nested loops with O(n^2) complexity
print("=" * 60)
print("Test 2: Bubble Sort with O(n^2) Complexity")
print("=" * 60)

viz2 = Vipey()

@viz2.capture
def bubble_sort(arr):
    """Bubble sort algorithm - O(n^2)"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

result2 = bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(f"Sorted array: {result2}")

viz2.save(interactive=False)
print("Visualization saved to viz/ folder!")
print()

# Test 3: Linear search with O(n) complexity
print("=" * 60)
print("Test 3: Linear Search with O(n) Complexity")
print("=" * 60)

viz3 = Vipey()

@viz3.capture
def linear_search(arr, target):
    """Linear search algorithm - O(n)"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

result3 = linear_search([10, 20, 30, 40, 50], 30)
print(f"Found at index: {result3}")

viz3.save(interactive=False)
print("Visualization saved to viz/ folder!")
print()

print("=" * 60)
print("✅ All tests completed successfully!")
print("=" * 60)
print("Check the viz/ folder for HTML visualizations.")
print("Each file shows the time complexity analysis!")
