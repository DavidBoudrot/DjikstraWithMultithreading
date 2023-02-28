import csv
import heapq

import hashtable





class Djikstra:
    address_table = None
    list_of_dist = None
    packages = []
    currentpath = []

    def get_path(self):
        return self.currentpath

    def __init__(self, packages):
        self.currentpath = []
        self.list_of_dist = None
        self.address_table = None
        self.packages = packages

        with open('distance.csv', 'r') as csvfile:
            distancedata = csv.reader(csvfile)
            list_of_dist = list(distancedata)
            #I hope its okay to use the list function here.

        address_table = hashtable.HashTable(1000)
        # This will create a dictionary that will have the address as the key and the index of the address as the value.
        with open('addresses.csv', 'r') as csvfile:
            addressdata = csv.reader(csvfile)
            addresses = []


            for line in addressdata:
                address_table.insert(line[1], int(line[0]))
                addresses.append(line[1])
                # dict = {'123 Street st' : 0}
                # addreses = ['123 Street st', ...]

        # This will be my method to get the distance between two addresses
        def get_distance(address1, address2):
            return float(list_of_dist[address_table.lookup(address1)][address_table.lookup(address2)])

        packages = self.packages
        paths = hashtable.HashTable(1000)
        # This will be a dictionary that will have the address as the key and the total cost as the value
        # The cheapest possible cost for each node will be tracked.
        start = packages[0]
        # Initialize the dictionary of costs with the starting node
        dictOfCosts = hashtable.HashTable(1000)
        # Loop until we've visited all nodes
        while len(packages) > 0:
            mincost = 1000000
            cheapestPackage = start
            # Loop through all the packages
            for package in packages:
                # Check if we have a cost for this package
                #check for key error here

                if not dictOfCosts.contains(package.address):
                    # If not, calculate the cost to get here
                    cost = float(get_distance(start.address, package.address))
                    dictOfCosts.insert(package.address, cost)

                else:
                    # If we do have a cost for this package, use it
                    cost = float(dictOfCosts.lookup(package.address))
                # Check if this package is cheaper than the current cheapest
                if cost < mincost:
                    mincost = cost
                    cheapestPackage = package

            # Add the cheapest package to the path
            if cheapestPackage:
                self.currentpath.append(cheapestPackage)
                packages.remove(cheapestPackage)
            # Remove the cheapest package from the list of unvisited packages
            # Update the costs for all the neighbors of the cheapest package
            for package in packages:
                # Calculate the cost to get from the cheapest package to this one
                cost = get_distance(cheapestPackage.address, package.address)
                total_cost = mincost + cost
                # Check if this is a new node or if we've found a shorter path
                if not dictOfCosts.contains(package.address) or total_cost < dictOfCosts.lookup(package.address):
                    dictOfCosts.insert(package.address, total_cost)
                    paths.insert(package.address, cheapestPackage.address)

            # Set the cheapest package as the starting point for the next iteration
            start = cheapestPackage

