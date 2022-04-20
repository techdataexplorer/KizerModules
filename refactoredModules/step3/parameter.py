# 5/18/21 Updated file paths to pull data from my machine

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import os
import numpy as np
import pandas as pd
import math

class ParameterB(object):

    def __init__(self):
        self.ExampleS3FolderPath = ""
        self.MilesKm = ""
        self.TheRoughness = [None] * 100
        self.TheHeight = [None] * 100


    def setFolderPath(self, folderPath):
        self.ExampleS3FolderPath = str(folderPath)

    def setMilesKm(self, milesKm):
        self.MilesKm = milesKm
        self.MilesKm = self.MilesKm.upper()

    def distance_between_a_and_b(self, MilesKm, LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB):
        # 'CALCULATE DISTANCE BETWEEN SITE A and SITE B
        # 'INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
        # 'OUTPUT: Z# (DISTANCE IN MILES)

        # 'HIGH ACCURACY FORMULA
        Z = (math.sin((math.radians(LATITUDEA - LATITUDEB)) / 2)) ** 2
        Z += math.cos(math.radians(LATITUDEA)) * math.cos(math.radians(LATITUDEB)) * (math.sin((math.radians(LONGITUDEA - LONGITUDEB)) / 2)) ** 2
        Z = math.sqrt(Z)
        # X = Z
        
        ZSHORT = 2 * (180 / math.pi) * math.asin(Z)

        if MilesKm == "M":
            return 69.06 * ZSHORT  # DISTANCE IN MILES
        # elif MilesKm == "K":
        return 111.1 * ZSHORT  # DISTANCE IN KILOMETERS

    # Retrieve path roughness and lower height
    def pathRoughnessLowerHeight(self, PathIndex, ProfilesFolderPath):
        ProfileNumber = str(PathIndex)
        COUNTER = PathIndex

        if COUNTER < 100000: 
            ProfileNumber = "0" + ProfileNumber
        if COUNTER < 10000:  
            ProfileNumber = "0" + ProfileNumber
        if COUNTER < 1000:  
            ProfileNumber = "0" + ProfileNumber
        if COUNTER < 100:  
            ProfileNumber = "0" + ProfileNumber
        if COUNTER < 10:
            ProfileNumber = "0" + ProfileNumber

        RoughnessFile = "/Roughness" + ProfileNumber + ".CSV"

        LoopCounter = 0
        #ProfilesFolderPath = 'C:\\Users\\Jeffrey\\Desktop\\Summer 2021\\Path Design 11 April 2021\\Step 3 Path Availability\\ExampleStep3\\Profiles\\'
        #ProfilesFolderPath = ProfilesFolderPath + "/Profiles"
        # print("AAAAAAAAAAAA")
        # print(ProfilesFolderPath)
        # print("AAAAAAAAAAAA")

        roughness_df = pd.read_csv(ProfilesFolderPath + RoughnessFile)
        
        self.TheRoughness[PathIndex] = roughness_df.columns.tolist()[0]
        self.TheHeight[PathIndex] = roughness_df.columns.tolist()[1]

        print(str(PathIndex) + " , " + "Roughness = " + str(self.TheRoughness[PathIndex]) + " ,  Lower Height = " + str(self.TheHeight[PathIndex]))

    def pathParameter(self, df, AvgLatitude, AvgLongitude):  # find a path parameter
        TheDistance = 500
        ThePathParameter = "100"

        for index, row in df.iterrows():
            ALongitude = row[0]
            ALatitude = row[1]
            APathParameter = row[2]

            LATITUDEA = AvgLatitude
            LONGITUDEA = AvgLongitude
            LATITUDEB = float(ALatitude)
            LONGITUDEB = float(ALongitude)

            Distance = self.distance_between_a_and_b("M", LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB)
            # print("Distance: ", Distance)

            if Distance < TheDistance:
                TheDistance = Distance
                ThePathParameter = APathParameter
        
        return TheDistance, ThePathParameter

    def execute(self):
        #empty array with 100 slots open, all values None
        TheClimateFactor = [None] * 100
        TempF = [None] * 100
        dN1 = [None] * 100
        Sa = [None] * 100 
        PathDistance = [None] * 100 
        self.TheRoughness = [None] * 100 
        R01 = [None] * 100 
        RelHum = [None] * 100
        self.TheHeight = [None] * 100

        #ExampleS3FolderPath = "C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Path Design 11 April 2021/Step 3 Path Availability/ExampleStep3"
        PathsFilePath = self.ExampleS3FolderPath + "/Paths.csv"
        paths_df = pd.read_csv(PathsFilePath)

        headers = list(paths_df.columns)
        HEADER1 = headers[0]
        HEADER2 = headers[1]

        MilesKm = "M"

        CheckFlag = 0
        if HEADER1 != "Index":
            CheckFlag = 1
        if HEADER2 != "Site1":
            CheckFlag = 2
        if CheckFlag > 0:
            print("File headers do not match required file format.")
            print("Left most two header words are not <Index> and <Site1>.")
            print("First header = <" + HEADER1 + "> but should be <Index>.")
            print("Second header = <" + HEADER2 + "> but should be <Site1>.")
            print("The program is terminated.")
            exit(1)

        # create the average coordinates for each path

        TheOutputDataFile11 = self.ExampleS3FolderPath + "\\AveragePaths.csv"
        average_paths_df = open(TheOutputDataFile11, "w+")
        average_paths_df.write("Index,Average Latitude,Average Longitude,Distance\n")


        for index, row in paths_df.iterrows():
            PathIndex = int(row['Index'])
            Site1 = row['Site1']
            Latitude1 = row['Latitude1']
            Longitude1 = row['Longitude1']
            Site2 = row['Site2']
            Latitude2 = row['Latitude2']
            Longitude2 = row['Longitude2']

            Distance = self.distance_between_a_and_b(MilesKm, Latitude1, Latitude2, Longitude1, Longitude2)
            AvgLatitude = (Latitude1 + Latitude2) / 2.
            AvgLongitude = (Longitude1 + Longitude2) / 2.

            # print(str(PathIndex) + ", " + str(AvgLatitude) + ", " + str(AvgLongitude) + ", " + str(Distance))
            average_paths_df.write(str(PathIndex) + "," + str(AvgLatitude) + "," + str(AvgLongitude) + "," + str(Distance) + '\n')

        average_paths_df.close()

        # 'find parameters for the path

        TheOutputDataFile12 = self.ExampleS3FolderPath + "/PathParameters.csv"

        path_parameters_df = open(TheOutputDataFile12, "w+")
        path_parameters_df.write("Index,Path Distance (miles),Path Roughness (ft),Climate Factor,Temp (F),dN1,Sa (ft),Rain Rate,Relative Humidity,Lower Height (ft)\n")

        average_paths_df = pd.read_csv(TheOutputDataFile11)

        ClimateFactorFilePath = self.ExampleS3FolderPath + "/Data/ClimateFactorNaA.csv"

        TempFAFilePath = self.ExampleS3FolderPath + "/Data/TempFnaB.csv"

        ITURdN1AFilePath =  self.ExampleS3FolderPath + "/Data/dN1naB.csv"

        ITURSaAFilePath = self.ExampleS3FolderPath + "/Data/SaFeetNaB.csv"

        ITURR01AFilePath = self.ExampleS3FolderPath + "/Data/R01naB.csv"

        RelHumAFilePath = self.ExampleS3FolderPath + "/Data/RelHumNaA.csv"

        ProfilesFolderPath = self.ExampleS3FolderPath + "/Profiles"

        for index, row in average_paths_df.iterrows():
            PathIndex = int(row['Index'])
            AvgLatitude = row['Average Latitude']
            AvgLongitude = row['Average Longitude']
            PathDistance[PathIndex] = row['Distance']

            # find the various parameters for the path
            self.pathRoughnessLowerHeight(PathIndex, ProfilesFolderPath)

            climate_factor_df = pd.read_csv(ClimateFactorFilePath) 
            TheDistance, TheClimateFactor[PathIndex] = self.pathParameter(climate_factor_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "Climate Factor = " + str(TheClimateFactor[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            tempFA_df = pd.read_csv(TempFAFilePath) 
            TheDistance, TempF[PathIndex] = self.pathParameter(tempFA_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "Average Temperture (F) = " + str(TempF[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            ITURdN1A_df = pd.read_csv(ITURdN1AFilePath)
            TheDistance, dN1[PathIndex] = self.pathParameter(ITURdN1A_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "Refractivity Gradient = " + str(dN1[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            ITURSaA_df = pd.read_csv(ITURSaAFilePath)
            TheDistance, Sa[PathIndex] = self.pathParameter(ITURSaA_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "ITR-R Roughness = " + str(Sa[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            ITURR01A_df = pd.read_csv(ITURR01AFilePath)
            TheDistance, R01[PathIndex] = self.pathParameter(ITURR01A_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "ITR-R Rain Rate = " + str(R01[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            RelHumA_df = pd.read_csv(RelHumAFilePath)
            TheDistance, RelHum[PathIndex] = self.pathParameter(RelHumA_df, AvgLatitude, AvgLongitude) 
            print(str(PathIndex) + " , " + "Relative Humidity = " + str(RelHum[PathIndex]) + " ,  Distance (miles) = " + str(TheDistance))

            path_parameters_df.write(str(PathIndex) + "," + str(PathDistance[PathIndex]) + "," + str(self.TheRoughness[PathIndex]) + "," + str(TheClimateFactor[PathIndex]) + "," + str(TempF[PathIndex]) + "," + str(dN1[PathIndex]) + "," + str(Sa[PathIndex]) + "," + str(R01[PathIndex]) + "," + str(RelHum[PathIndex]) + "," + str(self.TheHeight[PathIndex])  + '\n') # added  + '\n'

        print("Program Completed")

################################################## PyQT GUI Class ###################################################
# Based on code from https://pythonspot.com/pyqt5-file-dialog/

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

    def openFileNameDialog(self, filePrompt):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        
        fileName, _ = QFileDialog.getOpenFileName(self, filePrompt, "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            return fileName

    def openFolderNameDialog(self, folderPrompt):
        folderName = QFileDialog.getExistingDirectory(self, folderPrompt)
        if folderName:
            return folderName

################################################## End PyQT GUI Class ###################################################

## crate pyqt object
app = QApplication(sys.argv)
ex = App()



test = ParameterB()
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS3 Folder")
#test.setFolderPath("C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Path Design 11 April 2021/Step 3 Path Availability/ExampleStep3")
test.setFolderPath(ExampleS3FolderPath)
#test.setMilesKm("M")
test.setMilesKm(milesKm=input("Enter M or K(Miles or Kilometer): "))

test.execute()