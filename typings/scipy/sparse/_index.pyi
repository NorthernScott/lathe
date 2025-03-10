"""
This type stub file was generated by pyright.
"""

"""Indexing mixin for sparse array/matrix classes.
"""
INT_TYPES = ...
class IndexMixin:
    """
    This class provides common dispatching and validation logic for indexing.
    """
    def __getitem__(self, key):
        ...
    
    def __setitem__(self, key, x):
        ...
    


