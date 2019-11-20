"""Module containing a Stack class."""

from datastructures.DoublyLinkedList import DoublyLinkedList

class Stack:
    """A stack implemented with a linked list."""

    def __init__(self):
        """Initialize the stack as a linked list."""
        self.list = DoublyLinkedList()

    def push(self,item):
        """Add an item to the top of the stack."""
        self.list.add_to_front(item)

    def pop(self):
        """Remove and return top item from Stack; None if empty."""
        return self.list.remove_from_front()

    def peek(self):
        """Return top item from Stack without removing; None if empty."""
        if self.list.head == None:
            return None
        return self.list.head.data

    def is_empty(self):
        """Return whether or not Stack is empty."""
        return self.list.is_empty()

    def clear(self):
        """Clear the stack by initializing a new linked list."""
        self.list = DoublyLinkedList()
