"""Module containing a simple Node class."""

class Node:
    """A simple node class."""

    def __init__(self, data=None):
        """Initialize a Node with data, next, and prev fields."""

        self.data = data
        self.next = None
        self.prev = None
