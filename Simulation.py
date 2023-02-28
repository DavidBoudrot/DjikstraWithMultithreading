
import time as t

import threading
class Simulation:
    all_packages = []
    totalmiles = 0
    packsdelivered = 0
    trucks = []
    time = "8:00"
    def __init__(self, trucks, all_packages):
        self.trucks = trucks
        self.totalmiles = 0
        self.all_packages = all_packages



    #This is where the simulation will run
    #I will need to loop through each each package in each truck
    import multiprocessing


    def run_simulation(self):
        input("Press Enter to start the simulation")

        truck1 = self.trucks[0].current_packages
        truck2 = self.trucks[1].current_packages
        truck3 = self.trucks[2].current_packages

        # So this just leaves us with one problem.
        # If we just run the simulation on two different threads like this, the order we deliver the packages will not make sense.
        # Truck1 might deliver a package at 9:00 and then truck2 could deliver a package at 8:30 right after.
        # This is not how the simulation should be, that is not how the real world works.
        # I fixed this by running a seperate algorithm that will get the times for each package first, then we can continue with the simulation.
        # Only difference will be that now we have a list of packages with their delivery times and can just loop through them in order.


        thread1 = threading.Thread(target=self.deliver_packages, args=(self.trucks[0], "1"))
        thread2 = threading.Thread(target=self.deliver_packages, args=(self.trucks[1], "2"))
        thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3"))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        while thread1.is_alive() and thread2.is_alive():
            continue
        thread3.start()
        thread3.join()

    #Once one of the threads is done I can start the next one
    # I'm going to use the threading module to run the simulation on two different threads
     # This is super overly complicated and chaotic but I wanted to embrace a challenge for the sake of learning.
    # If I was not crazy I would have just looped through both truck 1 and truck 2 in the same method.

    # Okay so here is the deliver_packages method that will run on two different threads.
    # It will deliver the packages for truck 1 and truck 2.

    def deliver_packages(self, truck, truckID):
        for package in truck.get_current_packages().get_path():
            package.setDeliveryStatus("En Route")
        done = False
        for package in truck.get_current_packages().get_path():
            if not self.packsdelivered == 40:
                # Get the time for the other truck
                # If the time is less than the current time, then we need to wait until the other truck is done

                if truckID == "1":
                    truckTimeInt = self.parseTime(truck)
                    truck2TimeInt = self.parseTime(self.trucks[1])
                    while truckTimeInt > truck2TimeInt:
                        truckTimeInt = self.parseTime(truck)
                        truck2TimeInt = self.parseTime(self.trucks[1])
                        # If the time for truck 1 is greater than the time for truck 2, then we need to wait until truck 1 is done

                if truckID == "2":
                    print(truck.time)
                    # Here I have to parse the ints from the string and determine if the time is greater than the other truck
                    # If it is, then we need to wait until the other truck is done
                    truckTimeInt = self.parseTime(truck)
                    truck2TimeInt = self.parseTime(self.trucks[0])

                    print(truck2TimeInt)
                    while truckTimeInt > truck2TimeInt:
                        truckTimeInt = self.parseTime(truck)
                        truck2TimeInt = self.parseTime(self.trucks[0])

                        # If the time for truck 1 is greater than the time for truck 2, then we need to wait until truck 1 is done
                print(f"Delivering {package.package_id} on truck {truckID}")
                package.timestamp = truck.time
                print(f"Delivered at {str(truck.time)}")
                package.delivery_status = "Delivered"
                self.packsdelivered += 1
                # Set current package to prev and set next package to current if there is another.
                # After that increment the time with the difference
                prev = package
                if truck.get_current_packages().get_path().index(package) + 1 < len(
                        truck.get_current_packages().get_path()):
                    current = truck.get_current_packages().get_path()[
                        truck.get_current_packages().get_path().index(package) + 1]
                else:
                    print(f"That's it for truck {truckID}\nPackages delivered: {str(self.packsdelivered)}")
                    break
                print(current)
                truck = self.increment_time(prev, current, truck)
                print(f"Next package at for {str(truckID)} will arrive at {str(truck.time)}")
                print(f"Packages delivered: {str(self.packsdelivered)}")
                i = input("Press Enter to continue or enter I for stats")
                if i == "I":
                    self.lookupStats()
            else:
                print("All done")
                break

    # To parse the ints for the format of HH:MM or H:MM I will use the following if statements
    # This gives us the minute of the day for the time of the truck
    # the way Ill do this is by determining the time in minutes
    # 12:00 am aka 0:00 is 0 minutes
    # 12:01 am aka 0:01 is 1 minute
    def parseTime(self, truck):
        minutesTens = 0
        minutesOnes = 0
        hours = truck.time[0]
        if truck.time[1] == ":":  # This will tell us that the format is H:MM
            hours = int(truck.time[0]) * 60
            minutes = int(truck.time[2]) * 10 + int(truck.time[3])
        elif truck.time[2] == ":":  # This will tell us that the format is HH:MM
            hours = int(truck.time[0]) * 600 + int(truck.time[1]) * 60
            minutes = truck.time[3] * 10 + truck.time[4]
        return hours + minutes
    #time is a string that we will be adding to
    #prev is the previous package that was delivered last
    #current is the current package that is going to be delivered
    #we need to add the time it takes to deliver the package to the time
    def increment_time(self, prev, current, truck):
        ints = truck.time.split(":")
        hour = int(ints[0])
        minute = int(ints[1])
        x = range(0, int(prev.get_distance(current)), 1)  # 18 mph
        self.totalmiles += int(prev.get_distance(current))
        for mile in x:
            if x == 0:
                continue
            else:
                minute += 6 # add 6 minutes since it takes 6 minutes to travel 1 mile at 18 mph
                if minute >= 60:
                    hour += 1
                    minute -= 60
                if hour > 12:
                    hour -= 12
        if minute >= 10:
            truck.time = str(hour) + ":" + str(minute)
            return truck
        else :
            truck.time = str(hour) + ":0" + str(minute)
            return truck


    def lookupStats(self):
        print("What would you like to lookup by?")
        print("1. Package ID")
        print("2. Delivery Address")
        print("3. Delivery Deadline")
        print("4. Delivery City")
        print("5. Delivery Zip Code")
        print("6. Package Weight")
        print("7. Delivery Status")
        print("8. Back to Simulation")
        i = input()
        if i == "1":
            search_results = []
            print("Enter Package ID")
            i = input()
            found = False
            for package in self.all_packages:
                if package.package_id == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()

        elif i == "2":
            search_results = []
            print("Enter Delivery Address")
            i = input()
            for package in self.all_packages:
                if package.address == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()


        elif i == "3":
            search_results = []
            print("Enter Delivery Deadline")
            print("HH:MM")
            i = input()
            for package in self.all_packages:
                if package.deadline == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()




        elif i == "4":
            search_results = []
            print("Enter Delivery City")
            i = input()
            for package in self.all_packages:
                if package.city == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()


        elif i == "5":
            search_results = []
            print("Enter Delivery Zip Code")
            i = input()
            for package in self.all_packages:
                if package.zip_code == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()


        elif i == "6":
            search_results = []
            print("Enter Package Weight")
            i = input()
            search_results = []
            found = False
            for package in self.all_packages:
                if package.weight == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()


        elif i == "7":
            search_results = []
            print("Enter Delivery Status")
            i = input()
            for package in self.all_packages:
                if package.delivery_status == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()


        elif i == "8":
            return
        else:
            print("Invalid input")
            input("Press enter to continue")
            self.lookupStats()


















