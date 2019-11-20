"""Module containing a linked list class."""

import copy

from datastructures.Node import Node

class DoublyLinkedList:
    """A linked list class."""

    def __init__(self, get_key_function=None):
        """
        Initialize the head and tail of the linked list to None.

        Keyword arguments:
        get_key_function -- function to identify the key of each item.
        """

        self.head = None
        self.tail = None

        # The default key of a node is the node's data field.
        if get_key_function == None:
            self.get_key = lambda el : el.data
        else:
            self.get_key = lambda el: get_key_function(el.data)

    def add(self, item):
        """Add a node to the back of the linked list."""
        node = Node(item)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def add_to_front(self, item):
        """Add a node to the front of the linked list."""
        node = Node(item)
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_from_front(self):
        """Remove and return node at the front of the linked list."""
        if self.head == None:
            return None
        elif self.head == self.tail:
            temp = self.head
            self.head = None
            self.tail = None
            return temp.data
        else:
            temp = self.head
            self.head = self.head.next
            self.head.prev = None
            return temp.data

    def remove(self, key):
        """Remove and return a node with the specified key."""
        if self.head == None:
            return None
        else:
            current = self.head
            while current != None:
                if key == self.get_key(current):
                    if current == self.head:
                        if current == self.tail:
                            self.head = None
                            self.tail = None
                            return current
                        else:
                            self.head = self.head.next
                            self.head.prev = None
                            return current
                    elif current == self.tail:
                        self.tail = self.tail.prev
                        self.tail.next = None
                        return current
                    else:
                        current.prev.next = current.next
                        current.next.prev = current.prev
                        return current
            return None

    def search(self, key):
        """
        Search and return a node with a specific key; return None if not found.

        Keyword arguments:
        key -- key of the searched for item.
        """
        if self.head == None:
            return None
        else:
            current = self.head
            while current != None:
                if key == self.get_key(current):
                    return current.data
                current = current.next
            return None

    def exhaustive_search(self, key):
        """
        Return a linked list of nodes with the specified key or None if none found.

        Keyword arguments:
        key -- key of the searched for item.
        """
        if self.head == None:
            return None
        else:
            node = None
            runner = None
            current = self.head
            while current != None:
                if key == self.get_key(current):
                    if node == None:
                        node = Node(current.data)
                        runner = node
                    else:
                        new_node = Node(current.data)
                        runner.next = new_node
                        runner = new_node
                current = current.next
            return node

    def is_empty(self):
        """Return whether or not the list is empty."""
        if self.head == None:
            return True
        else:
            return False
