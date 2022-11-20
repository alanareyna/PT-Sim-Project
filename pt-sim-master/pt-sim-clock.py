import sys
import math
import numpy as np

global clock
global clockIndex
global table


def init(table):

    n = 0
    m = 0
    size = 0
    counter = 0
    for i in table[0][:3]:
        if counter == 0:
            n = i
        elif counter == 1:
            m = i
        else:
            size = i
        counter +=1  
        
    size = math.log(size,2)    
    return (n , m , int(size))  

def returnPhysicalAddress(pageNum, bitSize, offset):
    
    global table
    global clock
    global clockIndex
    
    rowIndex = int(pageNum,2)
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


def updateClockIndex():
    global clockIndex
    global clock
    if (clockIndex + 1) > len(clock)-1:
        clockIndex = 0
    else:
        clockIndex += 1

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


def main(arg):

    global clock
    global clockIndex
    global table

    with open(arg, 'r') as textFile:
        fileToRead = [list(map(int, line.split())) for line in textFile]


    n, m, size = init(fileToRead)

    fileToRead.pop(0)


    middleWare = filter(fileChecker, fileToRead)
    table = []
    for x in middleWare:
        table.append(x)

    clock = initClock()
    clockIndex = 0
    try:
        while True:
            userInput = input()
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