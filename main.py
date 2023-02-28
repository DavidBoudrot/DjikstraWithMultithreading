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
    trucks = [truck1, truck2, truck3]
    removed = []
    i = -1
    for package in packages:

        if package.package_id == "15":
            trucks[0].append(package)
            continue

        elif package.package_id == "19":
            trucks[0].append(package)

        elif package.special_notes:
            continue
        else:
            if i < 2:
                i += 1



            else:
                i = 0
            trucks[i].append(package)
            removed.append(package)

    for package in removed:
        packages.remove(package)
    # That divided the packages into 3 trucks evenly
    # Now the packages with special notes need to be added to the trucks manually
    #This was my original plan but I later realized that some packages had to be delivered with other packages and sometimes said packages did not have special notes.
    # I added filters in the initial loop to remove the packages that had to be delivered with other packages but did not actually have notes.



    #package 1
    trucks[1].append(packages[0])
    packages.pop(0)

    #package 2
    trucks[2].append(packages[0])
    packages.pop(0)

    #package 3
    trucks[2].append(packages[0])
    packages.pop(0)

    #package 4
    trucks[0].append(packages[0])
    packages.pop(0)

    #package 5
    trucks[0].append(packages[0])
    packages.pop(0)

    #package 6
    trucks[0].append(packages[0])
    packages.pop(0)

    #package 7
    trucks[1].append(packages[0])
    packages.pop(0)

    #package 8
    trucks[2].append(packages[0])
    packages.pop(0)

    #package 9
    trucks[0].append(packages[0])
    packages.pop(0)

    #package 10
    trucks[2].append(packages[0])
    packages.pop(0)

    #package 11
    trucks[1].append(packages[0])
    packages.pop(0)

    #package 12

    trucks[1].append(packages[0])
    packages.pop(0)



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




    #Okay so thats our path for each truck
    #Now I need to instantiate the actual trucks objects and add the packages to them



    truckObjects = [truck1Obj, truck2Obj, truck3Obj]

    #Now I need to instantiate the simulation object and run the simulation
    sim = Simulation(truckObjects, all_packages)
    sim.run_simulation()

create_packages()




