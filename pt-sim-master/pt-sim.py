import sys
import math

"""
This file contains the implementation of Part A
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

def returnPhysicalAddress(pageNum, twoArray, bitSize, offset):
    
    #print(repr(pageNumBits))
    rowIndex = int(pageNum,2)
    toAppend = f'{twoArray[rowIndex][2]:0{bitSize}b}'
    
    
    
    if twoArray[rowIndex][1] == 0:
        return("SEGFAULT")
    elif twoArray[rowIndex][0] == 0:
        return("DISK")
    return hex(int(toAppend + offset,2))
     
#'./tests/PT_A.txt'
with open(str(sys.argv[1]), 'r') as textFile:
    fileToRead = [list(map(int, line.split())) for line in textFile]
    
#print(input)

n, m, size = init(fileToRead)

fileToRead.pop(0)
#print(fileToRead)

middleWare = filter(fileChecker, fileToRead)
table = []
for x in middleWare:
    table.append(x)


try:
    while True:
        userInput = input()
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

    