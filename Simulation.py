
import time as t

import threading
from datetime import timedelta, datetime, time
class Simulation:
    all_packages = []
    totalmiles = 0
    packsdelivered = 0
    trucks = []
    time = "8:00"   # Mutex that will be used to keep track of the time
                    # Only one thread can access this at a time
                    # The thread will say; Hey I'm going to access the time now
                    # If a different thread is already accessing the time, it will wait until the other thread is done
                    # If a thread is accessing the time and it wants to deliver a package that has a delivery time after
                    # the current time, it will pass and give time access to another thread.


    thread1 = None
    thread2 = None
    thread3 = None
    thread4 = None
    reloaded = False
    truck2Started = False
    i = 0
    def __init__(self, trucks, all_packages):
        self.trucks = trucks
        self.totalmiles = 0
        self.all_packages = all_packages
    #This is where the simulation will run
    def run_simulation(self):
        # Create a lock for synchronizing thread access
        lock = threading.Lock()
        self.time = datetime.strptime("8:00", '%H:%M')
        packages = self.trucks[0].get_current_packages().get_path()
        print(len(packages))
        packages = self.trucks[1].get_current_packages().get_path()
        print(len(packages))
        packages = self.trucks[2].get_current_packages().get_path()
        print(len(packages))
        packages = self.trucks[3].get_current_packages().get_path()
        print(len(packages))

        # Wait for user input to start the simulation
        input("Press Enter to start the simulation")
        # Start the delivery threads for trucks 1 and 2
        self.thread1 = threading.Thread(target=self.deliver_packages, args=(self.trucks[0], "1", lock))
        self.thread2 = threading.Thread(target=self.deliver_packages, args=(self.trucks[1], "2", lock))
        self.thread3 = threading.Thread(target=self.deliver_packages, args=(self.trucks[2], "3", lock))
        self.thread4 = threading.Thread(target=self.deliver_packages, args=(self.trucks[3], "4", lock))


        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()


        self.thread1.join()
        self.thread3.join()
        self.thread2.join()
        self.thread4.join()
    def deliver_packages(self, truck, truckID, lock):
        if truckID == "3":
            truck.time = self.time
        if truckID == "2":
            self.truck2Started = True


        while truck.time > self.time:
            # self.time will be the time of the last delivery.
            # If the current truck's time is greater than the last delivery time, it means that the truck will have to wait to deliver.

            if not self.truck2Started:
                print("Detected a freeze in threads due to only 1 thread running and waiting")
                print("Force starting thread 2")
                self.thread2.start()
            continue
        packages = truck.get_current_packages().get_path()

        # Setting the packages status to en route
        for package in packages:
            package.setDeliveryStatus("En Route")

        # Delivering the packages
        for i, package in enumerate(packages):
            with lock:
                self.print_package_info(package, truck)
                package.delivery_status = "Delivered"
                package.timestamp = truck.time
                self.packsdelivered += 1
                # Check if next package is ready to be delivered
                if i + 1 < len(packages):
                    # If there is another package to deliver increment the time
                    next_package = packages[i + 1]
                    truck = self.increment_time(package, next_package, truck)
                else:
                    # No more packages to deliver
                    print(f"That's it for truck {truckID}\nPackages delivered: {str(self.packsdelivered)}")
                    return
    def print_package_info(self, package, truck):
        delivery_time_str = truck.time.strftime("%I:%M %p")
        print(f"Package {package.package_id} Delivered at {delivery_time_str} on truck {truck.truck_id} to {package.address}")
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
        self.time = truck.time
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


















