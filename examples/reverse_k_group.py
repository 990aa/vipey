#!/usr/bin/env python3
"""
Example: Reverse Nodes in k-Group
Demonstrates vipey visualization of linked list algorithm
"""
from vipey import Vipey
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        
        # If k is 1, no reversal is needed. Return the original list.
        if k == 1 or not head:
            return head

        # Create a dummy node to simplify edge cases, especially
        # for re-linking the head of the first group.
        dummy = ListNode(0, head)
        
        # 'prev_group_end' will point to the last node of the *previous*
        # reversed group. It starts at the dummy node.
        prev_group_end = dummy

        while True:
            # 1. Find the k-th node of the current group
            # 'kth_node' will be the last node *in* the current group.
            kth_node = self.find_kth_node(prev_group_end, k)
            
            # If kth_node is None, it means the remaining list has
            # fewer than k nodes. We stop and return.
            if not kth_node:
                break
                
            # 2. Store important pointers
            # This is the first node of the current group (will be the tail after reversal)
            group_head = prev_group_end.next
            # This is the first node of the *next* group
            next_group_start = kth_node.next
            
            # 3. Reverse the k-group
            # We reverse the sublist from 'group_head' to 'kth_node'.
            # We will make the new tail (group_head) point to 'next_group_start'.
            prev = next_group_start
            curr = group_head
            
            while curr != next_group_start:
                temp = curr.next
                curr.next = prev
                prev = curr
                curr = temp
                
            # 4. Connect the previous group to the new (reversed) group
            # 'prev' (which is the same as 'kth_node' at this point)
            # is the new head of the just-reversed group.
            
            # Save the old head of this group, which is now its tail.
            # This will be the 'prev_group_end' for the *next* iteration.
            new_prev_group_end = prev_group_end.next 
            
            # Link the end of the last group to the new head of this group
            prev_group_end.next = kth_node
            
            # 5. Move to the next group
            # The 'prev_group_end' for the next loop is the tail of
            # the group we just reversed.
            prev_group_end = new_prev_group_end

        # The dummy node's 'next' pointer always points to the
        # true head of the modified list.
        return dummy.next

    def find_kth_node(self, start_node: ListNode, k: int) -> Optional[ListNode]:
        """
        Helper function to find the k-th node *after* the start_node.
        'start_node' is the node *before* the group begins.
        """
        curr = start_node
        for _ in range(k):
            if not curr.next:
                # Not enough nodes
                return None
            curr = curr.next
        return curr

# Helper function to create a linked list from a list
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to print a linked list
def print_linked_list(head):
    vals = []
    current = head
    while current:
        vals.append(str(current.val))
        current = current.next
    return " -> ".join(vals)

# Custom serializer for ListNode
def listnode_serializer(node):
    """Serialize a ListNode for vipey visualization"""
    if node is None:
        return None
    
    vals = []
    current = node
    # Prevent infinite loops
    visited = set()
    while current:
        if id(current) in visited:
            vals.append("...")
            break
        visited.add(id(current))
        vals.append(current.val)
        current = current.next
        if len(vals) > 20:  # Limit to prevent huge outputs
            vals.append("...")
            break
    
    return {
        "type": "LinkedList",
        "values": vals,
        "display": " -> ".join(str(v) for v in vals)
    }


def main():
    print("=" * 60)
    print("Vipey - Reverse Nodes in k-Group Example")
    print("=" * 60)
    print()
    
    # Create vipey instance
    viz = Vipey()
    
    # Register custom serializer for ListNode
    viz.register_serializer(ListNode, listnode_serializer)
    
    # --- Example 1 ---
    print("Example 1: k=2")
    list1 = create_linked_list([1, 2, 3, 4, 5])
    k1 = 2
    print(f"Original list: {print_linked_list(list1)}")
    
    # Capture the execution
    sol = Solution()
    captured_reverse = viz.capture(sol.reverseKGroup)
    
    result1 = captured_reverse(list1, k1)
    print(f"Reversed list: {print_linked_list(result1)}")
    print("   Expected: 2 -> 1 -> 4 -> 3 -> 5")
    print()
    
    print("-" * 60)
    
    # --- Example 2 ---
    print()
    print("Example 2: k=3")
    list2 = create_linked_list([1, 2, 3, 4, 5])
    k2 = 3
    print(f"Original list: {print_linked_list(list2)}")
    
    sol2 = Solution()
    captured_reverse2 = viz.capture(sol2.reverseKGroup)
    
    result2 = captured_reverse2(list2, k2)
    print(f"Reversed list: {print_linked_list(result2)}")
    print("   Expected: 3 -> 2 -> 1 -> 4 -> 5")
    print()
    
    # Save visualization in static mode to test filename generation
    print("=" * 60)
    print("Saving visualization in STATIC mode...")
    print("=" * 60)
    
    viz.save(interactive=False)
    print(f"Visualization saved! Check the viz/ folder.")


if __name__ == "__main__":
    main()
