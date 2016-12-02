# Caleigh Runge-Hottman, Andrew Kittrell, Jeromie Clark
# CS325 - Project 4
# Traveling Salesman Problem Solver

from __future__ import print_function
import sys
import re
import time
import math
import random

# borrowed from tsp-verifier.py
def distance(a,b):
    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    #return int(math.sqrt(dx*dx + dy*dy)+0.5) # equivalent to the next line
    return int(round(math.sqrt(dx*dx + dy*dy)))

# borrowed from tsp-verifier.py
def readCities(inputFile):

    f = open(inputFile,'r')
    line = f.readline()
    cities = {}
    while len(line) > 1:
        lineparse = re.findall(r'[^,;\s]+', line)
        cities[int(lineparse[0])]={'id': int(lineparse[0]), 'x': int(lineparse[1]), 'y': int(lineparse[2])}
        line = f.readline()
    f.close()
    return cities

def main():

    # The first commandline option is the input file
    inputFile = sys.argv[1]
    outputFile = sys.argv[1] + ".tour"

    # A dictionary of cities and their coordinates
    cities = readCities(inputFile)

    # TODO: Calculate Tour

    # ***** DELETE THIS - ITS A PLACEHOLDER FOR THE CALCULATED TOUR *****
    tour = cities

    writeResults(outputFile, cities)


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
