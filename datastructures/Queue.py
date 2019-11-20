"""Module containing a Queue class."""

from datastructures.DoublyLinkedList import DoublyLinkedList

class Queue:
    """A queue implemented with a linked list."""

    def __init__(self):
        """Initialize the queue as a linked list."""
        self.list = DoublyLinkedList()

    def push(self, item):
        """Add an item to the back of the queue."""
        self.list.add(item)

    def pop(self):
        """Remove and return item from front of the queue; None if empty."""
        if not self.list.is_empty():
            return self.list.remove_from_front()
        else:
            return None

    def peek(self):
        """Return node at front of queue without removing; None if empty."""
        if not self.list.is_empty():
            return self.list.head.data
        else:
            return None

    def is_empty(self):
        """Return whether or not the queue is empty."""
        return self.list.is_empty()
