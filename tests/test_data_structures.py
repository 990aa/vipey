"""
Test suite for advanced data structure visualizations in Vipey.

Tests cover:
- Linked List detection and serialization
- Tree (BST/AVL) detection and serialization
- Graph detection and serialization
- Hash Map and LRU Cache serialization
- Integration with React Flow visualizers
"""

import pytest
from vipey import Vipey
from vipey.tracer import Tracer


# ============================================================================
# Linked List Tests
# ============================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def test_linked_list_detection():
    """Test that tracer detects and serializes linked lists."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create a linked list: 1 -> 2 -> 3
    head = ListNode(1, ListNode(2, ListNode(3)))
    
    serialized = tracer._serialize_value(head)
    
    assert serialized['type'] == 'LinkedList'
    assert serialized['values'] == [1, 2, 3]
    assert '1 -> 2 -> 3' in serialized['display']


def test_linked_list_circular_detection():
    """Test that circular linked lists are handled safely."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create a circular list: 1 -> 2 -> 3 -> 1
    head = ListNode(1)
    second = ListNode(2)
    third = ListNode(3)
    head.next = second
    second.next = third
    third.next = head  # Circular
    
    serialized = tracer._serialize_value(head)
    
    assert serialized['type'] == 'LinkedList'
    assert '...' in serialized['values']
    assert len(serialized['values']) <= 4  # Should detect cycle


def test_linked_list_empty():
    """Test that None/empty linked lists are handled."""
    viz = Vipey()
    tracer = viz.tracer
    
    serialized = tracer._serialize_value(None)
    assert serialized is None


def test_reverse_linked_list_integration():
    """Test visualization of a linked list reversal function."""
    viz = Vipey()
    
    def reverse_list(head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev
    
    # Create list: 1 -> 2 -> 3
    head = ListNode(1, ListNode(2, ListNode(3)))
    
    captured = viz.capture(reverse_list)
    result = captured(head)
    
    # Verify result
    vals = []
    current = result
    while current:
        vals.append(current.val)
        current = current.next
    assert vals == [3, 2, 1]
    
    # Verify storyboard was captured
    assert viz.tracer.storyboard is not None
    assert len(viz.tracer.storyboard) > 0


# ============================================================================
# Tree Tests
# ============================================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def test_tree_detection():
    """Test that tracer detects and serializes binary trees."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create a tree:
    #       1
    #      / \
    #     2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    
    serialized = tracer._serialize_value(root)
    
    assert serialized['type'] in ['Tree', 'BST', 'AVL']
    assert serialized['root']['value'] == 1
    assert serialized['root']['left']['value'] == 2
    assert serialized['root']['right']['value'] == 3


def test_avl_tree_with_height():
    """Test that AVL tree attributes are captured."""
    viz = Vipey()
    tracer = viz.tracer
    
    class AVLNode:
        def __init__(self, val=0, left=None, right=None, height=1):
            self.val = val
            self.left = left
            self.right = right
            self.height = height
    
    root = AVLNode(10, AVLNode(5, height=1), AVLNode(15, height=1), height=2)
    
    serialized = tracer._serialize_value(root)
    
    assert serialized['type'] == 'AVL'
    assert serialized['root']['height'] == 2
    assert serialized['root']['left']['height'] == 1


def test_tree_empty():
    """Test that empty trees are handled."""
    viz = Vipey()
    tracer = viz.tracer
    
    serialized = tracer._serialize_value(None)
    assert serialized is None


def test_tree_traversal_integration():
    """Test visualization of a tree traversal function."""
    viz = Vipey()
    
    def inorder_traversal(root: TreeNode) -> list:
        result = []
        
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.val)
                inorder(node.right)
        
        inorder(root)
        return result
    
    # Create tree
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    
    captured = viz.capture(inorder_traversal)
    result = captured(root)
    
    assert result == [2, 1, 3]
    assert len(viz.tracer.storyboard) > 0


# ============================================================================
# Graph Tests
# ============================================================================

def test_graph_adjacency_list_detection():
    """Test that tracer detects graph adjacency lists."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create adjacency list graph
    graph = {
        0: [1, 2],
        1: [2],
        2: [3],
        3: []
    }
    
    serialized = tracer._serialize_value(graph)
    
    assert serialized['type'] == 'Graph'
    assert set(serialized['nodes']) == {0, 1, 2, 3}
    assert serialized['directed'] is True
    assert len(serialized['edges']) == 4


def test_graph_string_nodes():
    """Test graphs with string node labels."""
    viz = Vipey()
    tracer = viz.tracer
    
    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': []
    }
    
    serialized = tracer._serialize_value(graph)
    
    assert serialized['type'] == 'Graph'
    assert set(serialized['nodes']) == {'A', 'B', 'C'}


