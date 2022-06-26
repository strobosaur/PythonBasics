#!/usr/bin/env python
# coding: utf-8

# In[175]:


import os
import sys
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
 
# ================================================================
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
          
# ================================================================
# FUNCTION NUMBER OF CARS
def NumberOfCars(inputList):
    
    totalCars = 0
    outputList1 = []
    outputList2 = []
    
    PrintFunctionBreak("Hitta antal fordon som passerat per hastighetsbegränsning")
    
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
    plt.rcParams.update({'font.size': 14})
    plt.bar(outputList1, outputList2)
    plt.title("Antal fordon för varje gällande hastighet")
    plt.xlabel("Gällande hastighet")
    plt.ylabel("Antal passerade fordon")
    plt.grid(True)
    plt.show()
     
# ================================================================
# FUNCTION NUMBER OF CAMERAS
def NumberOfCameras(inputList):
    
    totalCameras = 0
    areaDict = {}
    
    PrintFunctionBreak("Gör lista över antal fartkameror per kommun")
    
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
    print("================================================\n")
    
    #return areaDict
     
# ================================================================
# FUNCTION SPEEDING CHECK
def SpeedingCheck(inputList, multiplier = -1.0, displayData = True):
    
    outputList = []
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
    
    if displayData:            
        # PRINT SPEEDING DATA TO CONSOLE
        PrintFunctionBreak("Skapa lista över trafiköverträdelser av given procent")
        print("\nDet var " + str(speedingCount) + " överträdelser som var mer än " + str(multiplier) + "% över gällande hastighet.\n")
        print(f'{"Tid":<16}{"Mätplats ID":<16}{"Gällande Hastighet":<24}{"Hastighet":<16}{"Datum":<16}')
        print("========================================================================================")
        for row in outputList:
            print(f'{row[4]:<16}{row[0]:<16}{row[1] + " km/h":<24}{row[2] + " km/h":<16}{row[3]:<16}')
            
        print("========================================================================================\n")
        
    # RETURN CREATED LIST
    return outputList
     
# ================================================================
# FUNCTION SPEEDING CHECK DIAGRAM
def SpeedingCheckDiagram(inputList, multiplier):
    
    outputList = []    
    listSpeed = []
    listSpeeding = []
    listTime = []   
    
    PrintFunctionBreak("Skapa diagram över hastighetsöverträdelser") 
    
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
     
# ================================================================
# FUNCTION SPEEDING BY AREA
def SpeedingCheckArea(listSpeeding, listArea):
    
    tempstring = ""
    listSpeedingArea = []
    speedingCount = len(listSpeeding)
    
    PrintFunctionBreak("Kontrollera hastighetsöverträdelser per kommun och väg")
    
    for i in range(0, len(listSpeeding), 1):
        tempstring = listSpeeding[i][0]
        index = ListIndex2D(listArea, tempstring)
        listSpeedingArea.append(listArea[index[0]])
        
    print("Hastighetsöverträdelserna skedde vid följande " + str(speedingCount) + " platser.\n")
    print(f'{"Tid":<16}{"MätplatsID":<16}{"Kommun":<20}{"Vägnummer":<16}{"Hastighet":<16}')
    print("========================================================================================")
    for j in range(0, len(listSpeeding), 1):
        print(f'{listSpeeding[j][4]:<16}{listSpeeding[j][0]:<16}{listSpeedingArea[j][3]:<20}{listSpeedingArea[j][2]:<16}{listSpeeding[j][2] + " km/h":<16}')
        
    print("========================================================================================\n")
         
# FUNCTION NUMBER OF CARS PER HOURS OF THE DAY
def CarsPerHour(inputList, lowLimit = 7, highLimit = 17):
    
    hourList = []
    carList = []
    
    for j in range(lowLimit, highLimit + 1, 1):
        timetmp = datetime.time(j,0,0)
        hourList.append(timetmp.strftime("%H:%M"))
        carList.append(0)
    
    for i in range(1, len(inputList), 1):
        time = inputList[i][4].split(":")
        hour = int(time[0])
        if (hour >= lowLimit) and (hour <= highLimit):
            carList[hour - lowLimit] += 1     
        
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(16,16))
    plt.title('Antal bilar passerade per timme')
    plt.xlabel('Timmar')
    plt.ylabel('Antal bilar')
    plt.plot(hourList, carList)
    plt.grid(True)
    plt.show()    
        
# ================================================================
# FUNCTION FIND INDEX IN 2D LIST
def ListIndex2D(inputList, item):
    for i, x in enumerate(inputList):
        if item in x:
            return i, x.index(item)
        
def PrintFunctionBreak(name, length = 64):
    line = ""
    for i in range(0, length, 1):
        line += "="
    print(line)
    print(" *** " + name + " *** ")
    print(line)
    print()
    
# ================================================================    
# ================================================================    
# ================================================================
# HUVUDPROGRAM

platsData = ReadFileCsv('platsData.csv')
kameraData = ReadFileCsv('kameraData.csv')


    
#NumberOfCars(kameraData)
#list01 = [[1,2,3,4],[3,4,5,6,7],[5,2,3,7,9]]
#index = ListIndex2D(list01, 9)
#print(index[1])
#print(list01[index[0]][index[1]])
#speedingList = SpeedingCheck(kameraData, 70, False)
#SpeedingCheckArea(speedingList, platsData)

#NumberOfCameras(platsData)
#SpeedingCheck(kameraData)
#peedingCheckDiagram(kameraData, 80)
CarsPerHour(kameraData)


# In[ ]:




