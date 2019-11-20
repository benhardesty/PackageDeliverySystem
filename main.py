"""
Main script to import data, load packages onto trucks, and deliver packages.

Functions:
print_packages -- print details of all packages.
print_package -- print details of a single package.
min_path -- determine the minimum path through a set of vertices.
set_destinations_for_truck -- set the order of vertices to visit for a truck.
get_unique_addresses -- get unique addresses from a list of addresses.
load_trucks -- load trucks with packages.
deliver_packages -- deliver packages off a truck to a specified location.
management_updates_at_hub -- update packages_at_hub with newly received packages.
management_updates_for_trucks -- notify trucks of updates at the hub.
"""

from datastructures.Node import Node
from datastructures.Graph import Graph, Vertex
from datastructures.HashTable import HashTable
from datastructures.MinHeap import MinHeap
from datastructures.Stack import Stack
from models.Package import Package
from models.Truck import Truck
from utilities import imports
from utilities.time import *

def print_packages() -> None:
    """Print details of all packages."""

    print("Package ID | Status | Address | Delivery Deadline | Time Delivered"
        + " | Mass | Special Notes")
    for i in range(1,41):
        print_package(i, False)

def print_package(id, header=True) -> None:
    """
    Print details of a single package.

    Keyword arguments:
    package -- the package to print.
    header -- boolean indicating whether to print a header.
    """

    package = packages_hashtable.get(id)
    if package != None:
        package_id = package.package_id
        address = (package.address + " " + package.city + ", "
                   + package.state + " " + package.zip)
        deadline = convert_minutes_to_standard_time(package.delivery_deadline)
        delivered = ("En Route" if package.delivered_time == None
                     else convert_minutes_to_standard_time(package.delivered_time)
                    )
        mass = package.mass
        notes = package.special_notes
        status = package.status

        if header:
            print("Package ID | Status | Address | Delivery Deadline |"
                + " Time Delivered | Mass | Special Notes")

        print(package_id, "|", status, "|", address, "|", deadline, "|", delivered,
             "|", mass, "|", notes)
    else:
        print("Package not found.")

def min_path(start, set, end, graph) -> []:
    """
    Return the minimum path through a set of vertices as a list.

    Determine the minimum path from a starting vertex, through a set of vertices,
    to  an ending vertex. The minimum path will be chosen by finding the shortest
    path to the next closest vertex (greedy approach).

    Keyword arguments:
    start -- the starting vertex.
    set -- a list of vertices to visit.
    end -- the vertex to end at.
    graph -- the graph containing the vertices.

    Time complexity: O(S * (VLogV + ELogV)) where S is the number of vertices in
    the set of vertices to visit, V is the number of vertices in the graph, and
    E is the number of edges in the graph.

    Space complexity: O(V)
    """

    full_path = [start]

    # Time complexity: O(S)
    while len(set) > 0:

        # Time complexity: O(V^2)
        graph.dijkstra_shortest_path(start)

        # Time complexity: O(S)
        index = 0
        for i, v in enumerate(set):
            if v.distance < set[index].distance:
                index = i
        closest_vertex = set[index]

        # Time complexity: O(S)
        set.pop(index)

        # Time complexity: O(V)
        path = graph.find_shortest_path(start, closest_vertex)

        # If a path was found to the closest vertex.
        if len(path) > 0:
            full_path.pop()
            full_path += path
            start = closest_vertex

        # If a path does not exist, the search can stop here.
        else:
            break

    # Determine the shortest path from the last vertex visited in the set
    # to the end vertex.
    graph.dijkstra_shortest_path(start)
    path = graph.find_shortest_path(start, end)

    # If a path was found.
    if len(path) > 0:
        full_path.pop()
        full_path += path
        return full_path

    # If a path was not found, return the path found thus far.
    else:
        return full_path

def set_destinations_for_truck(truck, addresses_to_visit, ending_address, graph) -> None:
    """
    Set the destination order for a truck to visit.

    Add all vertices that a truck needs to visit onto the truck's destinations
    stack field starting with the last vertex to visit and ending with the
    first (the first vertex to visit will be on top of the stack).

    Keyword arguments:
    truck -- a truck object.
    addresses_to_visit -- a list of addresses the truck needs to visit.
    ending_address -- the address the truck should end at.
    graph -- the graph containing the vertices to visit.
    """

    # Get a unique set of addresses to visit.
    addresses = get_unique_addresses(addresses_to_visit)

    # Order the destinations that the truck needs to visit to deliver packages.
    destination_list = min_path(
        truck.location, [graph.vertices.get(i) for i in addresses],
        graph.vertices.get(ending_address), graph)

    # Load the destinations onto the truck's destinations stack.
    truck.destinations = Stack()
    while len(destination_list) > 0:
        truck.destinations.push(destination_list.pop())

    # The truck is already at the current location.
    truck.destinations.pop()

    # Deermine the truck's distance to the next destination.
    if not truck.destinations.is_empty():
        truck.dist_to_next_vertex = graph.edge_weights[
            (truck.location, truck.destinations.peek())
            ]

