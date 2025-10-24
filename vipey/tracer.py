# tracer.py
import sys
import copy
from typing import Any, Dict, List, Callable

class Tracer:
    def __init__(self, ast_map: Dict[int, str], source_code: str = "", custom_serializers: dict = None):
        self.ast_map = ast_map
        self.source_code = source_code
        self.storyboard = []
        self._return_value = None
        self.custom_serializers = custom_serializers or {}

    def trace_function(self, func: Callable, *args, **kwargs):
        """Trace the execution of a function and capture frames."""
        def tracer(frame, event, arg):
            if event == 'line':
                lineno = frame.f_lineno
                event_type = self.ast_map.get(lineno, 'other')
                frame_data = {
                    'line': lineno,
                    'event_type': event_type,
                    'locals': self._serialize_locals(frame.f_locals),
                }
                self.storyboard.append(frame_data)
            elif event == 'return':
                self._return_value = arg
            return tracer
        
        sys.settrace(tracer)
        result = func(*args, **kwargs)
        sys.settrace(None)
        
        storyboard_data = {
            'frames': self.storyboard,
            'return_value': self._serialize_value(self._return_value),
            'source_code': self.source_code
        }
        
        # Return both storyboard and the actual result
        return storyboard_data, result
    
    def _serialize_locals(self, locals_dict: dict) -> dict:
        """Serialize local variables, handling common Python types."""
        serialized = {}
        for key, value in locals_dict.items():
            try:
                # Skip special variables
                if key.startswith('__'):
                    continue
                # Try to create a JSON-serializable copy
                serialized[key] = self._serialize_value(value)
            except Exception:
                serialized[key] = f"<unserializable: {type(value).__name__}>"
        return serialized
    
    def _serialize_value(self, value):
        """Serialize a single value, with auto-detection of data structures."""
        # Check for custom serializers first
        for data_type, serializer in self.custom_serializers.items():
            if isinstance(value, data_type):
                return serializer(value)
        
        # Auto-detect linked list (object with 'val'/'value' and 'next')
        if hasattr(value, 'next') and hasattr(value, 'val'):
            return self._serialize_linked_list(value, 'val')
        elif hasattr(value, 'next') and hasattr(value, 'value'):
            return self._serialize_linked_list(value, 'value')
        
        # Auto-detect tree node (object with 'left'/'right' and 'val'/'value'/'key')
        if (hasattr(value, 'left') or hasattr(value, 'right')):
            if hasattr(value, 'val'):
                return self._serialize_tree(value, 'val')
            elif hasattr(value, 'value'):
                return self._serialize_tree(value, 'value')
            elif hasattr(value, 'key'):
                return self._serialize_tree(value, 'key')
        
        # Auto-detect graph (dict with 'nodes' and 'edges' keys or defaultdict)
        if isinstance(value, dict):
            # Check if it looks like an adjacency list
            if all(isinstance(k, (int, str)) and isinstance(v, (list, set)) for k, v in value.items()):
                # Could be a graph adjacency list
                if len(value) > 0:
                    return self._serialize_graph_adjacency_list(value)
        
        # Default serialization
        if isinstance(value, (int, float, str, bool, type(None))):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        else:
            return str(value)
    
    def _serialize_linked_list(self, head, value_attr='val'):
        """Serialize a linked list into a visual format."""
        values = []
        current = head
        visited = set()
        
        while current is not None:
            # Prevent infinite loops in circular lists
            if id(current) in visited:
                values.append('...')
                break
            visited.add(id(current))
            
            # Get the value
            val = getattr(current, value_attr, None)
            values.append(val)
            
            # Move to next
            current = getattr(current, 'next', None)
            
            # Safety limit
            if len(values) > 100:
                values.append('...')
                break
        
        return {
            'type': 'LinkedList',
            'values': values,
            'display': ' -> '.join(str(v) for v in values)
        }
    
    def _serialize_tree(self, root, value_attr='val'):
        """Serialize a tree into a visual format."""
        if root is None:
            return None
        
        def build_tree_dict(node):
            if node is None:
                return None
            
            result = {
                'value': getattr(node, value_attr, None)
            }
            
            # Add children
            left = getattr(node, 'left', None)
            right = getattr(node, 'right', None)
            
            if left is not None:
                result['left'] = build_tree_dict(left)
            if right is not None:
                result['right'] = build_tree_dict(right)
            
            # Add AVL-specific attributes if present
            if hasattr(node, 'height'):
                result['height'] = node.height
            if hasattr(node, 'balance'):
                result['balance'] = node.balance
            
            return result
        
        tree_type = 'Tree'
        if hasattr(root, 'height'):
            tree_type = 'AVL'
        
        return {
            'type': tree_type,
            'root': build_tree_dict(root)
        }
    
    def _serialize_graph_adjacency_list(self, adj_list):
        """Serialize a graph adjacency list into a visual format."""
        nodes = list(adj_list.keys())
        edges = []
        
        for node, neighbors in adj_list.items():
            for neighbor in neighbors:
                edges.append([node, neighbor])
        
        return {
            'type': 'Graph',
            'nodes': nodes,
            'edges': edges,
            'directed': True,
            'display': f'{len(nodes)} nodes, {len(edges)} edges'
        }
