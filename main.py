import csv

import Djikstra
import Package
import Truck
from Simulation import Simulation


def create_packages():
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        all_packages = []
        packages = []
        for line in reader:
            package = Package.Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
            packages.append(package)
            all_packages.append(package)
        #so this gives a list of packages that need to be delivered.
        #now I just have to order them in an efficient way that will allow me to deliver them all in the least amount of time
        #For my submission I will be creating a weighted graph that will use djiikstra's algorithm to find the shortest path between all the packages
        #Im gonna start by loading up the packages without any special notes

    truck1 = []
    truck2 = []
    truck3 = []
    truck1Reload = []
    trucks = [truck1, truck2, truck3, truck1Reload]
    removed = []
    i = -1

    for package in packages:
        # Truck 1 leaving at 8:00
        if package.package_id == '13': # This package has to be with 13 15 14 and 19
            truck1.append(package)
        elif package.package_id == '14': # This package has to be with 13 15 14 and 19
            truck1.append(package)
        elif package.package_id == '15': # This package has to be with 13 15 14 and 19
            truck1.append(package)
        elif package.package_id == '19': # This package has to be with 13 15 14 and 19
            truck1.append(package)
        #Truck 2 leaving at 9:05
        elif package.package_id == '28': #This package arrives at the hub at 9:05
            truck2.append(package)
        elif package.package_id == '32': #This package arrives at the hub at 9:05
            truck2.append(package)
        elif package.package_id == '6': #This package arrives at the hub at 9:05
            truck2.append(package)
        elif package.package_id == '25': #This package arrives at the hub at 9:05
            truck2.append(package)
        elif package.package_id == '30': #This package arrives at the hub at 9:05
            truck2.append(package)
        elif package.package_id == '3': #This package has to be on truck 2
            truck2.append(package)
        elif package.package_id == '18': #This package has to be on truck 2
            truck2.append(package)
        elif package.package_id == '36': #This package has to be on truck 2
            truck2.append(package)
        elif package.package_id == '38': #This package has to be on truck 2
            truck2.append(package)
        elif package.deadline != 'EOD':
            truck2.append(package)
        else:
            if int(package.package_id) % 2 == 0:
                truck1Reload.append(package)
            else:
                truck3.append(package)



    # Now I will use Djikstra's algorithm to find the shortest path between all the packages
    # I have created a class that will do this for me


    packagesForTruck1 = []
    packagesForTruck2 = []
    packagesForTruck3 = []

    packagesForTruck1 = Djikstra.Djikstra(trucks[0])
    truck1Obj = Truck.Truck(1, packagesForTruck1)
    packagesForTruck2 = Djikstra.Djikstra(trucks[1])
    truck2Obj = Truck.Truck(2, packagesForTruck2)
    packagesForTruck3 = Djikstra.Djikstra(trucks[2])
    truck3Obj = Truck.Truck(3, packagesForTruck3)
    truck1ReloadObj = Truck.Truck(1, trucks[3])



    #Okay so thats our path for each truck
    #Now I need to instantiate the actual trucks objects and add the packages to them



    truckObjects = [truck1Obj, truck2Obj, truck3Obj, truck1ReloadObj]

    #Now I need to instantiate the simulation object and run the simulation
    sim = Simulation(truckObjects, all_packages)
    sim.run_simulation()

create_packages()




