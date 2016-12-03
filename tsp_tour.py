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
    dx = abs(a['x'] - b['x'])
    dy = abs(a['y'] - b['y'])

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

# Optimize the calculated tour
# tour - dictionary with the tour in order
#

def optimize( tour, tourWeight, timeLimit):
    tourArray = []
    i = 0
    for k in tour:
        tourArray.append(tour.get(k))
        i += 1

    for j in tourArray:
        print(j)
    print(calcTour(tourArray) == tourWeight)
    print("==== optimize ====")

    oldWeight = tourWeight
    newWeight = 0
    found = False

    curTime = time.time()
    endTime = curTime + timeLimit

    #while(time.time() < endTime):
    while(True):
        raw_input("Press Enter to Continue")

        print("=====Back at top======")
        # find two edges that do not share a vertex
        # choose a random index u <= len(tour)
        print("obtaining random u value")
        u = random.randrange(0, len(tour) - 1)
        if u + 1 >= len(tour):
            v = 0
        else:
            v = u + 1

        edgeA = {'u': u,'v': v}
        print("obtaining random j value")
        j = random.randint(0, len(tour) - 1)

        #print("u: {0}, v: {1}".format(u, v))


        # find another pair of adjacent indices in tour with distinct vertices
        while(found == False):

            #print("j: {0}, edgeA.u: {1}, edgeA.v: {2}".format(j, edgeA['u'], edgeA['v']))
            #print("a: {0}, b: {1}".format(tour[edgeA['u']], tour[edgeA['v']]))

            if (j+1 >= len(tour)):
                print("In if where j+1 is greater than length")
                if (j == edgeA['u'] or j == edgeA['v'] or 0 == edgeA['u'] or 0 == edgeA['v']):
                    print("rerolling j")
                    j = random.randint(0, len(tour) - 1)
                else:
                    found = True
            else:
                print("in if where j+1 is less than length")
                if (j == edgeA['u'] or j == edgeA['v'] or j+1 == edgeA['u'] or j+1 == edgeA['v']):
                    print("rerolling J")
                    j = random.randint(0, len(tour) - 1)
                else:
                    found = True

            if (j+1 >= len(tour)):
                k = 0
            else:
                k = j+1


        edgeB = {'j': j, 'k': k}
        # get the distance of each edge and subtract from the total
#        print("Values found at tour[edgeA['u']], tour[edgeB['v']]: {0} {1}".format(tour[edgeA['u']], tour[edgeA['v']]))
#        distA = distance(tourArray[edgeA['u']], tourArray[edgeA['v']])
#        distB = distance(tourArray[edgeB['j']], tourArray[edgeB['k']])

#        print("before swap")
#        print("a: {0}, b: {1}".format(tour[edgeA['u']], tour[edgeA['v']]))
#        print("c: {0}, d: {1}".format(tour[edgeB['j']], tour[edgeB['k']]))

#        print("oldWeight: {0}, newWeight{1}".format(oldWeight, newWeight))
#        print("distA: {0}, distb: {1}".format(distA, distB))

#        newWeight = oldWeight - (distA + distB)


        # swapping the values of the indices rearrances the order of the tour
        # this effectively creates new edges between the adjacent indices
#        temp = tourArray[edgeB['k']]
#        tourArray[edgeB['k']] = tourArray[edgeA['v']]
#        tourArray[edgeA['v']] = temp
        newTourArr = swap(edgeA, edgeB, tourArray)
        newTourArrWeight = calcTour(newTourArr)
        print("Old Tour Length: {0}, New Tour Length: {1}".format(oldWeight, newTourArrWeight))
        if newTourArrWeight < oldWeight:
            print("Replacing old tour with new found tour, and oldWeight with our new weight")
            tourArray = newTourArr
            oldWeight = newTourArrWeight



#        print("after swap")
#        print("a: {0}, b: {1}".format(tourArray[edgeA['u']], tourArray[edgeA['v']]))
#        print("c: {0}, d: {1}".format(tourArray[edgeB['j']], tourArray[edgeB['k']]))

        # get the distance of our new edges

#        newDistA = distance(tourArray[edgeA['u']], tourArray[edgeA['v']])
#        newDistB = distance(tourArray[edgeB['j']], tourArray[edgeB['k']])

#        print("newDistA: {0}, newDistB: {1}".format(newDistA, newDistB))


        # add these distances to our newWeight
#        newWeight = newWeight + newDistA + newDistB
#        print("does newWeight = actual weight: {0}".format(calcTour(tourArray) == newWeight))
#        print("Removed Edges Total: {0},  New Edge Total: {1}".format(distA+distB, newDistA+newDistB))
#        print("oldweight: {0}, newweight: {1}".format(oldWeight, newWeight))
        # if the tour is longer, revert the swap
#        if (newWeight >= oldWeight):
#            print("Swapping back")
#            temp = tourArray[edgeB['k']]
#            tourArray[edgeB['k']] = tourArray[edgeA['v']]
#            tourArray[edgeA['v']] = temp
            #print("a: {0}, b: {1}".format(tourArray[edgeA['u']], tourArray[edgeA['v']]))
            #print("c: {0}, d: {1}".format(tourArray[edgeB['j']], tourArray[edgeB['k']]))
#           print("Checking to make sure our weight stayed the same: {0}".format(calcTour(tourArray) == oldWeight))


#        else:
#            oldWeight = newWeight
#            print("New Tour: {0}".format(tourArray))
#            print("What we say is the new weight: {0},  Actual: {1}".format(oldWeight, calcTour(tourArray)))

        found = False
#TODO load tourArray back into a dictionary
    return (tour, oldWeight)

def swap(a, b, tour):
    newTour = [];
    for i in range(0, a['u']+1):
        newTour.append(tour[i])

    for k in range(b['j'], a['v']-1, -1):
        newTour.append(tour[k])

    for j in range(b['j']+1, len(tour)):
        newTour.append(tour[j])
    return newTour

def calcTour(arr):
    total = 0
    i = 0
    while i < len(arr)-1:
        pointA = arr[i]
        pointB = arr[i+1]
        total += distance(pointA, pointB)
        i += 1
    total += distance(arr[len(arr)-1],arr[0])
    return total

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
    optimizedTour = optimize( nearestNeighbors[0], nearestNeighbors[1], 1)

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
