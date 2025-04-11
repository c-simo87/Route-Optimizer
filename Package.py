import csv
from Truck import *
from Distances import *
from HashTable import ChainingHashTable

pHash = ChainingHashTable()
createdPackages = []

class Package:
    #Default constructor
    #O(1)
    def __init__(self, id, address, city, state, zip, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status

    # Return values of package
    #->O(1)
    def values(self):
        return self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.state

    # Return the package values in string format instead of object memory address
    #->O(1)
    def __str__(self):
        return "ID:%s, Delivery Address:%s, %s, %s, %s,Delivery Time:%s,Weight:%s,Status:%s" % (
        self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.status)

    #Return the address of the package
    #O(1)
    def getAddress(self):
        return "%s"%(self.address)

    #This will convert the status string to time format
    #-> O(N^2) - uses minimizeDistance function
    def convertStatusTime(package):
        if package.status != 'En Route' or package.status != 'At Hub':
            status = package.status
            status = status.split("Delivered at ")[1]
            hour = int(status[0:2])
            minute = int(status[3:5])
            time1 = datetime.now()
            time1 = time1.replace(hour=hour, minute=minute)
            time1 = datetime.strftime(time1, '%I:%M %p')
            return time1
        return



    #Self.delivertime = none
    #method for time
    def setDeliveredTime(self,deliveredTime):
        self.status = "Delivered at " + str(deliveredTime)
        pHash.insert(self.id, self)

    #Return which truck the given package is on
    #->O(N)
    def getTruckLoaded(self):
        if self in truck1.inventory:
            return 1
        elif self in truck2.inventory:
            return 2
        elif self in truck3.inventory:
            return 3



#Load packages function
#Read the CSV file. Trucks are manually loaded on to the trucks given the constrains of the 'Status' of the package
#as well as a delivery deadline. Truck 1 will favor packages with a deadline of <= 10:30.
#Truck 2 will favor packages with delays at 9:05 and deadlines of 10:30a
#Truck 3 will favor packages that arive at 9:05 with EOD.
#-> O(N^2)
with open(r'packages.csv') as file:
    packageData = csv.reader(file, delimiter=',')
    truck1 = Truck("First Truck")
    truck2 = Truck("Second Truck")
    truck3 = Truck("Third Truck")
    truck1Packages = [1,13,14,16,19,20,29,30,31,34,37,40,15]
    truck2Packages = [3,6,18,25,28,32,36,38]
    truck3Packages = [9,28,32]

    for package in packageData:
        # print(package)
        id = int(package[0])
        address = package[1]
        city = package[2]
        state = package[3]
        zip = package[4]
        deadline = package[5]
        weight = package[6]
        # status = "None"
        try:
            status = package[7]
        except IndexError:
            status = 'At Hub'

        newPackage = Package(id, address, city, state, zip, deadline, weight, status)
        pHash.insert(id, newPackage)
        createdPackages.append(newPackage)

    #Determine which truck the package should be loaded on
    #Each For loop runs the integer list for each truck constraint
    #If that package ID number matches that list number, load it on the appropriate truck

    for i in truck1Packages:
        for j in createdPackages:
            if j.id == i:
                truck1.addPackage(j)
                createdPackages.remove(j)
    for i in truck2Packages:
        for j in createdPackages:
            if j.id == i:
                truck2.addPackage(j)
                createdPackages.remove(j)
    for i in truck3Packages:
        for j in createdPackages:
            if j.id == i:
                truck3.addPackage(j)
                createdPackages.remove(j)


    #For any left over packages that exceed the truck size or have a deadline, add them to the 3rd truck
    for i in createdPackages:
        if truck1.getTotalPackages() < 16:
            truck1.addPackage(i)
        elif len(truck2.inventory) < 16:
            truck2.addPackage(i)
        else:
            truck3.addPackage(i)


# This function prints the status of all packages by the requested time
# Determine which truck each package is on and determine when the departure time was on that truck
# Loop through each package on the truck and determine if the status must be set to either Delivered, En Route or At Hub
#->O(N)
def printTimeStatus(requestedTime):
    print('Requested package status time by: ', requestedTime)
    for i in range(1,41):
        package = pHash.search(i)
        packageTime = package.convertStatusTime()
        #Check if the requested time is less than the delayed packages
        if requestedTime[-2:] == 'AM' and (package.id == 6 or package.id == 25 or package.id == 28 or package.id == 32) and requestedTime < "09:05":
            # if (package.id == 6 or package.id == 25 or package.id == 28 or package.id == 32) and requestedTime < "09:05":
            package.status = "Delayed on flight---will not arrive to depot until 9:05 am"
        else:
            truck = package.getTruckLoaded()
            truckDepartureTime = datetime.now()
            if truck == 1:
                truckDepartureTime = truck1.departureTime
            elif truck == 2:
                truckDepartureTime = truck2.departureTime
            elif truck == 3:
                truckDepartureTime = truck3.departureTime
            truckDepartureTime = datetime.strftime(truckDepartureTime, '%I:%M:%S %p')
            #if the requested times am and pm are same
            if truckDepartureTime[-2:] == requestedTime[-2:]:
                # if the requested time is less than departure time, set at hub
                if requestedTime < truckDepartureTime:
                    package.status = "At Hub"
                # if the requested time is passed the departure time, check if its passed the delivered time
                elif requestedTime > truckDepartureTime:
                    if packageTime > requestedTime and packageTime[-2:] == requestedTime[-2:]:
                        package.status = "En Route"
    pHash.print()
