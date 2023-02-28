
import time as t

import threading
class Simulation:
    all_packages = []
    totalmiles = 0
    packsdelivered = 1
    trucks = []
    time = "8:00"
    thread1 = None
    thread2 = None
    thread3 = None
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
        self.trucks[1].time = "9:05"
        truck3 = self.trucks[2].current_packages
        # So this just leaves us with one problem.
        # If we just run the simulation on two different threads like this, the order we deliver the packages will not make sense.
        # Truck1 might deliver a package at 9:00 and then truck2 could deliver a package at 8:30 right after.
        # This is not how the simulation should be, that is not how the real world works.
        # I made it so the truck package stores the time of its last delivery.
        # If the truck on the other thread is ahead of the current thread, it will wait until caught up.
        # This allows me to have threads running at the same time but still deliver the packages in the correct order.
        self.thread1 = threading.Thread(target=self.deliver_packages, args=(self.trucks[0], "1"))
        self.thread2 = threading.Thread(target=self.deliver_packages, args=(self.trucks[1], "2"))
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()

       #if thread 1 is still running, thread 3 will start when thread 1 is done
        while self.thread1.is_alive() and self.thread2.is_alive():
            continue

        #at this point a thread has died, so we need to check which one
        if self.thread1.is_alive():
            self.trucks[2].time = self.trucks[1].time
            self.thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3"))
        else:
            self.trucks[2].time = self.trucks[0].time
            self.thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3"))
        self.thread3.start()
        self.thread3.join()

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
            if not self.packsdelivered == 41:
                # Get the time for the other truck
                # If the time is less than the current time, then we need to wait until the other truck is done
                if truckID == "1" and self.thread2.is_alive():
                    truckTimeInt = self.parseTime(truck)
                    truck2TimeInt = self.parseTime(self.trucks[1])
                    while truckTimeInt > truck2TimeInt:
                        truckTimeInt = self.parseTime(truck)
                        truck2TimeInt = self.parseTime(self.trucks[1])
                        # If the time for truck 1 is greater than the time for truck 2, then we need to wait until truck 1 is done
                if truckID == "2" and self.thread1.is_alive():
                # Here I have to parse the ints from the string and determine if the time is greater than the other truck
                # If it is, then we need to wait until the other truck is done
                    truckTimeInt = self.parseTime(truck)
                    truck2TimeInt = self.parseTime(self.trucks[0])
                    while truckTimeInt > truck2TimeInt:
                        truckTimeInt = self.parseTime(truck)
                        truck2TimeInt = self.parseTime(self.trucks[0])
                package.timestamp = truck.time
                if truckID == "1":
                    print(
                        f"Package {str(package.package_id)} Delivered at {str(truck.time)} on truck {str(truckID)} to {package.address}")
                    print(f"Package ID: {str(package.package_id)}")
                    print(f"Special Notes: {package.special_notes}")
                    print(f"Deadline: {package.deadline}")
                    if package.deadline != "EOD":
                        deadline = self.parseTimeFromString(package.deadline)
                        time = self.parseTimeFromString(truck.time)
                        if deadline < time:
                            print("Package was late")
                    print(f"Packages delivered: {str(self.packsdelivered)}")
                elif truckID == "2":
                    print(
                        f"Package {str(package.package_id)} Delivered at {str(truck.time)} on truck {str(truckID)} to {package.address}")
                    print(f"Package ID: {str(package.package_id)}")
                    print(f"Special Notes: {package.special_notes}")
                    print(f"Deadline: {package.deadline}")
                    if package.deadline != "EOD":
                        deadline = self.parseTimeFromString(package.deadline)
                        time = self.parseTimeFromString(truck.time)
                        if deadline < time:
                            print("Package was late")
                    print(f"Packages delivered: {str(self.packsdelivered)}")
                if truckID == "3":
                    print(
                        f"Package {str(package.package_id)} Delivered at {str(truck.time)} on truck {str(truckID)} to {package.address}")
                    print(f"Package ID: {str(package.package_id)}")
                    print(f"Special Notes: {package.special_notes}")
                    print(f"Deadline: {package.deadline}")
                    if package.deadline != "EOD":
                        deadline = self.parseTimeFromString(package.deadline)
                        time = self.parseTimeFromString(truck.time)
                        if deadline < time:
                            print("Package was late")
                    print(f"Packages delivered: {str(self.packsdelivered)}")
                package.delivery_status = "Delivered"
                self.packsdelivered += 1
                # Set current package to prev and set next package to current if there is another.
                # After that increment the time with the difference
                prev = package
                if truck.get_current_packages().get_path().index(package) + 1 < len(
                        truck.get_current_packages().get_path()):
                    current = truck.get_current_packages().get_path()[
                        truck.get_current_packages().get_path().index(package) + 1]
                    truck = self.increment_time(prev, current, truck)
                else:
                    print(f"That's it for truck {truckID}\nPackages delivered: {str(self.packsdelivered)}")
                    if truckID == "1":
                        print("Reloading truck 1")
                        self.trucks[3].time = truck.time
                        self.trucks[0].current_packages = self.trucks[3].get_current_packages()
                        self.deliver_packages(self.trucks[1], "1")
                        continue
                    break
            else:
                print("All done")
                break
    # To parse the ints for the format of HH:MM or H:MM I will use the following if statements
    # This gives us the minute of the day for the time of the truck
    # the way Ill do this is by determining the time in minutes
    # 12:00 am aka 0:00 is 0 minutes
    # 12:01 am aka 0:01 is 1 minute
    def parseTime(self, truck):
        minutes = 0
        hours = int(truck.time.split(":")[0])
        minutes_str = truck.time.split(":")[1]
        if len(minutes_str) == 2:  # This will tell us that the format is HH:MM
            minutes = int(minutes_str)
            hours = hours * 60
        elif len(minutes_str) == 1:  # This will tell us that the format is H:MM
            minutes = int(minutes_str) * 10 + int(truck.time.split(":")[2])
            hours = hours * 60
        return hours + minutes

    def parseTimeFromString(self, time):
        minutes = 0
        hours = time[0]
        if time[1] == ":":  # This will tell us that the format is H:MM
            hours = int(time[0]) * 60
            minutes = int(time[2]) * 10 + int(time[3])
        elif time[2] == ":":  # This will tell us that the format is HH:MM
            hours = int(time[0]) * 600 + int(time[1]) * 60
            minutes = int(time[3]) * 10 + int(time[4])
        return hours + minutes



    #time is a string that we will be adding to.
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



# This is kinda messy I'm sorry for anyone reading this. I just hacked it together.
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


















