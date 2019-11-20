"""A truck object used to move across a graph and deliver packages."""

from datastructures.MinHeap import *
from datastructures.Stack import Stack
from datastructures.HashTable import HashTable
from datastructures.Queue import Queue

class Truck:
    def __init__(self, number, location, max_packages=18, speed=16, mileage=0):
        """
        Initialize a truck object.

        Keyword arguments:
        number -- the truck's identification number.
        location -- the current vertex the truck is located at on a graph.
        max_packages -- the maximum packages the truck can hold.
        speed -- the speed the truck travels at.
        mileage -- the mileage of the truck.
        """

        self.number = number
        self.max_packages = max_packages
        self.speed = speed
        self.location = location
        self.mileage = mileage
        self.dist_to_next_vertex = 0
        self.packages = []
        self.destinations = Stack()

    def add_package(self, package):
        """Load a package onto the truck."""
        if len(self.packages) < self.max_packages:
            self.packages.append(package)
            return True
        else:
            return False

    def is_full(self):
        """Return whether or not the truck is full."""
        if len(self.packages) >= self.max_packages:
            return True
        else:
            return False
