# Jeromie Clark
# CS325 - Project 1
# Maximum Sum Subarray Experimental Analysis

import sys
import time
import math
import random

# Seeds the PNRG with time() or os.urandom() if available
random.seed(None)

# Just an example algorithm implementation
# Takes a List of inputData, returns an output string
def exampleAlg(inputData):
    output = "Example Algorithm: "
    for d in inputData:
        output += " " + repr(d)
    return output

# doPerfTest
# Peforms a series of performance tests on a given function
# Parameters:
# function = name of the function to test, must accept a List as input
# iterations = number of iterations to run the test (more iterations = more accuracy)
# size = size of random input data to generate for function
# inFile (optional) = input file to use (size is ignored)
# outFile (optional) = file to output results to

def doPerfTest(function, iterations, size):
    timerData = []                # Stores results in milliseconds
    outputData = []

    for i in range (0, iterations):

        inputData = genInputData(size)

        start_time = time.clock()   # time.clock() is more accurate than time.time()
        # Calls the algorithm to be timed
        out = function(inputData)
        end_time = time.clock()

        outputData.append(out)
        timerData.append(end_time - start_time)

    print("Results for function {}:").format(function.func_name)
    print("Function Output:")
    for out in outputData:
        print(out)
    print("Total Execution Time for {} iterations: {}").format(iterations, sum(timerData))

    # http://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
    mean = sum(timerData, 0.0) / len(timerData)
    print("Mean Execution Time: {}").format(mean)
    print("Raw Timer Data:")
    for td in timerData:
        print(td)

# genInputData
# Returns a list of random integers
# size - number of integers to return
# min (default = 0) - minimum random integer
# max (default = 99) - maximum random integer

def genInputData(size, min = 0, max = 99):
    intList = []
    for i in range (0, size):
        intList.append(random.randrange(min, max))
    return intList

# Example Call
# Executes exampleAlg 10 times, using 10 digits of input data

doPerfTest(exampleAlg, 10, 10)
