import sys
import math
import numpy as np
"""
This file contains the implementation of Part B
Contributors: Amit Deb, Andrew Avola, Alana Reyna, and Kallista Stamas
Description: This code contains the implementation of the clock(second chance) 
             page replacement algorithm. 
"""

"""
global clock: Array of the converted physical addresses
Args: None
Returns: None
"""
global clock

"""
global clockIndex: Array of the clock indexes
Args: None
Returns: None
"""
global clockIndex

"""
global table: 2D arrary that holds the updated page table
Args: None
Returns: None
"""
global table

"""
def init(table): Function that populates the page table 
Args: global table
Returns: the integer values of n(the number of bits in the virtual address), 
        m(the number of bits in the physical address), and size(the size of a
        page in bytes).
"""
def init(table):
    # n: number of bits in the virtual address
    n = 0
    # m: number of bits in the physical address
    m = 0
    # size: the size of a page converted to an integer
    size = 0
    # temp variable count: tells us if we are looking at the virtual address in
    # the table, physical address, or the page size 
    counter = 0
    # loop through the first line of our table from input to access n, m, and size
    for i in table[0][:3]:
        if counter == 0:
            # set the n variable to virtual address number of bits
            n = i
        elif counter == 1:
            # set the m variable to the physical address number of bits
            m = i
        else:
            # set the size variable to the size of the page 
            size = i
        counter +=1  
    
    # set the size to the natural logorithm of base 2
    size = math.log(size,2)    
    return (n , m , int(size))  

"""
def returnPhysicalAddress: updates the table variable by calling updateTable function
        with the physical addresses and PRINTS the physical address or prints SEGFAULT
        or DISK. 
Args: pageNum, bitSize, offset
Returns: None
"""
def returnPhysicalAddress(pageNum, bitSize, offset):
    
    global table
    global clock
    global clockIndex
    
    # create rowIndex integer variable based on the pageNum 
    rowIndex = int(pageNum,2)
    # 
    toAppend = f'{table[rowIndex][2]:0{bitSize}b}'
   
    if table[rowIndex][1] == 0:
        print("SEGFAULT")
        return
    elif table[rowIndex][0] == 0:
        while True:
            if clock[clockIndex][0] == 1:
                clock[clockIndex][0] = 0
                updateClockIndex()
                #update table with unrecently
            elif clock[clockIndex][0] == 0:

                updateTable(rowIndex)
                toAppend = f'{table[clock[clockIndex][1]][2]:0{bitSize}b}'
                clock[clockIndex][0] = 1
                table[rowIndex][3] = 1
                updateClockIndex()
                break
            
        
        print("PAGEFAULT ", hex(int(toAppend + offset,2)))
        return
    
    counter = 0
    for j in clock:
        if j[1] == rowIndex:
            clock[counter][0] = 1
        counter +=1
    table[rowIndex][3] = 1
    
    print(hex(int(toAppend + offset,2)))
    return 

"""
def updateClockIndex: updates our clockIndex variable 
Args: None
Returns: None
"""
def updateClockIndex():
    global clockIndex
    global clock
    if (clockIndex + 1) > len(clock)-1:
        clockIndex = 0
    else:
        clockIndex += 1

"""
def updateTable: updates the table, clock, and clock index based on the rowIndex given.
Args: rowIndex
Returns: None
"""
def updateTable(rowIndex):
    
    global table
    global clock
    global clockIndex
    
    table[clock[clockIndex][1]][0] = 0 #Old Value
    
    table[rowIndex][2] = table[clock[clockIndex][1]][2] #Replace table
    table[rowIndex][0] = 1 # Now Valid
    clock[clockIndex][0] = 1 #RU
    table[rowIndex][3] = 1 #RU
    clock[clockIndex][1] = rowIndex #New index at the table
    
"""
def initClock: creates the initial clock.
Args: None
Returns: localClock
"""
def initClock():
    
    global table
    
    localClock = []
    counter = 0
    for row in table:
        if row[0] == 1:
            localClock.append([row[3], counter])
        counter += 1
    #localClock = [row[3] for row in table if row[0] == 1]
    return localClock
    
"""
def fileChecker: checks if we are given valid input.
Args: x
Returns: True or False 
"""
def fileChecker(x):
    if len(x) == 4:
        if x[0] != 0 and x[0] != 1:
            return False
        elif x[1] < 0 or x[1] > 7:
            return False
        elif x[2] < 0:
            return False
        elif x[3] != 0 and x[3] != 1:
            return False
        else:
            return True
    else:
        return False

"""
def main: handles opening the input file, initializing/populating our global variables, 
            checks for valid input, and checks if the input file given is in hex or 
            decimal. 
Args: arg
Returns: None (calls the returnPhysicalAddress function which will 
        print the physical addresses) 
"""
def main(arg):

    global clock
    global clockIndex
    global table

    # open our file and put data into an array 
    with open(arg, 'r') as textFile:
        fileToRead = [list(map(int, line.split())) for line in textFile]


    n, m, size = init(fileToRead)

    # remove the first line that just contains our n, m, and size values.
    fileToRead.pop(0)
    # middleware: stores the fileToRead and checks that the input is valid 
    middleWare = filter(fileChecker, fileToRead)
    # temp table to store the page table 
    table = []
    # store input in table from the middleware variable 
    for x in middleWare:
        table.append(x)
    # create intial clock
    clock = initClock()
    # create intial clock index
    clockIndex = 0
    try:
        while True:
            userInput = input()
            # checks if input is given in hex
            if(userInput[:2] == "0x"):
                #TODO check for valid inputs
                res = f'{int(userInput,16):0{n}b}'
                if len(res)> n:
                    print("Number is too large!")
                    exit(1)
                offset = res[-size:]
                pageNumBits = len(res) - size
                pageNum = res[:pageNumBits]
                
                appendSize = m - len(offset)
                returnPhysicalAddress(pageNum, appendSize, offset)
                
                
            else:
                #TODO check for valid inputs
                res = f'{int(userInput):0{n}b}'
                if len(res)> n:
                    print("Number is too large!")
                    exit(1)
                offset = res[-size:]
                pageNumBits = len(res) - size
                #print(res,len(res), offset, len(offset), pageNumBits, size)
                pageNum = res[:pageNumBits]
                appendSize = m - len(offset)
                #print(pageNum)
                
                returnPhysicalAddress(pageNum, appendSize, offset)
                
        
    except EOFError as e:
        print()

main(str(sys.argv[1]))