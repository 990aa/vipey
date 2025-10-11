# tracer.py
import sys
import copy
from typing import Any, Dict, List, Callable

class Tracer:
    def __init__(self, ast_map: Dict[int, str], source_code: str = ""):
        self.ast_map = ast_map
        self.source_code = source_code
        self.storyboard = []
        self._return_value = None

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
        
        return {
            'frames': self.storyboard,
            'return_value': self._return_value,
            'source_code': self.source_code
        }
    
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
        """Serialize a single value."""
        if isinstance(value, (int, float, str, bool, type(None))):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        else:
            return str(value)
