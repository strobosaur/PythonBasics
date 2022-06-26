#!/usr/bin/env python
# coding: utf-8

# In[97]:


import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

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
    print(f'{"Kommun":<24}{"Antal kameror":<24}')
    print("================================================")
    for key in sorted(areaDict.keys()):
        print(f'{key:<24}{str(areaDict[key]):<24}')
        
    print("================================================")
    print("Det finns totalt " + str(totalCameras) + " kameror.")
    
# FUNCTION SPEEDING CHECK
def SpeedingCheck(inputList):
    
    outputList = []
    multiplier = -1.0
    speedingCount = 0;
    
    # GET SPEEDING INPUT FROM CONSOLE
    while multiplier < 0:
        try:
            multiplier = float(input("Med hur många % skall hastigheten överskrida hastighetsbegränsningen för att visas?"))
        except:
            print("Skriv in en siffra...")
    
    # CHECK FOR SPEEDING ENTRIES
    for i in range(1, len(inputList), 1):
        speedLimit = float(inputList[i][1])
        speedActual = float(inputList[i][2])
        
        # CHECK IF SPEED LIMIT IS EXCEEDED BY GIVEN AMOUNT
        if (speedActual > (speedLimit * ((multiplier / 100) + 1))):
            outputList.append(inputList[i])
            speedingCount += 1
            
    # SORT LIST ON DATE COLUMN
    outputList.sort(key = lambda x:x[4])
    
    # PRINT SPEEDING DATA TO CONSOLE
    print("\nDet var " + str(speedingCount) + " överträdelser som var mer än " + str(multiplier) + "% över gällande hastighet.\n")
    print(f'{"Tid":<16}{"Mätplats ID":<16}{"Gällande Hastighet":<24}{"Hastighet":<16}{"Datum":<16}')
    print("========================================================================================")
    for row in outputList:
        print(f'{row[4]:<16}{row[0]:<16}{row[1]:<24}{row[2]:<16}{row[3]:<16}')    
    
# FUNCTION SPEEDING CHECK DIAGRAM
def SpeedingCheckDiagram(inputList, multiplier):
    
    outputList = []    
    listSpeed = []
    listSpeeding = []
    listTime = []    
    
    # CHECK FOR SPEEDING ENTRIES
    for i in range(1, len(inputList), 1):
        speedLimit = float(inputList[i][1])
        speedActual = float(inputList[i][2])
        
        # CHECK IF SPEED LIMIT IS EXCEEDED BY GIVEN AMOUNT
        if (speedActual > (speedLimit * ((multiplier / 100) + 1))):
            outputList.append(inputList[i])
            
    # SORT LIST ON DATE COLUMN
    outputList.sort(key = lambda x:x[4])
    
    # MAKE SEPARATE LISTS BY TYPE OF DATA
    for j in range(0, len(outputList), 1):
        listSpeed.append(float(outputList[j][1]))
        listSpeeding.append(float(outputList[j][2]))
        listTime.append(outputList[j][4])
    
    # PLOT DIAGRAM
    width1 = 0.8
    width2 = 0.5
    plt.figure(figsize=(24,16))
    plt.rcParams.update({'font.size': 24})
    plt.title("Tidpunkter där gällande hastighet överskridits med mer än " + str(multiplier) + "%")
    plt.xlabel("Hastighet km/h")
    plt.ylabel("Tidpunkt")
    plt.barh(listTime, listSpeeding, width2, color='r')
    plt.barh(listTime, listSpeed, width1, color='b')
    plt.grid(True)
    plt.show()
    
# HUVUDPROGRAM
platsData = ReadFileCsv('platsData.csv')
kameraData = ReadFileCsv('kameraData.csv')
    
#NumberOfCars(kameraData)

#NumberOfCameras(platsData)
#SpeedingCheck(kameraData)
SpeedingCheckDiagram(kameraData, 80)


# In[ ]:




