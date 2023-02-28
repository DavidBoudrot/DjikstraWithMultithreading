
import time as t

import threading
from datetime import timedelta, datetime, time


class Simulation:
    all_packages = []
    totalmiles = 0
    packsdelivered = 1
    trucks = []
    time = "8:00"
    thread1 = None
    thread2 = None
    thread3 = None
    reloaded = False
    def __init__(self, trucks, all_packages):
        self.trucks = trucks
        self.totalmiles = 0
        self.all_packages = all_packages
    #This is where the simulation will run
    #I will need to loop through each each package in each truck
    import multiprocessing
    def run_simulation(self):
        # Create a lock for synchronizing thread access
        truck1 = self.trucks[0].current_packages
        for package in truck1.get_path():
            print(package.package_id)
        truck2 = self.trucks[1].current_packages
        for package in truck2.get_path():
            print(package.package_id)
        truck3 = self.trucks[2].current_packages
        for package in truck3.get_path():
            print(package.package_id)
        truck4 = self.trucks[3].current_packages
        for package in truck4.get_path():
            print(package.package_id)

        input("Press Enter to start the simulation")
        truck1 = self.trucks[0].current_packages
        truck2 = self.trucks[1].current_packages
        self.trucks[1].time = "9:05"
        truck3 = self.trucks[2].current_packages
        lock = threading.Lock()
        # Start the delivery threads
        self.thread1 = threading.Thread(target=self.deliver_packages, args=(self.trucks[0], "1", lock))
        self.thread2 = threading.Thread(target=self.deliver_packages, args=(self.trucks[1], "2", lock))
        self.thread1.start()
        self.thread2.start()

        # Wait for the threads to finish
        self.thread1.join()
        self.thread2.join()

        # Start the third delivery thread if necessary
        while self.thread1.is_alive() and self.thread2.is_alive():
            continue

        if self.thread1.is_alive():
            print("thread 2 died")
            self.trucks[2].time = self.trucks[1].time
            self.thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3", lock))
        else:
            print("thread 1 died")
            self.trucks[2].time = self.trucks[0].time
            self.thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3", lock))
        self.thread3.start()
        self.thread3.join()
        print("Simulation complete")

    #Once one of the threads is done I can start the next one
    # I'm going to use the threading module to run the simulation on two different threads
     # This is super overly complicated and chaotic but I wanted to embrace a challenge for the sake of learning.
    # If I was not crazy I would have just looped through both truck 1 and truck 2 in the same method.

    # Okay so here is the deliver_packages method that will run on two different threads.
    # It will deliver the packages for truck 1 and truck 2.
    def deliver_packages(self, truck, truckID, lock):
        packages = truck.get_current_packages().get_path()
        for package in packages:
            package.setDeliveryStatus("En Route")
        while len(packages) > 0:
            for package in packages:
                with lock:
                    self.print_package_info(package, truck)
                    package.delivery_status = "Delivered"
                    package.timestamp = truck.time
                    self.packsdelivered += 1
                    # Check if next package is ready to be delivered
                    index = packages.index(package)
                    if index + 1 < len(packages):
                        next_package = packages[index + 1]
                        truck = self.increment_time(package, next_package, truck)
                    else:
                        # No more packages to deliver
                        print(f"That's it for truck {truckID}\nPackages delivered: {str(self.packsdelivered)}")
                        if truckID == "1" and not self.reloaded:
                            truck = self.reload_truck(truck)
                            self.thread1 = threading.Thread(target=self.deliver_packages, args=(truck, "1", lock))
                            self.thread1.start()
                            self.thread1.join()
                        break
    def print_package_info(self, package, truck):
        delivery_time_str = truck.time.strftime("%I:%M %p")
        print(f"Package {package.package_id} Delivered at {delivery_time_str} on truck {truck} to {package.address}")
        print(f"Package ID: {package.package_id}")
        if package.special_notes:
            print(f"Special Notes: {package.special_notes}")
        # if package.deadline != "EOD":
        #     print(f"Deadline: {package.deadline}")
        #     print(f"Package was delivered at {delivery_time_str} on {truck.time.strftime('%m/%d/%Y')}")
        #
        #     if self.parseTimeFromString(package.deadline) < package.timestamp:
        #         print("Package was late")

    def reload_truck(self, truck):
        print("Reloading truck 1")
        self.trucks[0].time = truck.time
        self.trucks[0].current_packages = self.trucks[3].get_current_packages()
        self.reloaded = True

    def increment_time(self, prev, current, truck):
        speed = 18  # miles per hour
        distance = prev.get_distance(current)
        travel_time = timedelta(hours=distance/speed)
        truck.time += travel_time
        return truck

    def parseTimeFromString(self, time_str):
        datetime_obj = datetime.strptime(time_str, '%I:%M %p')
        return datetime_obj.strftime('%H:%M')

    def parseTime(self, time_str):
        datetime_obj = datetime.strptime(time_str, '%I:%M %p')
        return datetime_obj



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


















