import csv
import datetime

from Djikstra import Djikstra


class Package:
    package_id = ""
    address = ""
    city = ""
    state = ""
    zip_code = ""
    deadline = ""
    weight = ""
    timestamp = datetime.datetime.now()
    special_notes = ""
    delivery_status = ""

    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = "At Hub"
    def __str__(self):
        return "Package ID: " + self.package_id + "\n" + "Address: " + self.address + "\n" + "City: " + self.city + "\n" + "State: " + self.state + "\n" + "Zip Code: " + self.zip_code + "\n" + "Deadline: " + self.deadline + "\n" + "Weight: " + self.weight + "\n" + "Special Notes: " + self.special_notes + "\n" + "Delivery Status: " + self.delivery_status + "\n"

    def setDeliveryStatus(self, status):
        self.delivery_status = status


    def get_distance(self, package):

        with open('distance.csv', 'r') as csvfile:
            distancedata = csv.reader(csvfile)
            list_of_dist = list(distancedata)

        address_table = {}
        # This will create a dictionary that will have the address as the key and the index of the address as the value.
        with open('addresses.csv', 'r') as csvfile:
            addressdata = csv.reader(csvfile)
            addresses = []
            for line in addressdata:
                address_table[line[1]] = int(line[0])
                addresses.append(line[1])
                # dict = {'123 Street st' : 0}
                # addreses = ['123 Street st', ...]

        # This will be my method to get the distance between two addresses

        return float(list_of_dist[address_table[self.address]][address_table[package.address]])




