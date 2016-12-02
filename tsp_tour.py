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
    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    dx = a['x'] - b['x']
    dy = a['y'] - b['y']
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

# Optimize the calculated tour
# tour - dictionary with the tour in order
#

def optimize( tour, tourWeight, timeLimit):
    oldWeight = tourWeight
    newWeight = 0
    found = False

    curTime = time.time()
    endTime = curTime + timeLimit

    while(time.time() < endTime):
        # find two edges that do not share a vertex
        # choose a random index u <= len(tour)
        u = random.randrange(0, len(tour))
        if u + 1 > len(tour):
            v = tour[0]
        else:
            v = u + 1

        edgeA = {'u': u,'v': v}

        j = random.randrange(0, len(tour) - 1)

        # find another pair of adjacent indices in tour with distinct vertices
        while(found == False):
            if (j+1 >= len(tour)):
                if (j == edgeA['u'] or j == edgeA['v'] or 0 == edgeA['u'] or 0 == edgeA['v']):
                    j = random.randrange(0, len(tour) - 1)
                else:
                    found = True
            else:
                if (j == edgeA['u'] or j == edgeA['v'] or j+1 == edgeA['u'] or j+1 == edgeA['v']):
                    j = random.randrange(0, len(tour) - 1)
                else:
                    found = True

            if (j+1 >= len(tour)):
                k = tour[0]
            else:
                k = j+1

            edgeB = {'j': j, 'k': k}

            # get the distance of each edge and subtract from the total
            distA = distance(tour[edgeA['u']], tour[edgeA['v']])
            distB = distance(tour[edgeB['j']], tour[edgeB['k']])
            newWeight = oldWeight - (distA + distB)

            # swapping the values of the indices rearrances the order of the tour
            # this effectively creates new edges between the adjacent indices
            temp = tour[v]
            tour[k] = tour[v]
            tour[v] = temp

            # get the distance of our new edges

            newDistA = distance(tour[edgeA['u']], tour[edgeA['v']])
            newDistB = distance(tour[edgeB['j']], tour[edgeB['k']])

            # add these distances to our newWeight
            newWeight = newWeight + newDistA + newDistB

            # if the tour is longer, revert the swap
            if (newWeight > oldWeight):
                temp = tour[v]
                tour[k] = tour[v]
                tour[v] = temp
            else:
                oldWeight = newWeight

    return (tour, newWeight)


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
    optimizedTour = optimize( nearestNeighbors[0], nearestNeighbors[1], 179)

    print("=== optimized ===")
    print(optimizedTour[0])
    print(optimizedTour[1])

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
        print(city, file=outFile)
        print(city)



if __name__ == "__main__":
    main()
