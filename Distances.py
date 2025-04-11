import csv
from Package import *
from Truck import *
from datetime import *

distanceList = list()
addressList = list()

#Create a 2D list containing the list of distances from the CSV file
#-> O(N)
with open(r'Distance.csv') as file:
    distanceData = csv.reader(file, delimiter=',')
    for column in distanceData:
        #print(column)
        d = column
        distanceList.append(d)

#prints the list of distances
#O(N)
def printDistanceList():
    for row in distanceList:
        print(row)

#returns the distance in the distanceData list with the given indexes
# ->O(1)
def getDistance(row,column):
    totalDistance = float(distanceList[row][column])
    return totalDistance

#converts add1 and add2 into a upper string and searches the address list for the address
#returns distance between the two addresses
# -> O(N)
def addressDistance(add1,add2):
    a = 0
    b = 0
    for ad in addressList:
        if str.upper(str(add1)) in str.upper(str(ad)):
            a = addressList.index(ad)
            # print('Index of ', add1, ' ', a)
            break
    for ad in addressList:
        if str.upper(str(add2)) in str.upper(str(ad)):
            b = addressList.index(ad)
            # print('Index of ', add2, ' ', b)
            break
    if b > a:
        return getDistance(b,a)
    return getDistance(a,b)

#This function will return the total distance in miles from the truck packages
#-> O(N)
def totalPackageDistance(add, truckPackages):
    minDistance = 0.0

    for i,package in enumerate(truckPackages):
        if i == 0:
            minDistance += float(addressDistance(add,truckPackages[i+1].address))
        else:
            try:
                add1 = package.address
                add2 = truckPackages[i+1].address
                minDistance += float(addressDistance(add1,add2))
            except Exception:
                minDistance += 0.0
    return minDistance

#This function will return the total distance traveled from and to the hub
#-> O(N)
def totalDistanceFromHub(truckPackages):
    totalDistance = 0.0
    hub = addressList[0]
    totalDistance += addressDistance(hub, truckPackages[0])
    #print(add)
    for i,package in enumerate(truckPackages):
        try:
            totalDistance += addressDistance(package.address, truckPackages[i+1].address)
        except Exception:
            totalDistance += 0.0
    totalDistance += addressDistance(hub,truckPackages[-1])
    return totalDistance


#This function will calculate the total time to advance from the provided time
#->O(1)
def advanceTime(currentTime,miles):
    totalMins = math.ceil(miles/18 * 60)
    totalHours = math.floor(miles / 18)
    # currentTime = currentTime.replace(hour=currentTime.hour + totalHours, minute=currentTime.minute + totalMins)
    currentTime = currentTime + timedelta( minutes=totalMins, hours=totalHours)
    return currentTime


#Algorithm to determine the shortest path- Nearest Neighbor
#First, we declare a total variable to hold the total miles travelled, and a 'min' variable to keep track the shortest distanced compared in the below for loop
#The distance between the hub and the first package is calculated and is added to the total
#   Second, we loop through each of the packages on the truck:
#   Each package's distance within the first for loop is compared with all subsequent package's distance in the inner loop
#       If the current package's between the outer loop package and inner loop is less than the minimum variable, Set the minimum variable to the current variable and swap positions.
#   Increment the total variable with the recently searched minimum between packages
#Break the for loop when arriving at the last 2 packages.
#-> O(N^2)

def minimizeDistance(packages):
    total = 0.0
    total += addressDistance(addressList[0], packages[0])#Get the first package distance from the hub
    min = 999
    #current = 0.0
    for i, package in enumerate(packages):#Start a loop through each package
        try:
            for j, package2 in enumerate(packages):#Start a second loop to compare each subsequent package
                if(j>i):#If the index of the inner loop is greater than the outer loop index, begin the comparison
                    current = addressDistance(package.address, package2.address)#Set the current distance
                    if min > current:#If the minimum is less than the current, set min to the current and swap package positions
                        min = current
                        packages[i+1],packages[j] = packages[j],packages[i+1]
        except Exception:
            pass
        total += min
        if i < len(packages) - 2:
            min = 999




#Create a list of addresses extracted from the 'Address.csv' file
#->O(N)
with open(r'Addresses.csv') as file:
    addressData = csv.reader(file, delimiter=',')
    for row in addressData:
        addressList.append(row)


