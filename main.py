###################
# C950 - Data Structure and Algorithms Package Delivery Assessment
# Created by Christopher Simonetti. ID# 001219556
###################

import time

from Package import *
from _datetime import *


#Converts the requested tim in hour and minute to a date time str object
#->O(1)
def getReqeustedTime():
    try:
        print('Enter the hour to search for (1-24)')
        reqHour = int(input())
        print('Enter the minute to search for (00-59)')
        reqMin = int(input())
        setTime = datetime.now()
        setTime = setTime.replace(hour=reqHour, minute=reqMin)
        setTime = datetime.strftime(setTime, '%I:%M %p')
        return setTime
    except Exception:
        print('The requested time you entered is not in valid format. Please enter again')

#Begins the truck deliveries and prints their total mileage to the screen
#->O(N^2)
def startDelivery():
    truck1.sortPackages()
    truck2.sortPackages()
    truck3.sortPackages()

    truck1.deliverPackages(8,0,0)
    truck2.deliverPackages(9,5,0)
    truck3.deliverPackages(10,20,0)
    total = truck1.totalDrivenMiles + truck2.totalDrivenMiles + truck3.totalDrivenMiles
    print("\nTotal Mileage between all trucks by end of day: ", '%.1f' % total)
    print()


startDelivery()
select = 0
#Main menu of the program
#Allows the user to select one of the 4 options to retrieve package information.
#Loop is exited upon selecting option 4.
while select != 4:
    select = 0
    print()
    print('Welcome to the WGU UPS Delivery UI. Please enter a selection')
    print('1- Search for an package')
    print('2- Print the status of all the packages at given time')
    print('3- Print the total miles driven by each truck at a given time')
    print('4- Quit program')
    select = int(input())
    if select == 1:
        print('\nPlease enter the package id number to look up: (1-40)')
        try:
            packageId = int(input())
        except:
            print('The package id you entered is invalid')
        print(pHash.search(packageId))
    elif select == 2:
        setTime = getReqeustedTime()
        print(setTime)
        try:
            printTimeStatus(setTime)
        except:
            print('The time you entered is invalid')
    elif select == 3:
        setTime = getReqeustedTime()
        try:
            print('Truck mileage status by time: ', setTime)
            truck1.printDistanceStatus(setTime)
            truck2.printDistanceStatus(setTime)
            truck3.printDistanceStatus(setTime)
        except:
            print('The time you entered is invalid')


