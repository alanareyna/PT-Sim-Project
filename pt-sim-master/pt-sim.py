import sys
import math

"""
This file contains the implementation of Part A
Contributors: Amit Deb, Andrew Avola, Alana Reyna, Kallista Stamas
Description: This code contains the implementation of translating a given page table 
            and converting the virutal addresses to physical addresses.
"""

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
def init(twoArray): Function that gets and saves the number of bits in the virtual address,
                    number of bits in the physical address, and the sizeo of the page converted
                    to integer values. 
Args: twoArray
Returns: the integer values of n(the number of bits in the virtual address), 
        m(the number of bits in the physical address), and size(the size of a
        page in bytes).
"""
def init(twoArray):
    n = 0
    m = 0
    size = 0
    counter = 0
    for i in twoArray[0][:3]:
        if counter == 0:
            n = i
        elif counter == 1:
            m = i
        else:
            size = i
        counter +=1  
        
    size = math.log(size,2)    
    return (n , m , int(size))  

"""
def returnPhysicalAddress: returns either the physical address, SEGFAULT, or DISK.
Args: pageNum, twoArray, bitSize, offset
Returns: hex of the physical address, SEGFAULT, or DISK
"""
def returnPhysicalAddress(pageNum, twoArray, bitSize, offset):
    
    #print(repr(pageNumBits))
    rowIndex = int(pageNum,2)
    toAppend = f'{twoArray[rowIndex][2]:0{bitSize}b}'
    
    # checks if the twoArray at rowIndex does not have access permissions
    if twoArray[rowIndex][1] == 0:
        return("SEGFAULT")
    # checks if twoArray at rowIndex is invalid 
    elif twoArray[rowIndex][0] == 0:
        return("DISK")
    # returns the hex physical address otherwise
    return hex(int(toAppend + offset,2))
     
#'./tests/PT_A.txt'
with open(str(sys.argv[1]), 'r') as textFile:
    fileToRead = [list(map(int, line.split())) for line in textFile]
    
#print(input)

n, m, size = init(fileToRead)

fileToRead.pop(0)
#print(fileToRead)

# middleware: stores the fileToRead and checks that the input is valid 
middleWare = filter(fileChecker, fileToRead)

# static table variable to store the page table 
table = []

# populate table with data in middleware
for x in middleWare:
    table.append(x)


try:
    while True:
        userInput = input()
        # checks if the input given is in Hex
        if(userInput[:2] == "0x"):
            #TODO check for valid inputs
            
            res = f'{int(userInput,16):0{n}b}'
            if len(res)> n:
                print("Number is too large!")
                exit(1)
            #print("res:", res)
            #print(res[-size:])
            
            offset = res[-size:]
            pageNumBits = len(res) - size
            pageNum = res[:pageNumBits]
            
            appendSize = m - len(offset)
            print(returnPhysicalAddress(pageNum, table, appendSize, offset))
            
        # the input is given in decimal otherwise  
        else:
            #TODO check for valid inputs
            #decimalToBinary
            res = f'{int(userInput):0{n}b}'
            if len(res)> n:
                print("Number is too large!")
                exit(1)
            #print(res)
            offset = res[-size:]
            pageNumBits = len(res) - size
            pageNum = res[:pageNumBits]
            appendSize = m - len(offset)
            print(returnPhysicalAddress(pageNum, table, appendSize, offset))
            
    
except EOFError as e:
  print()

    