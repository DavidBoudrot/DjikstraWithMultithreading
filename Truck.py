#WGU Data Structures and Algorithms II
class Truck:

    truck_id = 0
    current_packages = []
    time = '8:00'


    def __init__(self, truck_id, current_packages):
        self.truck_id = truck_id
        self.current_packages = current_packages

    def get_current_packages(self):
        return self.current_packages
