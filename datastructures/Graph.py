"""Module containing Graph and Vertex classes."""

from datastructures.HashTable import *
from datastructures.MinHeap import *
from datastructures.PriorityQueue import *
from datastructures.Stack import *

class Vertex:
    """A vertex in a graph."""

    def __init__(self, data):
        """
        Initialize the vertex item.

        Keyword arguments:
        data -- the data associated with the vertex.
        """

        self.data = data
        self.distance = 0
        self.previous_vertex = None

    def __lt__(self, other):
        """Override the less than operator based on the vertex's distance."""
        return self.distance < other.distance

    def __gt__(self, other):
        """Override the greater than operator based on the vertex's distance."""
        return self.distance > other.distance

class Graph:
    """A graph class containing vertices and edges."""

    def __init__(self, size=27, get_key_function=None):
        """
        Initialize the graph.

        The graph will be created using a list of adjacent vertices for each
        vertex and a dictionary of edges between vertices.
        """
        self.adjacency_list = {}
        self.edge_weights = {}
        self.size = size

        if get_key_function == None:
            self.get_key = lambda el : el.data
        else:
            self.get_key = get_key_function

        self.vertices = HashTable(self.size, get_key_function)

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.

        Keyword arguments:
        vertex -- the vertex to add to the graph.
        """
        self.adjacency_list[vertex] = []

    def add_directed_edge(self, from_v, to_v, weight=1.0):
        """
        Add a directed edge between vertices.

        Keyword arguments:
        from_v -- the starting vertex.
        to_v -- the end vertex.
        weight -- the distance or weight of the edge (default of one).
        """
        self.adjacency_list[from_v].append(to_v)
        self.edge_weights[(from_v,to_v)] = weight

    def add_undirected_edge(self, vertex_1, vertex_2, weight=1.0):
        """
        Add an undirected edge between vertices.

        An undirected edge between vertices is established by creating two
        directed edges between the vertices.

        Keyword arguments:
        vertex_1 -- a vertex object.
        vertex_2 -- a vertex object.
        weight -- the distance or weight between the edges (default of 1).
        """
        self.add_directed_edge(vertex_1, vertex_2, weight)
        self.add_directed_edge(vertex_2, vertex_1, weight)

    def dijkstra_shortest_path(self, start_vetex):
        """
        Find the shortest distance from a starting vertex to all other vertices.

        Keyword arguments:
        start_vertex -- a vertex object.

        Time complexity:
        O(VLogV + ELogV)

        Space complexity:
        O(V)
        """

        unvisited_queue = PriorityQueue(self.size, lambda el : el.distance, lambda el : el.data)

        # Set all vertices to a distance of infinity and a previous vertex
        # of None. Set the start_vertex's distance to 0.
        for vertex in self.adjacency_list:
            vertex.distance = float('inf')
            vertex.previous_vertex = None
            if vertex == start_vetex:
                vertex.distance = 0
            unvisited_queue.push(vertex)

        # Time complexity: O(V)
        while not unvisited_queue.is_empty():

            # Time complexity: O(LogV)
            current_vertex = unvisited_queue.pop()

            # Go through each of the current_vertex's adjacent vertices checking
            # to see if the path from the current vertex is shorter than the
            # previously found paths.
            # Time complexity: O(E)
            for adjacent_vertex in self.adjacency_list[current_vertex]:

                edge_weight = self.edge_weights[(current_vertex,adjacent_vertex)]
                new_distance = current_vertex.distance + edge_weight

                # If a shorter path is found, update the adjacent vertex's distance
                # to the new distance and set it's previous pointer to the
                # current vertex.
                if new_distance < adjacent_vertex.distance:
                    adjacent_vertex.distance = new_distance
                    adjacent_vertex.previous_vertex = current_vertex

                    # Time complexity: O(LogV)
                    unvisited_queue.update_priority(adjacent_vertex)


    def find_shortest_path(self, start_vetex, end_vertex):
        """
        Return a list of vertices creating a path from the start to end vertices.

        Keyword arguments:
        start_vetex -- the starting vertex.
        end_vertex -- the ending vertex.

        Time complexity: O(V)
        Space complexity: O(V)
        """
        if end_vertex.distance == float('inf'):
            return []
        else:
            reverse = Stack()
            current_vertex = end_vertex
            reverse.push(current_vertex)
            while current_vertex != start_vetex:
                current_vertex = current_vertex.previous_vertex
                reverse.push(current_vertex)

            path = []
            while not reverse.is_empty():
                path.append(reverse.pop())

            return path