def get_unique_addresses(address_list) -> []:
    """Return a unique set of addresses given a list of addresses."""
    addresses = []
    for address in address_list:
        if address not in addresses:
            addresses.append(address)
    return addresses

def load_trucks(trucks_to_load, packages, graph) -> None:
    """
    Load trucks with packages.

    Pop packages off the packages_at_hub min heap, add them to each truck
    in the trucks_to_load list, and then determinte the order in which
    to visit the delivery addresses for the packages on each truck.

    Keyword arguments:
    trucks_to_load -- a list of trucks to load with packages.
    packages -- a min heap of packages to load.
    graph -- the graph containing the vertices at which to delivery the packages.
    """

    # For each truck, while the truck is not full and there are packages at the
    # hub, load the package onto the truck.
    for truck in trucks_to_load:
        trucks_have_room = True
        while trucks_have_room and not packages.is_empty():
            trucks_have_room = False
            if not truck.is_full():
                package = packages.pop()
                if package != None:
                    package.status = "Out for delivery"
                    truck.add_package(package)
                    trucks_have_room = True

    # For each truck, determine the fastest route through all package
    # destinations and back to the HUB.
    for truck in trucks_to_load:
        set_destinations_for_truck(
            truck, [i.address_and_zip for i in truck.packages], hub_address,
            graph
            )

def deliver_packages(truck, vertex, time) -> None:
    """
    Deliver packages that have a delivery address at the provided location

    Keyword arguments:
    truck -- the truck containing packages to deliver.
    vertex -- the vertex on the graph at which the truck has arrived.
    time -- the current time.

    Time complexity:
    Worst case: O(p^2). The worst case is if all packages are delivered to one location.
    Average case: O(p). The average case assumes that typically one package will be
                        delivered to each location.

    Space complexity:
    Worst case: O(p)
    Average case: O(1)
    """

    # Go through the packages on the truck and deliver all packages with
    # a delivery address of this location.
    packages_delivered = []
    for package in truck.packages:
        if package.address_and_zip == vertex.data:
            package.delivered_time = time
            if package.delivered_time <= package.delivery_deadline:
                package.status = "DELIVERED ON TIME"
            else:
                package.status = "DELIVERED LATE"
            packages_delivered.append(package)

    # Remove all delivered packages from the truck's packages list.
    for package in packages_delivered:
        truck.packages.pop(truck.packages.index(package))

def management_updates_at_hub(time) -> None:
    """
    Check for packages received at the hub or other management updates.

    Keyword arguments:
    time -- the current time.
    """

    # Packages 6, 25, 28, and 32 are arriving to the hub at 09:05:00 AM.
    # Time complexity: O(n). There is a maximum of 4 packages.
    # Space complexity: O(1). There is a maximum of 4 packages.
    if (time >= convert_standard_time_to_minutes("09:05:00 AM")
            and time <= convert_standard_time_to_minutes("09:10:00 AM")):
        packages_removed = []
        for package in packages:
            if package.package_id in [6, 25, 28, 32]:
                package.status = "Arrived at HUB"
                packages_at_hub.push(package)
                packages_removed.append(package)
        for package in packages_removed:
            packages.pop(packages.index(package))

    # Package 9 is having it's delivery address corrected at 10:20:00 AM.
    # Time complexity: O(n). There is a maximum of 1 package.
    # Space complexity: O(1).
    if (time >= convert_standard_time_to_minutes("10:20:00 AM")
            and time <= convert_standard_time_to_minutes("10:25:00 AM")):
        packages_removed = []
        for package in packages:
            if package.package_id in [9]:
                package.address = "410 S State St"
                package.zip = "84111"
                package.address_and_zip = "410 S State St (84111)"
                package.status = "Arrived at HUB"
                packages_at_hub.push(package)
                packages_removed.append(package)
        for package in packages_removed:
            packages.pop(packages.index(package))

