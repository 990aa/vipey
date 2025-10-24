"""
Sliding Window Maximum

You are given an array of integers nums and a positive integer $k$, representing the size of a sliding window.A window of size $k$ moves from the very left of the array to the very right. You can only see the $k$ numbers in the window at each position. The window moves one position to the right at a time.Your task is to return an array containing the maximum value from each window.

Example:
Input: 
nums = [1, 3, -1, -3, 5, 3, 6, 7], $k = 3$
Output: [3, 3, 5, 5, 6, 7]

Explanation:
Window Position                Max
[1, 3, -1] -3, 5, 3, 6, 7       3
1, [3, -1, -3] 5, 3, 6, 7       3
1, 3, [-1, -3, 5] 3, 6, 7       5
1, 3, -1, [-3, 5, 3] 6, 7       5
1, 3, -1, -3, [5, 3, 6] 7       6
1, 3, -1, -3, 5, [3, 6, 7]      7
"""

import collections
from vipey import Vipey

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        
        # 'output' will store the max of each window
        output = []
        
        # 'q' is a deque (double-ended queue) that will
        # store *indices* of the numbers in nums.
        # It will be maintained in monotonically decreasing
        # order *by the values* they point to.
        q = collections.deque() # q stores indices

        # We'll use 'l' (left) and 'r' (right) as the
        # window boundaries, but the main loop iterates
        # with 'r' as the index.
        
        for r in range(len(nums)):
            # --- STACK-LIKE BEHAVIOR (at the back) ---
            # Maintain the decreasing order.
            # Before adding the new index 'r', remove all indices
            # from the *back* of the deque that point to values
            # smaller than or equal to the current value (nums[r]).
            # This ensures the largest element is always at the front.
            while q and nums[q[-1]] < nums[r]:
                q.pop() # Pop from the right (like a stack)
                
            # Add the current index to the back
            q.append(r)
            
            # --- QUEUE-LIKE BEHAVIOR (at the front) ---
            # Remove the leftmost index if it's now
            # outside the window [r - k + 1, r].
            # The left boundary is at index (r - k + 1).
            # If the index at q[0] is less than that,
            # it's out of the window.
            if q[0] < r - k + 1:
                q.popleft() # Pop from the left (like a queue)

            # --- RECORDING THE MAX ---
            # Once the window is full (i.e., we have at least k elements),
            # the index at the *front* of the deque (q[0])
            # is the index of the maximum element in the current window.
            if r >= k - 1:
                output.append(nums[q[0]])
                
        return output

# --- Example Usage ---
if __name__ == "__main__":
    viz = Vipey()
    sol = Solution()

    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"Array: {nums}, k: {k}")
    
    captured_func = viz.capture(sol.maxSlidingWindow)
    result = captured_func(nums, k)
    print(f"Result: {result}")  # Output: [3, 3, 5, 5, 6, 7]

    print("-" * 20)

    nums2 = [1]
    k2 = 1
    print(f"Array: {nums2}, k: {k2}")
    
    sol2 = Solution()
    captured_func2 = viz.capture(sol2.maxSlidingWindow)
    result2 = captured_func2(nums2, k2)
    print(f"Result: {result2}") # Output: [1]

    print("-" * 20)

    nums3 = [9, 10, 9, -7, -4, -8, 2, -6]
    k3 = 5
    print(f"Array: {nums3}, k: {k3}")
    
    sol3 = Solution()
    captured_func3 = viz.capture(sol3.maxSlidingWindow)
    result3 = captured_func3(nums3, k3)
    print(f"Result: {result3}") # Output: [10, 10, 9, 2, 2]
    
    # Save visualization
    print("\n" + "=" * 60)
    print("Generating visualization...")
    print("=" * 60)
    viz.save(interactive=True)