def test_graph_traversal_integration():
    """Test visualization of a graph traversal (DFS)."""
    viz = Vipey()
    
    def dfs(graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                dfs(graph, neighbor, visited)
        
        return list(visited)
    
    graph = {
        0: [1, 2],
        1: [2],
        2: [3],
        3: []
    }
    
    captured = viz.capture(dfs)
    result = captured(graph, 0)
    
    assert set(result) == {0, 1, 2, 3}
    assert len(viz.tracer.storyboard) > 0


# ============================================================================
# Custom Serializer Tests
# ============================================================================

def test_custom_serializer_override():
    """Test that custom serializers override auto-detection."""
    viz = Vipey()
    
    def custom_list_serializer(node):
        return {
            'type': 'CustomLinkedList',
            'custom': True,
            'values': [node.val]
        }
    
    viz.register_serializer(ListNode, custom_list_serializer)
    
    head = ListNode(42)
    serialized = viz.tracer._serialize_value(head)
    
    assert serialized['type'] == 'CustomLinkedList'
    assert serialized['custom'] is True


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_visualization_pipeline():
    """Test complete pipeline from trace to storyboard."""
    viz = Vipey()
    
    def process_list(head: ListNode) -> int:
        count = 0
        current = head
        while current:
            count += 1
            current = current.next
        return count
    
    head = ListNode(1, ListNode(2, ListNode(3)))
    
    captured = viz.capture(process_list)
    result = captured(head)
    
    assert result == 3
    
    # Check storyboard structure
    assert len(viz.tracer.storyboard) > 0
    first_frame = viz.tracer.storyboard[0]
    assert 'line' in first_frame
    assert 'event_type' in first_frame
    assert 'locals' in first_frame


def test_complexity_analysis_with_tree():
    """Test complexity analysis works with tree data structures."""
    viz = Vipey()
    
    def tree_height(root: TreeNode) -> int:
        if root is None:
            return 0
        return 1 + max(tree_height(root.left), tree_height(root.right))
    
    root = TreeNode(1, TreeNode(2), TreeNode(3))
    
    captured = viz.capture(tree_height)
    result = captured(root)
    
    assert result == 2


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_unserializable_object_handling():
    """Test that unserializable objects don't crash the tracer."""
    viz = Vipey()
    tracer = viz.tracer
    
    class ComplexObject:
        def __init__(self):
            self.data = "test"
        
        def __repr__(self):
            raise Exception("Cannot represent")
    
    obj = ComplexObject()
    serialized = tracer._serialize_value(obj)
    
    # Should return string representation
    assert isinstance(serialized, str)


def test_deeply_nested_structure():
    """Test that deeply nested structures are handled safely."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create a deep tree
    root = TreeNode(0)
    current = root
    for i in range(1, 50):
        current.left = TreeNode(i)
        current = current.left
    
    serialized = tracer._serialize_value(root)
    
    assert serialized['type'] in ['Tree', 'AVL', 'BST']
    # Should not crash


def test_large_linked_list_truncation():
    """Test that very large linked lists are truncated."""
    viz = Vipey()
    tracer = viz.tracer
    
    # Create a list with 200 nodes
    head = ListNode(0)
    current = head
    for i in range(1, 200):
        current.next = ListNode(i)
        current = current.next
    
    serialized = tracer._serialize_value(head)
    
    assert serialized['type'] == 'LinkedList'
    # Should be truncated
    assert len(serialized['values']) <= 101  # 100 + '...'
    assert '...' in serialized['values']


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
