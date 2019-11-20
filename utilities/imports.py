"""Functions used to import package and graph data."""

from datastructures.Graph import *
from models.Package import *
from utilities.time import *

def import_packages_to_hashtable(hashtable, packages, filename):
    """Import package data into a list and a hash table."""

    with open(filename) as f:
        lines = f.readlines()

        # Read each line in the file, create a package item for it, and place
        # the package in the hashtable.
        for line in lines:
            line = line.strip()
            line = line.replace('"','')
            line = line.split(",")

            # If the special notes column has commas in it, correct the multiple
            # comma separated columns to 1 column.
            special_notes = ""
            if len(line) > 8:
                special_notes = line[7]
                for i in range(8, len(line)):
                    special_notes += ", " + line[i]
                line = line[:7] + [special_notes]

            # Create a package.
            package = Package(int(line[0]), str(line[1]), str(line[2]), str(line[3]),
                              str(line[4]), convert_standard_time_to_minutes(str(line[5])),
                              int(line[6]), str(line[7]))

            # Place the package into the hash table.
            hashtable.add(package)

            # Add the package to the provided queue.
            packages.append(package)

def import_distance_map_to_graph(g, v, filename):
    """Import distance table into the graph as weighted edges."""

    with open(filename) as f:
        lines = f.readlines()
        matrix = []
        address_list = []

        # Convert each line in the file to a list and append the list to the
        # matrix list to create a 2d list. Get the address at the beginning
        # of each line and add it to the address list.
        for i, line in enumerate(lines):
            if i == 0:
                continue
            line = line.strip()
            line = line.split(',')
            matrix.append(line[1:i])
            address_list.append(line[0])

        # Add vertices to the graph for each address imported from the file.
        for address in address_list:
            vertex = Vertex(address)
            g.add_vertex(vertex)
            v.add(vertex)

        # For each unique intersection in the matrix, create a new vertex and
        # add an undirected edge to the graph.
        for c, col in enumerate(matrix):
            for r, row in enumerate(col):
                weight = float(matrix[c][r])
                if weight > 0.0:
                    vertex_a = v.get(address_list[c])
                    vertex_b = v.get(address_list[r])
                    g.add_undirected_edge(vertex_a, vertex_b, weight)