def management_updates_for_trucks(truck, time) -> None:
    """
    Inform a truck of management updates to delivery locations and deadlines.

    Keyword arguments:
    truck -- a truck object.
    time -- the current time.
    """

    # If the time is between 09:00:00 AM and 09:05:00 AM, add the HUB to the
    # destinations stack of the truck to pick up packages 6, 25, 28, and 32.
    if (time >= convert_standard_time_to_minutes("09:00:00 AM")
            and time <= convert_standard_time_to_minutes("09:05:00 AM")):
        address_list = get_unique_addresses(
            [i.address_and_zip for i in truck.packages]
            )
        address_list.append(hub_address)
        set_destinations_for_truck(truck, address_list, hub_address, graph)

def program_interface(trucks, current_time, run_until):
    """
    Interface to run the program.

    Interface allowing the admin to run the program for a specified length
    of time, print packages, or print truck details.

    Keyword arguments:
    trucks -- an array of the trucks that are delivering packages.
    current_time -- the current time.
    run_until -- the next time to stop the program to ask for further instructions.
    """
    while True:
        print()
        print("Current time:", convert_minutes_to_standard_time(current_time))
        print()
        print("1. Run program for 1 virtual hour.")
        print("2. Run program for 4 virtual hours.")
        print("3. Run program until completion.")
        print("4. Print packages.")
        print("5. Print truck details.")
        print()
        option = input("Enter selection: ")
        print()

        # Guard against the user entering letters.
        try:
            option = int(option)

            # Run for 1 hour.
            if option == 1:
                run_until[0] += 60
                break
            # Run for 4 hours.
            elif option == 2:
                run_until[0] += 60*4
                break
            # Run until EOD.
            elif option == 3:
                run_until[0] += 60*9
                break
            # Print packages.
            elif option == 4:

                while True:
                    print("1. Choose a package to print.")
                    print("2. Print all packages.")
                    print()
                    option2 = input("Enter selection: ")
                    print()

                    # Guard against the user entering letters.
                    try:
                        option2 = int(option2)
                        if option2 == 1:
                            while True:
                                id = input("Package ID: ")
                                print()
                                try:
                                    id = int(id)
                                    print_package(id)
                                    print()
                                    break
                                except:
                                    print("Package ID must be an integer.")
                        if option2 == 2:
                            print_packages()
                            break
                        break

                    # Prompt user until they enter an integer.
                    except:
                        print("Please enter 1 or 2.")
                        print()

            # Print truck details.
            elif option == 5:
                for truck in trucks:
                    print("Truck", truck.number, "last location:", truck.location.data +
                    ", mileage: {:0.2f}".format(truck.mileage))
            else:
                print('Please select options 1, 2, 3, or 4.')
                print()

        # Prompt user until they enter an integer.
        except:
            print('Please enter 1, 2, 3, or 4.')
            print()

