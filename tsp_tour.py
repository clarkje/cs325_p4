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

#class Vertex:
#    def __init__(self, id, x, y):
#        self.id = id
#        self.x = x
#        self.y = y

# adapted from tsp-verifier.py
# expects a dictionary item with the city id as the first element, and a dictionary of x, y as the second element
def distance(a,b):
    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    print("-- distance --")
    print(a)
    print(b)
    dx = a['x'] - b['x']
    print(dx)
    dy = a[1]['y']-b[1]['y']
    return int(math.sqrt(dx*dx + dy*dy)+0.5) # equivalent to the next line
    #return int(round(math.sqrt(dx*dx + dy*dy)))

    return 1

# borrowed from tsp-verifier.py
def readCities(inputFile):

    f = open(inputFile,'r')
    line = f.readline()
    cities = {}
    while len(line) > 1:
        lineparse = re.findall(r'[^,;\s]+', line)
        #cities[int(lineparse[0])] = Vertex(int(lineparse[0]), int(lineparse[1]), int(lineparse[2]))
        cities[int(lineparse[0])]={'x': int(lineparse[1]), 'y': int(lineparse[2])}
        line = f.readline()
    f.close()
    return cities

def NearestNeighbor(unvisited):
    visited = {}
    first = unvisited[0]
    print("== nn ==")
    print(unvisited)

    while len(unvisited) > 0:
        #pop a vertex off the graph
        vertex = unvisited.popitem()
        #add it to the visisted list
        visited[vertex[0]] = vertex[1]
        # find the nearest unvisited vertex and its distance
        nearest = findClosest(vertex, copy.deepcopy(unvisited))
        # add the distance between the current node and nearest node to total tour length
        # tourLen += nearest
        # the new current node is now the node that was previously the nearest node
        print("-- nearest --")
        print(nearest)
        #print(nearest.id, nearest.x, nearest.y)

    return visited

def findClosest( current, unvisited ):

    print(" -- find closest -- ")
    print("unvisited")
    print(unvisited)

    # the distance of the closest vertex
    closestDist = 0
    # the index of the closest node
    closestNode = {}

    for vertex in unvisited:
        #HACK: This is odd... instead of getting the vertex and tuple as vertex, I just get its index
        #I'm effectively reconstructing it by assigning the whole node in the unvisisted dict
        v = {}
        v[vertex] = {'id': vertex, 'x': unvisited[vertex]['x'], 'y': unvisited[vertex]['y'] }
        c = {}
        c[current[0]] = {'id': current[0], 'x': current[1]['x'], 'y': current[1]['y']}
        dist = distance(c, v)
        if dist < closestDist:
            closestDist = dist
            closestVertex = vertex

    return (closestDist, closestNode)

def main():

    # The first commandline option is the input file
    inputFile = sys.argv[1]
    outputFile = sys.argv[1] + ".tour"

    # A dictionary of cities and their coordinates
    cities = readCities(inputFile)

    # TODO: Calculate Tour
    nearestNeighbors = NearestNeighbor(cities)

    #writeResults(outputFile, cities)


def writeResults(outputFile, cities):

    # open for writing, clears existing file
    outFile = open(outputFile, 'w')

    # first line in the file is the total distance of the tour
    totalDistance = 0;

    # TODO: Calculate total tour distance
    print(totalDistance, file=outFile)
    # TODO: Comment out (easier to look at output in console for debugging)
    print(totalDistance)

    # Print the City IDs of the tour
    for city in cities:
        #print("{0} {1} {2}".format(city, cities[city]["x"], cities[city]["y"]))
        print(city, file=outFile)
        # TODO: Comment out (easier to look at output in console for debugging)
        print(city)

if __name__ == "__main__":
    main()
