#WGU Data Structures and Algorithms II
from datetime import datetime


class Truck:

    truck_id = 0
    current_packages = []
    time = None

    def __init__(self, truck_id, start_time, current_packages):
        self.truck_id = truck_id
        self.current_packages = current_packages
        self.time = datetime.strptime(start_time, '%H:%M')
    def get_current_packages(self):
        return self.current_packages
