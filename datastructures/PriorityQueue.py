"""Module containing a priority queue class."""

import math

from datastructures.MinHeap import MinHeap
from datastructures.HashTable import HashTable

class IndexItem:
    """Helper class to track the index of items in the Priority Queue."""

    def __init__(self, data, index):
        """Initialize the IndexItem."""

        self.data = data
        self.index = index

class PriorityQueue(MinHeap):

    def __init__(self, size, get_key_function=None, hashtable_get_key_function=None):
        """
        Initialize the PriorityQueue object.

        PriorityQueue inherits from MinHeap. A hashtable is added to keep
        track of items in the priority queue in order to update priorities. The
        push, pop, and swap methods of MinHeap have been overridden in order
        to store the items in the hashtable. A get_index method has been added
        to get the index of an item in the heap in O(1) time. A update_priority
        method has been added to call get_index and percolate the item up or
        down in the queue.

        Keyword arguments:
        size - expected size of the priority queue to be used for the hashtable.
        get_key_function -- used to identify the priority of an item in the heap.
        hashtable_get_key_function - used to identify the item in the hashtable.
        """

        super().__init__(get_key_function)

        if hashtable_get_key_function == None:
            self.hashtable_get_key = lambda el : el
        else:
            self.hashtable_get_key = hashtable_get_key_function

        self.index_table = HashTable(size, self.hashtable_get_key)

    def push(self, item):
        """
        Add an item to the heap.

        Add a node to the back of the heap, and then percolate it up. Overrides
        the push method of MinHeap to add the item to the hashtable.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        # Add this item to the hash table with an index of the length of list.
        index_item = IndexItem(self.hashtable_get_key(item), len(self.list))
        self.index_table.add(index_item)

        # Add the item to the list.
        self.list.append(item)
        # Percolate up the item until it reaches it's correct index.
        self.percolate_up(len(self.list) - 1)

    def pop(self):
        """
        Remove the minimum item from the heap.

        Remove node from the front of the heap by swapping it with the node
        at the back and percolating the new root down. Overrides the pop method
        to update the index of the item that is percolated down.

        Time complexity: O(log n)
        Space complexity: O(1)
        """

        if len(self.list) == 0:
            return None
        else:
            min_item = self.list[0]

            # Get the last item in the list.
            last_item = self.list.pop()

            # If there was a last item.
            if len(self.list) > 0:

                # Place the last_item at the front of the list.
                self.list[0] = last_item

                # Update the last_item with it's new index
                index_item = self.index_table.get(self.hashtable_get_key(last_item))
                index_item.index = 0

                # Percolate the last_item down.
                self.percolate_down(0)

            return min_item

    def swap(self, i, j):
        """Swap two elements in the list."""

        # Update each item's index in the index hash table.
        self.index_table.get(self.hashtable_get_key(self.list[i])).index = j
        self.index_table.get(self.hashtable_get_key(self.list[j])).index = i

        # Swap the two items.
        temp = self.list[i]
        self.list[i] = self.list[j]
        self.list[j] = temp

    def update_priority(self, item):
        """
        Update the position of an item in the queue if it's priorty changed.

        Time complexity: O(log n)
        """

        index = self.get_index(item)
        self.percolate_up(index)
        self.percolate_down(index)

    def get_index(self, item):
        """
        Get the index of an item in the priority queue.

        Time complexity: O(1)
        """

        return self.index_table.get(self.hashtable_get_key(item)).index
