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
   # dx = a['x'] - b['x']
   # dy = a['y'] - b['y']
    dist = int(math.sqrt(math.pow((a['x'] - b['x']),2) + math.pow((a['y'] - b['y']),2))+0.5)
    #print("dx: {0}, dy: {1}".format(dx, dy))
    return dist


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


# Optimize the calculated tour
# tour - dictionary with the tour in order
#


def optimize( tour, tourWeight, timeLimit):

    print("==== optimize ====")

    # because we've just began, the best weight is the previous tours weight.
    bestTour = tourWeight
    # we have yet to find a new tour weight.
    newTour = 0
    # we haven't found any adjacent vertices, because we haven't looked.
    found = False
    # hold on to the # of vertices 0..last.
    numVertices = len(tour) - 1

    # time calcs.
    curTime = time.time()
    endTime = curTime + timeLimit

    # while we still have time...
    while(time.time() < endTime and bestTour > 0):
        # find two edges that do not share a vertex
        # choose a random index randVertIdx <= # vertices.
        u = random.randrange(0, numVertices)

        # if that index is the last index...
        if u == numVertices:
            # the adjacent vertex should be the first index instead.
            v = 0
        else:
            v = u + 1
        edgeA = {'u': u,'v': v}
        

        j = random.randrange(0, numVertices)
        # find another pair of adjacent indices in tour with distinct vertices
        while(found == False):
         # we don't want j or its adjacent vertex to be u or v.
            while (j == u or j == v or j+1 == u or j+1 == v or (j == numVertices and 0 == u) or (j == numVertices and 0 == v)):
                j = random.randrange(0, numVertices)

            if (j == numVertices):
                k = 0
                found = True
            else:
                k = j+1
                found = True
        edgeB = {'j': j, 'k': k}

        # swapping the values of the indices rearrances the order of the tour
        # this effectively creates new edges between the adjacent indices
        temp = tour[edgeB['k']]
        tour[edgeB['k']] = tour[edgeA['v']]
        tour[edgeA['v']] = temp

        newTour = 0
        for i in range(0,len(tour)-1):
            if(i < len(tour)-1):
                newTour += distance(tour[i], tour[i+1])
        newTour += distance(tour[len(tour)-1], tour[0])
        print ("temp tour: ", newTour)
        

        # if the tour is longer, revert the swap
        if (newTour > bestTour):
            print("New tour is greater. Best tour is still ", bestTour)
            temp = tour[edgeB['k']]
            tour[edgeB['k']] = tour[edgeA['v']]
            tour[edgeA['v']] = temp

        else:
            bestTour = newTour
            print("NEW BEST TOUR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        found = False

    return (tour, bestTour)


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
 #   writeResults(outputFile, nearestNeighbors[0], nearestNeighbors[1])



    # Optimize Tour
    optimizedTour = optimize( nearestNeighbors[0], nearestNeighbors[1], 5)

    print("=== optimized ===")
    print(optimizedTour[0])
    print(optimizedTour[1])

    writeResults(outputFile, optimizedTour[0], optimizedTour[1])

    print("Tour from NN: ",(nearestNeighbors[1]), " Tour from 2OPT: ", optimizedTour[1] )

def writeResults(outputFile, cities, totalDistance):

    # open for writing, clears existing file
    outFile = open(outputFile, 'w')

    # TODO: Calculate total tour distance
    print(totalDistance, file=outFile)
    print(totalDistance)

    # Print the City IDs of the tour
    for city in cities:
        #print("{0} {1} {2}".format(city, cities[city]["x"], cities[city]["y"]))
        print(city, file=outFile)
        print(city)



if __name__ == "__main__":
    main()
