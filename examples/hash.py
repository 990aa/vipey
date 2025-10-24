"""
Problem Statement:
Design and implement a data structure for a Least Recently Used (LRU) Cache. 
It must support two operations, both in $O(1)$ average time complexity:
get(key):If the key exists in the cache, return its value and mark it as the most recently used item.If the key does not exist, return -1.
put(key, value):If the key already exists, update its value and mark it as the most recently used item.If the key does not exist, insert the (key, value) pair.
If the cache is full (i.e., size == capacity), evict the least recently used item before inserting the new item.
"""

import collections

# We need a DLinkedNode to store key/value
# This allows us to delete from the hash map when evicting from the list
class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # The cache is our Hash Map
        self.cache = {} # Stores key -> DLinkedNode
        
        # We use dummy head and tail nodes to avoid edge cases
        # for empty list or single-item list
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: DLinkedNode):
        """Remove a node from its position in the DLL"""
        prev = node.prev
        new = node.next
        prev.next = new
        new.prev = prev

    def _add_to_head(self, node: DLinkedNode):
        """Add a node right after the dummy head (most recent)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: DLinkedNode):
        """Move an existing node to the head"""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> DLinkedNode:
        """Pop the least recently used item (just before the dummy tail)"""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        # Use the hash map for O(1) lookup
        node = self.cache.get(key, None)
        
        if not node:
            return -1
        
        # Move the accessed node to the head of the list
        # to mark it as most recently used
        self._move_to_head(node)
        
        return node.val

    def put(self, key: int, value: int) -> None:
        # Check if key is already in the hash map
        node = self.cache.get(key)
        
        if not node:
            # Key is new. Create a new node.
            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # Check if we exceeded capacity
            if len(self.cache) > self.capacity:
                # Evict the least recently used item
                tail = self._pop_tail()
                # Remove it from the hash map as well
                del self.cache[tail.key]
        else:
            # Key exists. Update value and move to head.
            node.val = value
            self._move_to_head(node)

# --- Example Usage ---
print("LRU Cache with capacity 2")
cache = LRUCache(2)

cache.put(1, 1)    # cache is {1: 1}
cache.put(2, 2)    # cache is {1: 1, 2: 2}
print(f"Get 1: {cache.get(1)}") # returns 1, cache is {2: 2, 1: 1} (1 is now most recent)

cache.put(3, 3)    # LRU key 2 was evicted. cache is {1: 1, 3: 3}
print(f"Get 2: {cache.get(2)}") # returns -1 (not found)

cache.put(4, 4)    # LRU key 1 was evicted. cache is {3: 3, 4: 4}
print(f"Get 1: {cache.get(1)}") # returns -1 (not found)
print(f"Get 3: {cache.get(3)}") # returns 3. cache is {4: 4, 3: 3}
print(f"Get 4: {cache.get(4)}") # returns 4. cache is {3: 3, 4: 4}