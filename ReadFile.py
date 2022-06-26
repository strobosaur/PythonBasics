#!/usr/bin/env python
# coding: utf-8

# In[32]:


import os
import sys
import csv
import matplotlib.pyplot as plt

# FUNCTION ReadFileCsv
# LÄSER IN EN CSV FIL OCH RETURNERAR INNEHÅLLET SOM EN 2-DIMENSIONELL LISTA
def ReadFileCsv(filename):
    
    outputList = []
    
    if not os.path.isfile(filename):
        print('File does not exist. Terminating process.')
        sys.exit()
    else:
        with open (filename, mode='r', encoding='utf-8') as file:
            csvReader = csv.reader(file, delimiter = ';')
            
            for line in csvReader:
                outputList.append(line)
                
            return outputList
         
# FUNCTION NUMBER OF CARS
def NumberOfCars(inputList):
    totalCars = 0
    outputList1 = []
    outputList2 = []
    
    # FIND ALL SPEED LIMITS
    for i in range(1, len(inputList), 1):
        currentSpeed = int(inputList[i][1])
        if not currentSpeed in outputList1:
            outputList1.append(currentSpeed)
            outputList1.sort()            
            outputList2.append(0)
    
    # POPULATE LIST OF CARS AT EACH SPEED LIMIT
    for j in range(1, len(inputList), 1):
        currentSpeed = int(inputList[j][1])
        index = outputList1.index(currentSpeed)
        outputList2[index] += 1
        totalCars += 1
    
    # PRINT CAR & SPEED LIMIT DATA
    for k in range(0, len(outputList1), 1):
        print("Det finns " + str(outputList2[k]) + "\tmätningar där gällande hastighet är " + str(outputList1[k]) + "km/h")
        
    print("================================================================")
    print("Totalt passerade " + str(totalCars) + " bilar.")
    
    # PLOT DIAGRAM
    plt.bar(outputList1, outputList2)
    plt.title("Antal fordon för varje gällande hastighet")
    plt.xlabel("Gällande hastighet")
    plt.ylabel("Antal passerade fordon")
    plt.grid(True)
    plt.show()
    
# FUNCTION NUMBER OF CAMERAS
def NumberOfCameras(inputList):
    totalCameras = 0
    areaDict = {}
    
    # POPULATE DICTIONARY WITH CAMERA AND AREA DATA
    for i in range(1, len(inputList), 1):
        currentArea = inputList[i][3]
        if not currentArea in areaDict:
            areaDict[currentArea] = 1
            totalCameras += 1
        else:
            areaDict[currentArea] += 1
            totalCameras += 1
    
    # PRINT DICTIONARY CONTENTS
    print("Kommun\t\tAntal kameror")
    print("================================================================")
    for key in sorted(areaDict.keys()):
        print(key + "\t\t" + str(areaDict[key]))
        
    print("================================================================")
    print("Det finns totalt " + str(totalCameras) + " kameror.")
    
# FUNCTION SPEEDING CHECK
def SpeedingCheck(inputList):
    outputList = []
    multiplier = -1.0
    
    while (multiplier < 0.0)
        try:
            multiplier = float(input("Med hur många % skall hastigheten överskrida hastighetsbegränsningen för att visas?"))
        except:
            print("Skriv in en siffra...")
            
    multiplier /= 100
    multiplier += 1
    
    for i in range(1, len(inputList), 1):
        speedLimit = inputList[i][1]
        speedActual = inputList[i][2]
        
        if (speedActual >= (speedLimit * multiplier)):
            outputList.append(inputList[i])
        
    
# HUVUDPROGRAM
platsData = ReadFileCsv('platsData.csv')
kameraData = ReadFileCsv('kameraData.csv')
    
NumberOfCars(kameraData)

NumberOfCameras(platsData)


# In[ ]:




