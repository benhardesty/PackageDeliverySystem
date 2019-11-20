"""Module containing a min heap class."""

import math

class MinHeap:

    def __init__(self, get_key_function=None):
        """
        Initialize the MinHeap object.

        Keyword arguments:
        get_key_function -- used to identify the priority of an item in the heap.
        """

        self.list = []

        if get_key_function == None:
            self.get_key = lambda el : el
        else:
            self.get_key = get_key_function

    def push(self, item):
        """
        Add an item to the heap.

        Add a node to the back of the heap, and then percolate it up.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        self.list.append(item)
        self.percolate_up(len(self.list) - 1)

    def pop(self):
        """
        Remove the minimum item from the heap.

        Remove node from the front of the heap by swapping it with the node
        at the back and percolating the new root down.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        if len(self.list) == 0:
            return None
        else:
            min_item = self.list[0]
            last_item = self.list.pop()
            if len(self.list) > 0:
                self.list[0] = last_item
                self.percolate_down(0)
            return min_item

    def peek(self):
        """Return the smallest item without removing it from the heap."""

        if len(self.list) == 0:
            return None
        else:
            return self.list[0]

    def percolate_up(self, index):
        """
        Percolate an item up the heap to it's proper location.

        Starting at a specified index, if the node at that index is less than it's
        parent, swap it with it's parent, and then continue percolating up.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        while index > 0:
            parent = math.floor((index - 1)/2)
            if self.get_key(self.list[index]) < self.get_key(self.list[parent]):
                self.swap(parent, index)
                index = parent
            else:
                return

    def percolate_down(self, index):
        """
        Percolate an item down the heap to it's proper location.

        Starting at a specified index, if the node at that index is greater than
        the greatest of it's children, swap it with it's greatest child and then
        continue percolating down.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        while index < len(self.list):
            left_child = index*2 + 1
            right_child = index*2 + 2

            # Determine the minimum index between a node and it's children.
            min_index = index
            if left_child < len(self.list) and self.get_key(self.list[left_child]) < self.get_key(self.list[min_index]):
                min_index = left_child
            if right_child < len(self.list) and self.get_key(self.list[right_child]) < self.get_key(self.list[min_index]):
                min_index = right_child

            # If a child node is less than the parent, swap them, else return.
            if min_index != index:
                self.swap(index, min_index)
                index = min_index
            else:
                return

    def swap(self, i, j):
        """Swap two elements in the list."""

        temp = self.list[i]
        self.list[i] = self.list[j]
        self.list[j] = temp

    def heapify(self, array):
        """
        Turn an array into a min heap.

        Turn an array into a min heap by running percolate_up on all leaf nodes
        in the min heap.

        Keyword arguments:
        array -- an array to turn into a heap.

        Time complexity: O(n)
        Space complexity: O(1)
        """

        heap = MinHeap()
        heap.list = array

        if len(heap.list) > 0:
            height = math.floor(math.log2(len(heap.list)))
            leaves_if_full = 2**height
            nodes_if_full = leaves_if_full * 2 - 1
            first_leaf = nodes_if_full - leaves_if_full
            for index in range(first_leaf,len(heap.list)):
                heap.percolate_up(index)
        return heap

    def is_empty(self):
        """Return whether or not the heap is empty."""

        if len(self.list) == 0:
            return True
        return False

    def get_length(self):
        """Return the number of items in the min heap."""

        return len(self.list)
