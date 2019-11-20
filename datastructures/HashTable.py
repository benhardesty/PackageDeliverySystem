"""Module containing a hashtable class."""

import math
import hashlib

from datastructures.Node import Node
from datastructures.DoublyLinkedList import DoublyLinkedList

class HashTable:
    """A hashtable implemented using chaining."""

    def __init__(self, size=40, get_key_function=None):
        """Initialize the hashtable.

        Keyword arguments:
        size -- the number of indexes in the hashtable (default is 40).
        get_key_function -- function to identify the key of each item.
        """

        self.table = []
        self.size = size

        # Default get_key function is the item itself.
        if get_key_function == None:
            self.get_key = lambda el : el.data
        else:
            self.get_key = get_key_function

        # Initialize all hash indexes as linked lists.
        for i in range(self.size):
            self.table.append(DoublyLinkedList(get_key_function))

    def add(self, item):
        """
        Add an item to the hash table.

        Time complexity: O(1)
        """

        key = self.get_key(item)
        index = self.hash(key)
        self.table[index].add(item)

    def hash(self, key):
        """
        Calculate a hash value for the provided key.

        Binary mid square hash function is used for numbers and
        multiplicative string hash function is used for stings.

        Time complexity: O(1)
        """

        # Mid square hash function for numbers.
        if type(key) is int or type(key) is float:

            squaredKey = key**2
            # Bits required to represent self.size.
            R = math.ceil(math.log2(self.size))
            # Bits required to represent squaredKey.
            bits_in_key = math.ceil(math.log2(squaredKey))

            if bits_in_key < R:
                return squaredKey % self.size
            else:
                # Right shift squaredKey by (bits_in_key - R) / 2
                new_key = squaredKey >> math.floor((bits_in_key - R) / 2)
                # All bits set to 1 for R bits.
                mid_bits_on = 2**R - 1
                # Bitwise AND.
                extracted_bits = new_key & mid_bits_on
                return extracted_bits % self.size

        # Multiplicative string hash function for strings.
        else:
            hash = self.size * 7

            for char in key:
                hash *= 11
                hash += ord(char)

            return hash % self.size

    def get(self, key):
        """
        Retrieve an item from the hashtable; return None if item not found.

        Keyword arguments:
        key -- the key of the item to be returned.


        Time complexity: O(1)
        """

        index = self.hash(key)
        item = self.table[index].search(key)
        return item

    def remove(self, key):
        """
        Remove and return an item from the hashtable; return None if not found.

        Keyword arguments:
        key -- the key of the item to be removed and returned.

        Time complexity: O(1)
        """

        index = self.hash(key)
        item = self.table[index].remove(key)
        return item

    def get_all(self, key):
        """
        Return a linked list of all items in the table with a given key.

        Keyword arguments:
        key -- the key of the item(s) to be returned.
        """

        index = self.hash(key)
        list = self.table[index].exhaustive_search(key)
        return list
