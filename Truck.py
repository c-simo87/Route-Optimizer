import csv
import datetime
import math

from math import *
from datetime import *
from HashTable import ChainingHashTable
from Package import *
from Distances import *


class Truck():
    #Defining constructed
    #-> O(1)
    def __init__(self, name):
        self.inventory = []
        self.name = name
        self.speed = 18
        self.mileage = 0
        self.departureTime = datetime.now()
        self.endTime = datetime.now()
        self.totalDrivenMiles = 0.0

    #Adds a package to the truck inventory
    #-> O(1)
    def addPackage(self,package):
        self.inventory.append(package)

    #Removed the package from the truck inventory
    #-> O(1)
    def removePackage(self, id):
        self.inventory = [i for i in self.inventory if i.id != id]

    #Get the total number of packages in the trucks inventory
    #-> O(1)
    def getTotalPackages(self):
        return len(self.inventory)

    #Print each of the packages within the truck inventory
    #-> O(N)
    def printPackages(self):
        print('==',self.name, " Packages==")
        for i in self.inventory:
            print(i)

    #Determine which of the packages has a timed deadline and if so, add it to a deadline list
    #->O(N)
    def getTimedPackages(self):
        d = []
        for i in self.inventory:
            if '10' in i.deadline or '9' in i.deadline:
                d.append(i)
        return d

    #Determine if the package has no time constraint and add it to a spearate list
    #->O(N)
    def getEODPackages(self):
        d = []
        for i in self.inventory:
            if i.deadline == 'EOD':
                d.append(i)
        return d

    #Sort the packages due to time constraints and then by distance
    #->O(N^2)
    def sortPackages(self):
        hub = addressList[0]
        priorityDelivery = self.getTimedPackages()
        if priorityDelivery:
            minimizeDistance(priorityDelivery)
        nonPriority = self.getEODPackages()
        minimizeDistance(nonPriority)
        self.inventory.clear()
        self.inventory = priorityDelivery + nonPriority

    # Return the packages address in the truck inventory
    # ->O(1)
    def getPackageAddress(self, index):
        return self.inventory[index].address


    #Function to deliver packages in the truck
    #First sort the packages in the truck to minimize the distance. Start from the hub and deliver all packages
    #Calculate the first package's distance from the hub and then loop through the inventory to calculate the distance
    #As well as tracking time for each delivery
    #->O(N)
    def deliverPackages(self,departHour,departMin,departSecond):
        self.sortPackages()
        self.departureTime = self.departureTime.replace(hour=departHour, minute=departMin, second=departSecond)
        totalDistance = totalDistanceFromHub(self.inventory)
        self.totalDrivenMiles = totalDistance
        totalMins = math.ceil(totalDistance*18 / 60 % 60)
        totalHours = math.floor(totalDistance/18)
        self.endTime = self.endTime.replace(hour = departHour + totalHours, minute= departMin+ totalMins)
        #keep track of the current time from departure and update the delivered time status
        currentTime = self.departureTime
        distance = addressDistance(addressList[0], self.getPackageAddress(0))
        currentTime = advanceTime(currentTime,distance)
        # print(currentTime)
        self.inventory[0].status = "Delivered at " + str(currentTime.strftime('%I:%M %p'))
        for i,package in enumerate(self.inventory):
            try:
                distance = addressDistance(package.getAddress(),self.inventory[i+1].getAddress())
                currentTime = advanceTime(currentTime,distance)
                self.inventory[i+1].status = "Delivered at " + str(currentTime.strftime('%I:%M %p'))
            except:
                pass

    #This function prints the total driven miles by the provided users time
    #It will first check if the requested time is before the departure time, which will return 0
    #A for loop will check if each status has been delivered and if so, it will advance time accordingly
    #Once the requested time has been surpassed, the function will return the total travelled distance at the requested time
    #-> O(N)
    def printDistanceStatus(self, requestedTime):
        totalDistance = 0.0
        departTime = datetime.now()
        departTime = self.departureTime
        strTime = self.departureTime.strftime('%I:%M %p')
        if requestedTime < strTime and requestedTime[-2:] == 'AM':
            print('\n', self.name, ' has traveled a total of ', "%.1f" % totalDistance, ' miles by ', requestedTime)
            return totalDistance

        departTime = advanceTime(departTime, 10)
        strTime = departTime.strftime('%I:%M %p')
        if strTime > requestedTime:
            pass
        for i,package in enumerate(self.inventory):
            try:
                distance = addressDistance(package.getAddress(),self.inventory[i+1].getAddress())
                totalDistance += distance
                departTime = advanceTime(departTime,distance)
                strTime = departTime.strftime('%I:%M %p')
                if strTime > requestedTime:
                    print('\n',self.name,' has traveled a total of ', "%.1f" % totalDistance, ' miles by ', requestedTime)
                    return totalDistance
            except:
                pass
        print('\n',self.name, ' has traveled a total of ', "%.1f" % totalDistance, ' miles by ', requestedTime)
        return totalDistance

