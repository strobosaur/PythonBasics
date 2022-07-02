#!/usr/bin/env python
# coding: utf-8

# In[23]:


import os
import sys
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
 
# ================================================================
# FUNCTION read_file
# LÄSER IN EN CSV FIL OCH RETURNERAR INNEHÅLLET SOM EN 2-DIMENSIONELL LISTA
def read_file(file_name):
    
    # DEFINE VARIABLES
    outputList = []
    
    if not os.path.isfile(file_name):
        print('File does not exist. Terminating process.')
        sys.exit()
    else:
        with open (file_name, mode='r', encoding='utf-8') as file:
            csvReader = csv.reader(file, delimiter = ';')
            
            for line in csvReader:
                outputList.append(line)
                
            return outputList
          
# ================================================================
# FUNCTION NUMBER OF CARS
def antal_bilar(kamera_data):
    
    # DEFINE VARIABLES
    totalCars = 0
    outputList1 = []
    outputList2 = []
    
    # PRINT HEADING TO CONSOLE
    PrintFunctionBreak("Hitta antal fordon som passerat per hastighetsbegränsning")
    
    # FIND ALL SPEED LIMITS
    for i in range(1, len(kamera_data), 1):
        currentSpeed = int(kamera_data[i][1])
        if not currentSpeed in outputList1:
            outputList1.append(currentSpeed)
            outputList1.sort()            
            outputList2.append(0)
    
    # POPULATE LIST OF CARS AT EACH SPEED LIMIT
    for j in range(1, len(kamera_data), 1):
        currentSpeed = int(kamera_data[j][1])
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
def antal_kameror(plats_data):
    
    # DEFINE VARIABLES
    totalCameras = 0
    areaDict = {}
    
    # PRINT HEADING TO CONSOLE
    PrintFunctionBreak("Gör lista över antal fartkameror per kommun")
    
    # POPULATE DICTIONARY WITH CAMERA AND AREA DATA
    for i in range(1, len(plats_data), 1):
        currentArea = plats_data[i][3]
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
def hastighetplus(kamera_data, procentover = -1.0, displayData = True):
    
    # DEFINE VARIABLES
    plushastighet = []
    speedingCount = 0;
    
    # GET SPEEDING INPUT FROM CONSOLE
    while procentover < 0:
        try:
            procentover = float(
                input("Med hur många % skall hastigheten överskrida hastighetsbegränsningen för att visas?"))
        except:
            print("Skriv in en siffra...")
    
    # CHECK FOR SPEEDING ENTRIES
    for i in range(1, len(kamera_data), 1):
        speedLimit = float(kamera_data[i][1])
        speedActual = float(kamera_data[i][2])
        
        # CHECK IF SPEED LIMIT IS EXCEEDED BY GIVEN AMOUNT
        if (speedActual > (speedLimit * ((procentover / 100) + 1))):
            plushastighet.append(kamera_data[i])
            speedingCount += 1
            
    # SORT LIST ON DATE COLUMN
    plushastighet.sort(key = lambda x:x[4])
    
    if displayData:            
        # PRINT SPEEDING DATA TO CONSOLE
        PrintFunctionBreak("Skapa lista över trafiköverträdelser av given procent")
        print("\nDet var " 
              + str(speedingCount) 
              + " överträdelser som var mer än " 
              + str(procentover) 
              + "% över gällande hastighet.\n")
        print(f'{"Tid":<16}{"Mätplats ID":<16}{"Gällande Hastighet":<24}{"Hastighet":<16}{"Datum":<16}')
        print("========================================================================================")
        for row in plushastighet:
            print(f'{row[4]:<16}{row[0]:<16}{row[1] + " km/h":<24}{row[2] + " km/h":<16}{row[3]:<16}')
            
        print("========================================================================================\n")
        
    # RETURN CREATED LIST
    return (plushastighet, procentover)
     
# ================================================================
# FUNCTION SPEEDING CHECK DIAGRAM
def hastighetplusdiagram(plus_hastighet, procent_over):
    
    # DEFINE VARIABLES
    outputList = []    
    listSpeed = []
    listSpeeding = []
    listTime = []   
    
    # PRINT HEADING TO CONSOLE
    PrintFunctionBreak("Skapa diagram över hastighetsöverträdelser") 
    
    # MAKE SEPARATE LISTS BY TYPE OF DATA
    for i in range(0, len(plus_hastighet), 1):
        listSpeed.append(float(plus_hastighet[i][1]))
        listSpeeding.append(float(plus_hastighet[i][2]))
        listTime.append(plus_hastighet[i][4])
    
    # PLOT DIAGRAM
    width1 = 0.8
    width2 = 0.5
    plt.figure(figsize=(16,8))
    plt.rcParams.update({'font.size': 20})
    plt.title("Tidpunkter där gällande hastighet överskridits med mer än " + str(procent_over) + "%")
    plt.xlabel("Hastighet km/h")
    plt.ylabel("Tidpunkt")
    plt.barh(listTime, listSpeeding, width2, color='green')
    plt.barh(listTime, listSpeed, width1, color='black')
    plt.grid(True)
    plt.show()
    
     
# ================================================================
# FUNCTION SPEEDING CHECK DIAGRAM
def SpeedingCheckDiagram(inputList, multiplier):
    
    # DEFINE VARIABLES
    outputList = []    
    listSpeed = []
    listSpeeding = []
    listTime = []   
    
    # PRINT HEADING TO CONSOLE
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
def hastighetkommun(plus_hastighet, plats_data):
    
    # DEFINE VARIABLES
    tempstring = ""
    listSpeedingArea = []
    speedingCount = len(plus_hastighet)
    
    # PRINT HEADING TO CONSOLE
    PrintFunctionBreak("Kontrollera hastighetsöverträdelser per kommun och väg")
    
    # LOOP THROUGH LIST AND FIND AREAS WHERE SPEEDING HAS OCCURED
    for i in range(0, len(plus_hastighet), 1):
        tempstring = plus_hastighet[i][0]
        index = ListIndex2D(plats_data, tempstring)
        listSpeedingArea.append(plats_data[index[0]])
        
    # PRINT RESULTING DATA TO CONSOLE
    print("Hastighetsöverträdelserna skedde vid följande " + str(speedingCount) + " platser.\n")
    print(f'{"Tid":<16}{"MätplatsID":<16}{"Kommun":<20}{"Vägnummer":<16}{"Hastighet":<16}')
    print("========================================================================================")
    for j in range(0, len(plus_hastighet), 1):
        print(f'{plus_hastighet[j][4]:<16}{plus_hastighet[j][0]:<16}{listSpeedingArea[j][3]:<20}{listSpeedingArea[j][2]:<16}{plus_hastighet[j][2] + " km/h":<16}')
        
    print("========================================================================================\n")
         
# FUNCTION NUMBER OF CARS PER HOURS OF THE DAY
def bilar_timme(kamera_data, lowLimit = 7, highLimit = 17):
    
    # DEFINE VARIABLES
    hourList = []
    carList = []
    
    # POPULATE HOUR LIST & CAR LIST WITH INDEXES
    for j in range(lowLimit, highLimit + 1, 1):
        timetmp = datetime.time(j,0,0)
        hourList.append(timetmp.strftime("%H:%M"))
        carList.append(0)
    
    # FILL LISTS WITH ACTUAL DATA
    for i in range(1, len(kamera_data), 1):
        time = kamera_data[i][4].split(":")
        hour = int(time[0])
        if (hour >= lowLimit) and (hour <= highLimit):
            carList[hour - lowLimit] += 1     
        
    # PLOT DIAGRAM WITH GATHERED DATA
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(16,16))
    plt.title('Antal bilar passerade per timme')
    plt.xlabel('Tid')
    plt.ylabel('Antal registrerade fordon')
    plt.ylim(0,200)
    plt.plot(hourList, carList)
    plt.grid(True)
    plt.show()  
        
# ================================================================
# FUNCTION FIND INDEX IN 2D LIST
def ListIndex2D(inputList, item):
    for i, x in enumerate(inputList):
        if item in x:
            return i, x.index(item)
        
        
# ================================================================
# FUNCTION PRINT FUNCTION BREAK LINES
def PrintFunctionBreak(name, length = 64):
    line = ""
    for i in range(0, length, 1):
        line += "="
    print(line)
    print(" *** " + name + " *** ")
    print(line)
    print() 
        
# ================================================================
# FUNCTION MAIN MENU
def MainMenu():
    runProgram = True
    menuIndex = 0
    
    indent1 = 8
    indent2 = 16
    
    os.system('clear')
    
    while runProgram:
        print(f'{"":<indent1}{"1. Hämta data från fil":<16}')
        print(f'{"":<indent1}{"2. Analysera data":<16}')
        print(f'{"":<indent2}{"a. Antal bilar":<16}')
        print(f'{"":<indent2}{"b. Antal kameror":<16}')
        print(f'{"":<indent2}{"c. För fort":<16}')
        print(f'{"":<indent2}{"d. Bilar per timme":<16}')
        print(f'{"":<indent1}{"3. Avsluta":<16}')
        
        menuIndex = input("\nVälj menyalternativ (1-3):")
        if menuIndex not in range(1,3,1):
            break
        else:
            break
        
    
# ================================================================    
# ================================================================    
# ================================================================
# HUVUDPROGRAM

platsData = read_file('platsData.csv')
kameraData = read_file('kameraData.csv')


    
#antal_bilar(kameraData)
#antal_kameror(platsData)
#hplista = hastighetplus(kameraData)
#hastighetplusdiagram(hplista[0], hplista[1])
#hastighetkommun(hplista[0], platsData)
bilar_timme(kameraData)

#list01 = [[1,2,3,4],[3,4,5,6,7],[5,2,3,7,9]]
#index = ListIndex2D(list01, 9)
#print(index[1])
#print(list01[index[0]][index[1]])
#speedingList = SpeedingCheck(kameraData, 70, False)
#SpeedingCheckArea(speedingList, platsData)

#antal_kameror(platsData)
#SpeedingCheck(kameraData)
#peedingCheckDiagram(kameraData, 80)
#CarsPerHour(kameraData)


# In[ ]:




