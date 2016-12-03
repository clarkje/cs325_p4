# Caleigh Runge-Hottman, Andrew Kittrell, Jeromie Clark
# CS325 - Project 4
# Traveling Salesman Problem Solver

from __future__ import print_function
import copy
import sys
import re
import time
import math
import random
import collections

# adapted from tsp-verifier.py
# expects a dictionary item with the city id as the first element, and a dictionary of x, y as the second element

def distance(a,b):

    #print("distance: a:{0} b:{1}".format(a,b))

    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    dx = a['x'] - b['x']
    dy = a['y'] - b['y']

    #print("dx: {0}, dy: {1}".format(dx, dy))
    return int(math.sqrt(dx*dx + dy*dy)+0.5)


# borrowed from tsp-verifier.py
def readCities(inputFile):

    f = open(inputFile,'r')
    line = f.readline()
    cities = {}
    while len(line) > 1:
        lineparse = re.findall(r'[^,;\s]+', line)
        cities[int(lineparse[0])]={'x': int(lineparse[1]), 'y': int(lineparse[2]), 'id': int(lineparse[0])}
        line = f.readline()
    f.close()
    return cities

def nearestNeighbor(unvisited):
    visited = collections.OrderedDict()
    current = unvisited.get(0)
    first = unvisited.get(0)
    tourLen = 0

    while len(unvisited) > 1:
        #pop a vertex off the graph
        current = unvisited.pop(current['id'])
        #add it to the visisted list
        visited[current['id']] = current
        # find the nearest unvisited vertex and its distance
        nearest = findClosest(current, copy.deepcopy(unvisited))
        # add the distance between the current node and nearest node to total tour length
        if (nearest[0] < sys.maxint):
            tourLen += nearest[0]
        # the new current node is now the node that was previously the nearest node
        current = nearest[1]

    visited[current['id']] = current
    tourLen += distance(current, first)
    unvisited.pop(current['id'])
    return (visited, tourLen)

def findClosest( current, unvisited ):

    # the distance of the closest vertex
    closestDist = sys.maxint
    # the index of the closest node
    closestVertex = {}

    for vertex in unvisited:

        #HACK: This is odd... instead of getting the vertex and tuple as vertex, I just get its index
        #I'm effectively just constructing the object I expected with get() from the parent dict...
        v = unvisited.get(vertex)

        dist = distance(current, v)
        if dist < closestDist:
            closestDist = dist
            closestVertex = v
    return (closestDist, closestVertex)

# Reverse the order of a subset of the tour
def doSwap( tourList, startSwap, endSwap ):
    newList = []
    toInvert = []
    for x in range(0, startSwap):
        newList.append(tourList[x])

    for x in range(startSwap, endSwap):
        toInvert.append(tourList[x])

    toInvert.reverse()
    for x in range(0, len(toInvert)):
        newList.append(toInvert[x])

    for x in range(endSwap, len(tourList)):
        newList.append(tourList[x])

    return newList


def calculateTourLength(tour):

    newTour = 0

    for i in range(0,len(tour)-1):
        if(i < len(tour)-1):
            newTour += distance(tour[i][1], tour[i+1][1])
    newTour += distance(tour[len(tour)-1][1], tour[0][1])

    return newTour

# Optimize the calculated tour
# tour - dictionary with the tour in order
# after much struggle, referenced pseudocode at https://en.wikipedia.org/wiki/2-opt
def optimize( tour, tourWeight, timeLimit):

    # Convert our dict to a list because it's easier to work with here
    tourList = []
    for x in range(0,len(tour)):
        item = tour.popitem
        tourList.append(tour.popitem())
    tourList.reverse()

    oldWeight = tourWeight
    newWeight = 0
    found = False

    curTime = time.time()
    endTime = curTime + timeLimit

    #for x in range(0,100):
    while(time.time() < endTime):

        # We exclude the first node because it's our origin and terminus
        startSwap = random.randrange(1, len(tourList) - 1)
        #endSwap = random.randrange(startSwap, len(tourList) - 1)
        if(startSwap < len(tourList) - 1):
            endSwap = startSwap + 1
        else:
            startSwap = 1
            endSwap = random.randrange(2, len(tourList) - 1)

        newTourList = doSwap( tourList, startSwap, endSwap)

        newTourWeight = calculateTourLength(newTourList)

        if newTourWeight < oldWeight:
            tourList = newTourList
            oldWeight = newTourWeight

    return (tourList, oldWeight)


def main():

    # The first commandline option is the input file
    inputFile = sys.argv[1]
    outputFile = sys.argv[1] + ".tour"

    # A dictionary of cities and their coordinates
    cities = readCities(inputFile)

    # Calculate Tour
    nearestNeighbors = nearestNeighbor(cities)

    print("=== nearestNeighbors ===")
    print(nearestNeighbors[0])
    print(nearestNeighbors[1])

    # Optimize Tour
    optimizedTour = optimize( nearestNeighbors[0], nearestNeighbors[1], 178)

    print("=== optimized ===")
    print(optimizedTour[0])
    print(optimizedTour[1])

    #writeResults(outputFile, nearestNeighbors[0], nearestNeighbors[1])
    writeResults(outputFile, optimizedTour[0], optimizedTour[1])


def writeResults(outputFile, cities, totalDistance):

    # open for writing, clears existing file
    outFile = open(outputFile, 'w')

    # TODO: Calculate total tour distance
    print(totalDistance, file=outFile)
    print(totalDistance)

    # Print the City IDs of the tour
    for city in cities:
        #print("{0} {1} {2}".format(city, cities[city]["x"], cities[city]["y"]))
        print(city[0], file=outFile)
        print(city)



if __name__ == "__main__":
    main()