if __name__ == '__main__':

    # Graph to store map data.
    graph = Graph(27,lambda el : el.data)

    # Packages to be received at the hub.
    packages = []

    # Hashtable of all packages.
    packages_hashtable = HashTable(40,lambda el : el.package_id)

    # Packages received at the hub.
    packages_at_hub = MinHeap(lambda el : el.delivery_deadline)

    # Import map data.
    imports.import_distance_map_to_graph(graph, graph.vertices,
                                         "map_import_data.csv")
    # Import package data.
    imports.import_packages_to_hashtable(packages_hashtable, packages,
                                         "package_import_data.csv")
    # Locate the HUB.
    hub_address = "4001 South 700 East (84107)"
    hub_vertex = graph.vertices.get(hub_address)

    # Initialize truck variables.
    max_packages = 16
    truck_speed = 18
    trucks = []
    truck1 = Truck(1,hub_vertex,max_packages,truck_speed)
    truck2 = Truck(2,hub_vertex,max_packages,truck_speed)
    trucks.append(truck1)
    trucks.append(truck2)

    # Set time variables.
    current_time = convert_standard_time_to_minutes("08:00:00 AM")
    EOD = convert_standard_time_to_minutes("05:00:00 PM")

    # Set how often program checks for updates from the admin (in minutes).
    time_segment = 5

    # Receive packages at the hub and load to specified trucks if needed as per
    # the special notes.
    # Time complexity: O(n)
    # Space complexity: O(n)
    packages_remaining = []
    for package in packages:
        # Place all packages that need to be delivered together on one truck.
        if package.package_id in [13, 14, 15, 16, 19, 20]:
            package.status = "Out for delivery"
            truck1.packages.append(package)
        # Place all packages that must be delivered on truck 2 on truck 2.
        elif package.special_notes == "Can only be on truck 2":
            package.status = "Out for delivery"
            truck2.packages.append(package)
        # Add packages without any other special notes to the packages at the hub.
        elif package.special_notes == "":
            package.status = "Arrived at HUB"
            packages_at_hub.push(package)
        # The packages that have not arrived to the hub or are pending destination
        # address updates will remian in the packages queue.
        else:
            package.status = "Shipping to HUB"
            packages_remaining.append(package)
    packages = packages_remaining

    # Load the trucks with packages and set their routes.
    load_trucks(trucks, packages_at_hub, graph)

    # Control variable for the user interface.
    run_until = [convert_standard_time_to_minutes("08:00:00 AM")]
    print()
    print("Welcome to the package delivery system!")

    # Deliver packages from 08:00:00 AM until EOD at 05:00:00 PM. For each truck,
    # move the truck along the map for 5 minutes, then switch to the next truck.
    # Deliver packages at each vertex as the trucks moves across the map. Once a
    # truck has delivered all it's packages, it will go back to the HUB and pick
    # up more to deliver if any are left.
    while current_time < EOD:

        if current_time >= run_until[0]:
            program_interface(trucks, current_time, run_until)

        # Check for packages received at the hub or other management updates.
        management_updates_at_hub(current_time)

        # For each truck, move the truck along the map for 5 minutes, then switch
        # to the next truck.
        for truck in trucks:
            time = current_time
            stop_time = min((time + time_segment), EOD)

            # While the truck has scheduled destinations left to visit and time
            # is less than the stop time (current time + 5 minutes).
            while not truck.destinations.is_empty() and time < stop_time:

                # Determine the amount of time needed to get to the next destination.
                time_to_next_stop = truck.dist_to_next_vertex * 60 / truck.speed

                # If the truck can get to the next destination before the stop_time.
                if time + time_to_next_stop < stop_time:

                    # Update time.
                    time = time + time_to_next_stop

                    # Update the truck's location and mileage.
                    truck.location = truck.destinations.pop()
                    truck.mileage += truck.dist_to_next_vertex

                    # Check for updates to package priorities including delivery
                    # deadlines and delivery locations.
                    management_updates_for_trucks(truck, time)

                    # If the truck happens to be at the hub, check if there are more
                    # packages available for delivery and load the truck as needed.
                    if truck.location == hub_vertex:
                        if not packages_at_hub.is_empty():
                            load_trucks([truck], packages_at_hub, graph)
                    # If the truck is not at the hub, check if there are packages
                    # to deliver at the current location.
                    else:
                        deliver_packages(truck, truck.location, time)

                    # If the truck has more destinations to visit, update the
                    # truck's distance to the next destination and continue.
                    if not truck.destinations.is_empty():
                        truck.dist_to_next_vertex = graph.edge_weights[
                            (truck.location, truck.destinations.peek())
                        ]

                    # If the truck has no more scheduled destinations to visit.
                    else:

                        # If the truck is not at the hub, head back to the hub.
                        if truck.location != hub_vertex:
                            set_destinations_for_truck(truck, [], hub_address, graph)

                        # If the truck is at the hub.
                        else:

                            # If there are more packages at the hub, load the truck
                            # and continue.
                            if not packages_at_hub.is_empty():
                                load_trucks([truck], packages_at_hub, graph)

                # If the truck cannot get to the next destination before the stop
                # time, update the truck's mileage and distance to the next stop.
                else:
                    truck.dist_to_next_vertex -= (stop_time - time) * truck.speed / 60
                    truck.mileage += (stop_time - time) * truck.speed / 60
                    time = stop_time

            # If packages come later on in the day and the truck is sitting at the
            # hub, load the truck and continue delivering packages.
            if (truck.destinations.is_empty()
                    and truck.location == hub_vertex
                    and not packages_at_hub.is_empty()):
                load_trucks([truck], packages_at_hub, graph)

        # Move time along by the time segment (5 minutes).
        current_time += time_segment

    # Print status of all packages at EOD.
    print("Current time:", convert_minutes_to_standard_time(current_time))
    print()
    print_packages()
    print()

    # Print location and mileage of trucks at EOD.
    print("Truck 1 location: " + truck1.location.data + ", mileage: {:0.2f}".format(truck1.mileage))
    print("Truck 2 location: " + truck2.location.data + ", mileage: {:0.2f}".format(truck2.mileage))
    print("Total mileage: {:0.2f}".format(truck1.mileage + truck2.mileage))
