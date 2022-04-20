#
# PathA.py
# Kizer Modules API
# Created by Che Blankenship on 11/08/2021
#

import os
import math
# import requests
import pandas as pd
from pandas.core.indexing import convert_to_index_sliceable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PathsA(object):

    def __init__(self, parent=None):
        # class attributes (variables for user input)
        self.FolderPath      = ""
        self.Answers         = []
        self.LandUse         = "Y"
        self.MaxDataPointsN  = 1
        self.DistanceFraction= None
        self.FeetMeters      = "" # F or M
        self.CompChoice      = 1

    # Setters
    def setFolderPath(self, folderPath):
        self.FolderPath = str(folderPath)

    def setLULC(self, landUse):
        self.LandUse = landUse

    def setMaxDataPoints(self, maxDataPoints):
        self.maxDataPointsN = int(maxDataPoints)

    def setDistanceFraction(self, distanceFraction):
        self.DistanceFraction = float(distanceFraction)

    def setCompressionOption(self, compression):
        self.CompChoice = compression


    #110
    def makeFiles(self, FolderPath, Answers,LandUse,MaxDataPointsN,DistanceFraction): #110
        DataFile = Answers[0]
        BuildingHt = Answers[4]
        TreeHt = Answers[5]
        OpFreq1 = Answers[6]
        OpFreq2 = Answers[8]
        OpFreq3 = Answers[10]
        OpFreq4 = Answers[12]
        MaxDist1 = Answers[21]
        MaxDist2 = Answers[7]
        MaxDist3 = Answers[9]
        MaxDist4 = Answers[11]

        PathFreqFileName = self.FolderPath + "\TempFile\\" + "PathFreq.CSV" #66
        PathDataFileName = self.FolderPath + "\TempFile\\" + "PathData.CSV" #67
        PathFreqFile = open(PathFreqFileName, "w")
        PathDataFile = open(PathDataFileName, "w")
        PathFileName = self.FolderPath + "\\" + DataFile + ".CSV"
        PathFile_df = pd.read_csv(PathFileName, header = None)#10

        for index, pfRow in PathFile_df.iterrows():

            Header1 = str(pfRow[0])
            Header2 = str(pfRow[1])
            Header3 = str(pfRow[2])
            Header4 = str(pfRow[3])
            Header5 = str(pfRow[4])
            Header6 = str(pfRow[5])
            Header7 = str(pfRow[6])
            Header8 = str(pfRow[7])
            Header9 = str(pfRow[8])
            break

        if(not(Header1 == "Index" and Header8 == "TowerHeight1" and Header9 == "TowerHeight2")):
            print("File does not match required file format.")
            print("The left most column should be labeled <Index>.")
            print("The two right columns should be labeled <TowerHeight1> and <TowerHeight2> respectively.")
            print("Program terminated prematurely.")
            PathFreqFile.close()
            PathDataFile.close()
            del PathFile_df
            self.endProgram()#9999
        PathCounter = 0
        del PathFile_df

        PathFileName = self.FolderPath + "\\" + DataFile + ".CSV"
        PathFile_df = pd.read_csv(PathFileName)#10

        for index1, pfRow1 in PathFile_df.iterrows():
            PathIndex = str(pfRow1[0])
            SITE1 = str(pfRow1[1])
            Latitude1 = str(pfRow1[2])
            Longitude1 = str(pfRow1[3])
            SITE2 = str(pfRow1[4])
            Latitude2 = str(pfRow1[5])
            Longitude2 = str(pfRow1[6])
            TwrHt1 = str(pfRow1[7])
            TwrHt2 = str(pfRow1[8])

            ProfileNumber = int(PathIndex)

            if(ProfileNumber < 10):
                ProfileNumber = "00000" + str(ProfileNumber)
            elif(ProfileNumber < 100):
                ProfileNumber = "0000" + str(ProfileNumber)
            elif(ProfileNumber < 1000):
                ProfileNumber = "000" + str(ProfileNumber)
            elif(ProfileNumber < 10000):
                ProfileNumber = "00" + str(ProfileNumber)
            elif(ProfileNumber < 100000):
                ProfileNumber = "0" + str(ProfileNumber)

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Processing Path Number " + PathIndex + ", Site 1 = " + SITE1 + ", Site 2 = " + SITE2)

            #Initial profile processing - Pass A ++++++++++++++++++++++++++++++++++
            #Create path distances and place tower heights as end point obstructions
            #If land use codes are available, add assumed obstruction buildings and trees

            TempFilePName = self.FolderPath + "\TempFile\P" + str(ProfileNumber) + ".CSV"
            TempFilePAName = self.FolderPath + "\TempFile\PA" + str(ProfileNumber) + ".CSV"


            try:
                TempFileP_df = pd.read_csv(TempFilePName, header = None) #11

            except FileNotFoundError:
                print("FileNotFoundError: " + TempFilePName + " not found")
                self.endProgram()

            TempFilePA = open(TempFilePAName, "w")    #12
            print("     Initial Processing  - PA")
            ProfileCount = 1

            if(self.LandUse == "Y"):
                for index2, pfRow2 in TempFileP_df.iterrows():
                    LONGITUDEA = float(pfRow2[0])
                    LATITUDEA = float(pfRow2[1])
                    ELEVATION = float(pfRow2[2])
                    LANDUSECODE = int(pfRow2[3])
                    break

            else:
                for index3, pfRow3 in TempFileP_df.iterrows():
                    LONGITUDEA = float(pfRow3[0])
                    LATITUDEA = float(pfRow3[1])
                    ELEVATION = float(pfRow3[2])
                    break

            Site1Elevation = ELEVATION
            Site1Distance = "0.0"
            TempFilePA.write("0.0" + "," + str(ELEVATION) + "," + str(TwrHt1) + "," + "A" + "," + "End Site" +"\n")

            #137
            del TempFileP_df
            TempFileP_df = pd.read_csv(TempFilePName) #11

            counter = 1
            for index4, pfRow4 in TempFileP_df.iterrows():
                ProfileCount +=1

                if(self.LandUse == "Y"):
                    LONGITUDEB = float(pfRow4[0])
                    LATITUDEB = float(pfRow4[1])
                    ELEVATION = float(pfRow4[2])
                    LANDUSECODE = int(pfRow4[3])

                if(self.LandUse == "N"):
                    LONGITUDEB = float(pfRow4[0])
                    LATITUDEB = float(pfRow4[1])
                    ELEVATION = float(pfRow4[2])

                LUcode = "N"
                LANDUSECODE = ""
                ObstructionHeight = "0.0"
                LANDUSECODESTR = ""

                if(self.LandUse == "Y"):
                    LANDUSECODE = int(pfRow4[3])
                    LUcode, LANDUSECODESTR = self.landUseConv(LANDUSECODE)
                if(LUcode == "B"):
                    ObstructionHeight = str(BuildingHt)
                if(LUcode == "T"):
                    ObstructionHeight = str(TreeHt)

                Zkm, Zmiles = self.calcDistance(LATITUDEA,LATITUDEB,LONGITUDEA,LONGITUDEB)

                if(self.FeetMeters == "F"):
                    distance = Zmiles
                if(self.FeetMeters == "M"):
                    distance = Zkm
                if(ProfileCount == 2):
                    DistanceIncrement = distance

                distance = int((distance * 1000) + .5)
                distance = distance / 1000
                distance = str(distance)

                EndOfFile =  (index4 == TempFileP_df.index[-1])
                if(not EndOfFile):
                    TempFilePA.write(distance + "," + str(ELEVATION) + "," + ObstructionHeight + "," + LUcode + "," + LANDUSECODESTR + "\n")
                else:
                    TempFilePA.write(distance + "," + str(ELEVATION) + "," + str(TwrHt2) + "," + "A" + "," + "End Site" + "\n")

            Site2Elevation = ELEVATION
            Site2Distance = distance

            del TempFileP_df
            TempFilePA.close()

            #Compress profile file - Pass B ++++++++++++++++++++++++++++++++++

            if(self.CompChoice == 1):
                CompressionRatio = 1
            if(self.CompChoice == 2):
                CompressionRatio = int((float(self.DistanceFraction) / float(DistanceIncrement) + .5))
            if(self.CompChoice == 3):
                CompressionRatio = ProfileCount // int(self.MaxDataPointsN)
            if(CompressionRatio < 1):
                CompressionRatio = 1

            #Initialize path clearances
            SiteDistance4MinInf = "0.0"     #K = Infinity
            SiteHeight4MinInf = 999999
            SiteDistance4Min43 = "0.0"      #K = 4/3
            SiteHeight4Min43 = 999999
            SiteDistance4Min1 = "0.0"       #K = 1
            SiteHeight4Min1 = 999999
            SiteDistance4Min23 = "0.0"      #K = 2/3
            SiteHeight4Min23 = 999999
            SiteDistance4Min12 = "0.0"      #K = 1/2
            SiteHeight4Min12 = 999999
            SiteDistance4Min512 = "0.0"     #K = 5/12
            SiteHeight4Min512 = 999999
            SiteDistance4Min410 = "0.0"     #K = 4/10
            SiteHeight4Min410 = 999999

            TempFilePAName = self.FolderPath + "\TempFile\PA" + ProfileNumber + ".CSV"
            TempFilePBName = self.FolderPath + "\TempFile\PB" + ProfileNumber + ".CSV"
            TempFilePA_df = pd.read_csv(TempFilePAName, header = None) #11
            TempFilePB = open(TempFilePBName, "w")    #12
            print("     Compressing Profile - PB")

            #reads in first line?
            for index5, pfRow5 in TempFilePA_df.iterrows():
                distance = float(pfRow5[0])
                ELEVATION = float(pfRow5[1])
                ObstructionHeight = int(pfRow5[2])
                LUcode = str(pfRow5[3])
                LANDUSECODE = str(pfRow5[4])
                break

            ELEVATION = float(ELEVATION)
            ELEVATION = int(ELEVATION + .5)
            ELEVATION = str(ELEVATION)
            TempFilePB.write(str(distance) + "," + ELEVATION + "," + str(ObstructionHeight) + "," + LUcode + "," + LANDUSECODE + "\n")

            del TempFilePA_df
            TempFilePA_df = pd.read_csv(TempFilePAName) #11

            counter = 0
            for index6, pfRow6 in TempFilePA_df.iterrows():
                EndOfFile =  (index6 == TempFilePA_df.index[-1])
                counter+=1

                MaxHeight = 0
                MaxELEVATION = ""
                MaxObstructionHeight = ""
                MaxLUcode = ""
                MaxLANDUSECODE = ""

                distance = float(pfRow6[0])
                ELEVATION = (pfRow6[1])
                ObstructionHeight = (pfRow6[2])
                LUcode = str(pfRow6[3])
                LANDUSECODE = str(pfRow6[4])

                #???
                ELEVATION = float(ELEVATION)
                ELEVATION = int(ELEVATION + .5)
                ELEVATION = str(ELEVATION)

                ObstructionHeight = float(ObstructionHeight)
                TotalHeight = float(ELEVATION) + ObstructionHeight

                if(TotalHeight > MaxHeight):
                    MaxHeight = TotalHeight
                    MaxELEVATION = ELEVATION
                    MaxObstructionHeight = ObstructionHeight
                    MaxLUcode = LUcode
                    MaxLANDUSECODE = LANDUSECODE

                if(EndOfFile):
                    continue

                if(not EndOfFile and (counter == CompressionRatio)):
                    counter = 0
                    TempFilePB.write(str(distance) + "," + str(MaxELEVATION) + "," + str(MaxObstructionHeight) + "," + str(MaxLUcode) + "," + str(MaxLANDUSECODE) + "\n")
                self.findTerrain(Site1Elevation,TwrHt1,Site2Elevation,TwrHt2,Site2Distance,distance,MaxELEVATION,SiteHeight4MinInf,SiteHeight4Min43,SiteHeight4Min1,SiteHeight4Min23,SiteHeight4Min12,SiteHeight4Min512,SiteHeight4Min410)

            TempFilePB.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + LUcode + "," + LANDUSECODE + "\n")
            del TempFilePA_df
            TempFilePB.close()

            #Final profile processing - Pass C ++++++++++++++++++++++++++++++++++
            #Add assumed tree obstructions for profiles without land use code information
            TempFilePBName = self.FolderPath + "\TempFile\PB" + ProfileNumber + ".CSV"
            TempFilePCName = self.FolderPath + "\TempFile\PC" + ProfileNumber + ".CSV"
            TempFilePB_df = pd.read_csv(TempFilePBName, header = None) #11
            TempFilePC = open(TempFilePCName, "w")    #12
            print("     Final Processing    - PC")

            if(self.LandUse == "Y"): #No further processing required - terrain obstructuions are already added
                for index7, pfRow7 in TempFilePB_df.iterrows():
                    distance = float(pfRow7[0])
                    ELEVATION = float(pfRow7[1])
                    ObstructionHeight = int(pfRow7[2])
                    LUcode = str(pfRow7[3])
                    LANDUSECODE = str(pfRow7[4])
                    TempFilePC.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + LUcode + "," + LANDUSECODE + "\n")


            if(self.LandUse == "N"): #Add trees at peaks and locations closest to path

                del TempFilePB_df
                TempFilePB_df = pd.read_csv(TempFilePBName, header = None) #11

                for index8, pfRow8 in TempFilePB_df.iterrows():
                    distance = float(pfRow8[0])
                    ELEVATION = float(pfRow8[1])
                    ObstructionHeight = int(pfRow8[2])
                    LUcode = str(pfRow8[3])
                    LANDUSECODE = str(pfRow8[4])
                    ELEVATIONA = float(ELEVATION)
                    ObstructionHeightA = ObstructionHeight
                    LUcodeA = LUcode
                    LANDUSECODEA = LANDUSECODE

                    TempFilePC.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + LUcode + "," + LANDUSECODE + "\n")
                    break

                del TempFilePB_df
                TempFilePB_df = pd.read_csv(TempFilePBName) #11

                for index9, pfRow9 in TempFilePB_df.iterrows():
                    distance = float(pfRow9[0])
                    ELEVATION = float(pfRow9[1])
                    ObstructionHeight = int(pfRow9[2])
                    LUcode = str(pfRow9[3])
                    LANDUSECODE = str(pfRow9[4])

                    DistanceB = distance
                    ELEVATIONB = float(ELEVATION)
                    ELEVATIONB = ELEVATION
                    ObstructionHeightB = ObstructionHeight
                    LUcodeB = LUcode
                    LANDUSECODEB = LANDUSECODE

                    break

                del TempFilePB_df
                TempFilePB_df = pd.read_csv(TempFilePBName, skiprows=1) #11

                for index10, pfRow10 in TempFilePB_df.iterrows():
                    EndOfFile =  (index10 == TempFilePB_df.index[-1])

                    distance = float(pfRow10[0])
                    ELEVATION = float(pfRow10[1])
                    ObstructionHeight = int(pfRow10[2])
                    LUcode = str(pfRow10[3])
                    LANDUSECODE = str(pfRow10[4])

                    DistanceC = distance
                    ELEVATIONC = float(ELEVATION)
                    ELEVATIONC = ELEVATION
                    ObstructionHeightC = ObstructionHeight
                    LUcodeC = LUcode
                    LANDUSECODEC = LANDUSECODE

                    if(EndOfFile):
                        TempFilePC.write(str(DistanceB) + "," + str(ELEVATIONB) + "," + str(ObstructionHeightB) + "," + LUcodeB + "," + LANDUSECODEB + "\n")
                        TempFilePC.write(str(DistanceC) + "," + str(ELEVATIONC) + "," + str(ObstructionHeightC) + "," + LUcodeC + "," + LANDUSECODEC + "\n")
                        break

                    addTrees(ELEVATIONA,ELEVATIONB,ELEVATIONC,TreeHt,DistanceB,SiteDistance4MinInf,SiteDistance4Min43,SiteDistance4Min1,SiteDistance4Min23,SiteDistance4Min12,SiteDistance4Min512,SiteDistance4Min410)
                    TempFilePC.write(str(DistanceB) + "," + str(ELEVATIONB) + "," + str(ObstructionHeightB) + "," + LUcodeB + "," + LANDUSECODEB + "\n")


                    DistanceA = DistanceB
                    ELEVATIONA = ELEVATIONB
                    ELEVATIONA = ELEVATIONB
                    ObstructionHeightA = ObstructionHeightB
                    LUcodeA = LUcodeB
                    LANDUSECODEA = LANDUSECODEB

                    DistanceB = DistanceC
                    ELEVATIONB = ELEVATIONC
                    ELEVATIONB = ELEVATIONC
                    ObstructionHeightB = ObstructionHeightC
                    LUcodeB = LUcodeC
                    LANDUSECODEB = LANDUSECODEC

            del TempFilePB_df
            TempFilePC.close()

            OpFreq = ""
            MaxDistance = float(Site2Distance)
            MaxDist1 = float(MaxDist1)
            MaxDist2 = float(MaxDist2)
            MaxDist3 = float(MaxDist3)
            MaxDist4 = float(MaxDist4)

            if(MaxDist1 >= MaxDistance):
                OpFreq = OpFreq1
            if(MaxDist2 >= MaxDistance):
                OpFreq = OpFreq2
            if(MaxDist3 >= MaxDistance):
                OpFreq = OpFreq3
            if(MaxDist4 >= MaxDistance):
                OpFreq = OpFreq4

            PathFreqFile.write(PathIndex + "," + OpFreq + "\n")
            if(OpFreq == ""):
                print("\nMaximum distance and operating frequency could not be found for path " + PathIndex + ".")
                print("Program is terminated.\n")
                self.endProgram()

            PathDataFile.write(PathIndex + "," + str(Site1Elevation) + "," + TwrHt1 + "," + str(Site2Elevation) + "," + TwrHt2 + "," + str(Site2Distance) + "\n")

        PathFreqFile.close()
        PathDataFile.close()

        self.endProgram()


    #2000 (never gets called)
    def evalPoint(distance,ELEVATION,ObstructionHeight,Eval,Site1Elevation,Site2Elevation,TwrHt1,TwrHt2,AntHt1,AntHt2,Site2Distance,SecondKFactor,ITURkFactor,FeetMeters,ALUkFactor,FirstKFactor,DLaneTest,FirstFresnelFraction,SecondFresnelFraction,PathEval,WorstCaseObst,OpFreq,AddlClearance,Test2Flag):

        distance = float(distance)
        ELEVATION = float(ELEVATION)
        ObstructionHeight = float(ObstructionHeight)

        if(Eval == 1):
            Site1AntennaElevation = float(Site1Elevation) + float(TwrHt1)
        if(Eval == 2):
            Site2AntennaElevation = float(Site2Elevation) + float(TwrHt2)
        if(Eval == 3):
            Site1AntennaElevation = float(Site1Elevation) + float(AntHt1)
        if(Eval == 4):
            Site2AntennaElevation = float(Site2Elevation) + float(AntHt2)

        Site1Distance = 0
        Site2Distance = float(Site2Distance)

        PathHeight = Site1AntennaElevation + (((Site2AntennaElevation - Site1AntennaElevation) / Site2Distance) * distance)

        PathDistanceA = float(distance)
        PathDistanceB = Site2Distance - PathDistanceA

        #Second (obstruction) K factor creation (ITU-R) or (ALU) modification
        SecondKFactorMod = SecondKFactor

        if(ITURkFactor == "Y"):
            PD = distance
            if(self.FeetMeters == "F"):
                PD = PD * 1.609344
            if(PD < 20):
                PD = 20
            if(PD > 200):
                PD = 200
            SecondKFactorMod = .80379426 + (.0029438097 * PD) - (6.1701657 / PD)
            SecondKFactorMod = SecondKFactorMod - (.000013619815 * PD * PD) + (10.375301 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod + (.000000022844768 * PD * PD * PD)

        if(ALUkFactor == "Y"):
            PD = distance
            if(self.FeetMeters == "M"):
                PD = PD / 1.609344
            if(PD < 25):
                PD = 25
            if(PD > 150):
                PD = 150

            if(ALUkFactor == 1):
                SecondKFactorMod = 1.3525442 - (.0025870465 * PD) - (13.402012 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000018703584 * PD * PD) + (148.40133 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000045263631 * PD * PD * PD)

            if(ALUkFactor == 2):
                SecondKFactorMod = 1.0561294 - (.0026434873 * PD) - (14.930824 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000025692173 * PD * PD) + (161.86573 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.00000007235408 * PD * PD * PD)

            if(ALUkFactor == 3):
                SecondKFactorMod = .82999889 - (.0015503296 * PD) - (13.665673 / PD)
                SecondKFactorMod = SecondKFactorMod + (.0000172027 * PD * PD) + (152.99299 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000046838057 * PD * PD * PD)

            if(ALUkFactor == 4):
                SecondKFactorMod = .6454992899999999 - (.00116752 * PD) - (11.930858 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000017371414 * PD * PD) + (156.48897 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000053622664 * PD * PD * PD)

        if(self.FeetMeters == "F"):
            EarthBulge1 = (PathDistanceA * PathDistanceB) / (1.5 * FirstKFactor)   #miles
        if(self.FeetMeters == "M"):
            EarthBulge1 = (PathDistanceA * PathDistanceB) / (12.75 * FirstKFactor)   #kilometers

        if(SecondKFactor != ""):
            if(self.FeetMeters == "F"):
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (1.5 * SecondKFactorMod)   #miles
            if(self.FeetMeters == "M"):
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (12.75 * SecondKFactorMod)  #kilometers

        if(DLaneTest == "Y"):
            if(self.FeetMeters == "F"):
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (1.5 * 1)   #miles
                EarthBulge2 = EarthBulge2 + 150
            if(self.FeetMeters == "M"):
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (12.75 * 1)  #kilometers
                EarthBulge2 = EarthBulge2 + (150 * .3048)

        if(self.FeetMeters == "F"):
            FirstFresnelZone = 72.1 * math.sqrt((PathDistanceA * PathDistanceB) / (OpFreq * Site2Distance))
        if(self.FeetMeters == "M"):
            FirstFresnelZone = 17.3 * math.sqrt((PathDistanceA * PathDistanceB) / (OpFreq * Site2Distance))


        #Test 1 first Fresnel zone (F1) clearance
        FirstFresnelTestHeight = FirstFresnelFraction * FirstFresnelZone

        #Test 2 first Fresnel zone (F1) clearance
        if(SecondKFactor != ""):
            SecondFresnelTestHeight = SecondFresnelFraction * FirstFresnelZone
        if(DLaneTest == "Y"):
            SecondFresnelTestHeight = 0

        #Test 1
        EarthHeight1 = ELEVATION + EarthBulge1
        if(PathEval == 1):
            EarthHeight1 = EarthHeight1 + ObstructionHeight
        if(PathEval == 2):
            EarthHeight1 = EarthHeight1 + WorstCaseObst

        ModifiedPathHeight1 = PathHeight - FirstFresnelTestHeight - AddlClearance
        Clearance1 = ModifiedPathHeight1 - EarthHeight1

        if(Clearance1 < 0):
            FailFlag = 1

        if(Test2Flag == 1):
            #Test 2
            EarthHeight2 = ELEVATION + EarthBulge2
            if(PathEval == 1):
                EarthHeight2 = EarthHeight2 + ObstructionHeight
            if(PathEval == 2):
                EarthHeight2 = EarthHeight2 + WorstCaseObst

            ModifiedPathHeight2 = PathHeight - SecondFresnelTestHeight - AddlClearance
            Clearance2 = ModifiedPathHeight2 - EarthHeight2

            if(Clearance2 < 0):
                FailFlag = 1

        #Calculate reflection points
        H1 = Site1AntennaElevation
        H2 = Site2AntennaElevation
        D1 = PathDistanceA  #to reflection point from left site
        D = Site2Distance   #total path distance

        if(self.FeetMeters == "F"):
            H1 = H1 * .3048
            H2 = H2 * .3048
            D1 = D1 * 1.609344
            D = D * 1.609344

        if(H2 > H1):
            HX = H1
            H1 = H2
            H2 = HX
            D1 = D - D1

        if((H1 != H2) and (D1 <= (D/2))):
            HRinf = "0.0"
            HR1 = "0.0"
            HR2 = "0.0"
            return

        if((H1 == H2) and (D1 <= (D / 2))):
            D1 = D - D1

        #K = infinity
        HRinf = (((H1 + H2) * D1) - (H1 * D)) / ((2 * D1) - D)
        if(self.FeetMeters == "F"):
            HRinf / .3048     #convert back to feet
        HRinf = str(HRinf)

        K = float(FirstKFactor)
        A = ((4 / 3) * (D1 * D1 * D1)) - (2 * D * D1 * D1) + (D * D * D1)
        B = K * (((H1 + H2) * D1) - (H1 * D))
        C = K * (D - (2 * D1))
        HR1 = (A - B) / C  #reflection plane elevation
        if(self.FeetMeters == "F"):
            HR1 = HR1 / .3048
        HR1 = str(HR1)

        HR2 = "0.0"
        if(Test2Flag == 1):
            K = float(SecondKFactor)
            if(DLaneTest == "Y"):
                K = 1
            A = ((4 / 3) * (D1 * D1 * D1)) - (2 * D * D1 * D1) + (D * D * D1)
            B = K * (((H1 + H2) * D1) - (H1 * D))
            C = K * (D - (2 * D1))
            HR2 = (A - B) / C  #reflection plane elevation
            if(self.FeetMeters == "F"):
                HR2 = HR2 / .3048
            HR2 = str(HR2)

        return


    #3000
    def addTrees(ELEVATIONA,ELEVATIONB,ELEVATIONC,TreeHt,DistanceB,SiteDistance4MinInf,SiteDistance4Min43,SiteDistance4Min1,SiteDistance4Min23,SiteDistance4Min12,SiteDistance4Min512,SiteDistance4Min410):

        #Put tree at path inflection point
        if((ELEVATIONA < ELEVATIONB) and (ELEVATIONB > ELEVATIONC)):
            ObstructionHeightB = str(TreeHt)
            LUcodeB = "T"
            LANDUSECODEB = "Tree"
        #Put trees at terrain points closest to path
        if((DistanceB == SiteDistance4MinInf) or (DistanceB == SiteDistance4Min43) or (DistanceB == SiteDistance4Min1) or (DistanceB == SiteDistance4Min23) or (DistanceB == SiteDistance4Min12) or (DistanceB == SiteDistance4Min512) or (DistanceB == SiteDistance4Min410)):
            ObstructionHeightB = str(TreeHt)
            LUcodeB = "T"
            LANDUSECODEB = "Tree"

        return

    #4000
    def findTerrain(self, Site1Elevation,TwrHt1,Site2Elevation,TwrHt2,Site2Distance,distance,MaxELEVATION,SiteHeight4MinInf,SiteHeight4Min43,SiteHeight4Min1,SiteHeight4Min23,SiteHeight4Min12,SiteHeight4Min512,SiteHeight4Min410):
        Site1AntennaElevation = float(Site1Elevation) + float(TwrHt1)
        Site1Distance = 0
        Site2AntennaElevation = float(Site2Elevation) + float(TwrHt2)
        Site2Distance = float(Site2Distance)

        PathDistance1 = float(distance)
        PathDistance2 = Site2Distance - PathDistance1
        PathHeight = Site1AntennaElevation + (((Site2AntennaElevation - Site1AntennaElevation) / Site2Distance) * PathDistance1)

        #K factor = infinity
        EarthCurve = 0
        EarthHeight = float(EarthCurve) + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4MinInf):
            SiteHeight4MinInf = DeltaHeight
            SiteDistance4MinInf = distance

        #K factor = 4/3
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (4 / 3))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (4 / 3))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min43):
            SiteHeight4Min43 = DeltaHeight
            SiteDistance4Min43 = distance

        #K factor = 1
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (1))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (1))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min1):
            SiteHeight4Min1 = DeltaHeight
            SiteDistance4Min1 = distance

        #K factor = 2/3
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (2 / 3))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (2 / 3))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min23):
            SiteHeight4Min23 = DeltaHeight
            SiteDistance4Min23 = distance

        #K factor = 1/2
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (1 / 2))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (1 / 2))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min12):
            SiteHeight4Min12 = DeltaHeight
            SiteDistance4Min12 = distance

        #K factor = 5/12
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (5 / 12))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (5 / 12))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min512):
            SiteHeight4Min512 = DeltaHeight
            SiteDistance4Min512 = distance

        #K factor = 4/10
        if(self.FeetMeters == "F"):
            EarthCurve = (PathDistance1 * PathDistance2) / (1.5 * (4 / 10))   #miles
        if(self.FeetMeters == "M"):
            EarthCurve = (PathDistance1 * PathDistance2) / (12.75 * (4 / 10))   #kilometers
        EarthHeight = EarthCurve + float(MaxELEVATION)
        DeltaHeight = PathHeight - EarthHeight
        if(DeltaHeight < SiteHeight4Min410):
            SiteHeight4Min410 = DeltaHeight
            SiteDistance4Min410 = distance

        return

    #5000
    def landUseConv(self, LANDUSECODE):
        LUcode = "N"
        if((LANDUSECODE == 1) or (10 < LANDUSECODE and LANDUSECODE < 20)):
            LUcode = "B"
        elif((LANDUSECODE == 2)or(20 < LANDUSECODE and LANDUSECODE < 30)or(LANDUSECODE == 3)or (30 < LANDUSECODE and LANDUSECODE < 40)or(LANDUSECODE == 5)or(50 < LANDUSECODE and LANDUSECODE < 60)or(LANDUSECODE == 6)or(60 < LANDUSECODE and LANDUSECODE < 70)or(LANDUSECODE == 7)or(70 < LANDUSECODE and LANDUSECODE < 80)or(LANDUSECODE == 8)or(80 < LANDUSECODE and LANDUSECODE < 90)or(LANDUSECODE == 9)or(90 < LANDUSECODE and LANDUSECODE < 100)):
            LUcode = "N"
        elif((LANDUSECODE == 4)or(40 < LANDUSECODE and LANDUSECODE < 50)or(LANDUSECODE == 61)or(LANDUSECODE == 82)or(LANDUSECODE == 85)):
            LUcode = "T"

        LANDUSECODESTR = "Unknown"

        if((LANDUSECODE == 1)or(LANDUSECODE == 18)or(LANDUSECODE == 18)):
            LANDUSECODESTR = "Urban or Built-Up Land"
        elif(LANDUSECODE == 11):
            LANDUSECODESTR = "Residential"
        elif(LANDUSECODE == 12):
            LANDUSECODESTR = "Commercial Services"
        elif(LANDUSECODE == 13):
            LANDUSECODESTR = "Industrial"
        elif(LANDUSECODE == 14):
            LANDUSECODESTR = "Transportation\Communications"
        elif(LANDUSECODE == 15):
            LANDUSECODESTR = "Industrial and Commercial"
        elif(LANDUSECODE == 16):
            LANDUSECODESTR = "Mixed Urban or Built-Up Land"
        elif(LANDUSECODE == 17):
            LANDUSECODESTR = "Other Urban or Built-Up Land"
        elif((LANDUSECODE == 2)or(LANDUSECODE == 25)or(LANDUSECODE == 26)or(LANDUSECODE == 27)or(LANDUSECODE == 28)or(LANDUSECODE == 29)):
            LANDUSECODESTR = "Agricultural Land"
        elif(LANDUSECODE == 21):
            LANDUSECODESTR = "Cropland and Pasture"
        elif(LANDUSECODE == 22):
            LANDUSECODESTR = "Orchards\\Groves\\Vineyards\\Nurseries"#print this out, idk if its right
        elif(LANDUSECODE == 23):
            LANDUSECODESTR = "Confined Feeding Operations"
        elif(LANDUSECODE == 24):
            LANDUSECODESTR = "Other Agricultural Land"
        elif((LANDUSECODE == 3)or(LANDUSECODE == 34)or(LANDUSECODE == 35)or(LANDUSECODE == 36)or(LANDUSECODE == 37)or(LANDUSECODE == 38)or(LANDUSECODE == 39)):
            LANDUSECODESTR = "Rangeland"
        elif(LANDUSECODE == 31):
            LANDUSECODESTR = "Herbaceous Rangeland"
        elif(LANDUSECODE == 32):
            LANDUSECODESTR = "Shrub and Brush Rangeland"
        elif(LANDUSECODE == 33):
            LANDUSECODESTR = "Mixed Rangeland"
        elif((LANDUSECODE == 4)or(LANDUSECODE == 44)or(LANDUSECODE == 45)or(LANDUSECODE == 46)or(LANDUSECODE == 47)or(LANDUSECODE == 48)or(LANDUSECODE == 49)):
            LANDUSECODESTR = "Forest Land"
        elif(LANDUSECODE == 41):
            LANDUSECODESTR = "Deciduous Forest Land"
        elif(LANDUSECODE == 42):
            LANDUSECODESTR = "Evergreen Forest Land"
        elif(LANDUSECODE == 43):
            LANDUSECODESTR = "Mixed Forest Land"
        elif((LANDUSECODE == 5)or(LANDUSECODE == 55)or(LANDUSECODE == 56)or(LANDUSECODE == 57)or(LANDUSECODE == 58)or(LANDUSECODE == 59)):
            LANDUSECODESTR = "Water"
        elif(LANDUSECODE == 51):
            LANDUSECODESTR = "Streams and Canals"
        elif(LANDUSECODE == 52):
            LANDUSECODESTR = "Lakes"
        elif(LANDUSECODE == 53):
            LANDUSECODESTR = "Reservoirs"
        elif(LANDUSECODE == 54):
            LANDUSECODESTR = "Bays and Estuaries"
        elif((LANDUSECODE == 6)or(LANDUSECODE == 63)or(LANDUSECODE == 64)or(LANDUSECODE == 65)or(LANDUSECODE == 66)or(LANDUSECODE == 67)or(LANDUSECODE == 68)or(LANDUSECODE == 69)):
            LANDUSECODESTR = "Rangeland"
        elif(LANDUSECODE == 61):
            LANDUSECODESTR = "Forested Wetlands"
        elif(LANDUSECODE == 62):
            LANDUSECODESTR = "Nonforested Wetlands"
        elif((LANDUSECODE == 7)or(LANDUSECODE == 78)or(LANDUSECODE == 79)):
            LANDUSECODESTR = "Barren Land"
        elif(LANDUSECODE == 71):
            LANDUSECODESTR = "Dry Salt Flats"
        elif(LANDUSECODE == 72):
            LANDUSECODESTR = "Beaches"
        elif(LANDUSECODE == 73):
            LANDUSECODESTR = "Sandy Areas Other than Beaches"
        elif(LANDUSECODE == 74):
            LANDUSECODESTR = "Bare Exposed Rock"
        elif(LANDUSECODE == 75):
            LANDUSECODESTR = "Strip Mines\Quarries\and Gravel Pits"
        elif(LANDUSECODE == 76):
            LANDUSECODESTR = "Transitional Areas"
        elif(LANDUSECODE == 77):
            LANDUSECODESTR = "Mixed Barren Land"
        elif((LANDUSECODE == 8)or(LANDUSECODE == 86)or(LANDUSECODE == 87)or(LANDUSECODE == 88)or(LANDUSECODE == 89)):
            LANDUSECODESTR = "Tundra"
        elif(LANDUSECODE == 81):
            LANDUSECODESTR = "Shrub and Brush Tundra"
        elif(LANDUSECODE == 82):
            LANDUSECODESTR = "Herbaceous Tundra"
        elif(LANDUSECODE == 83):
            LANDUSECODESTR = "Bare Ground"
        elif(LANDUSECODE == 84):
            LANDUSECODESTR = "Wet Tundra"
        elif(LANDUSECODE == 85):
            LANDUSECODESTR = "Mixed Tundra"
        elif((LANDUSECODE == 9)or(LANDUSECODE == 93)or(LANDUSECODE == 94)or(LANDUSECODE == 95)or(LANDUSECODE == 96)or(LANDUSECODE == 97)or(LANDUSECODE == 98)or(LANDUSECODE == 99)):
            LANDUSECODESTR = "Perennial Snow and Ice"
        elif(LANDUSECODE == 91):
            LANDUSECODESTR = "Perennial Snowfields"
        elif(LANDUSECODE == 92):
            LANDUSECODESTR = "Glaciers"

        return LUcode, LANDUSECODESTR


    #6000
    def calcDistance(self, LATITUDEA,LATITUDEB,LONGITUDEA,LONGITUDEB): #CALCULATE DISTANCE BETWEEN SITE A AND SITE B
        #INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
        #OUTPUT: Z# (DISTANCE IN MILES)
        PI = 3.1415926

        #USUAL FORMULA
        #Z# = SIN(PI# * LATITUDEA# / 180) * SIN(PI# * LATITUDEB# / 180)
        #Z# = Z# + COS(PI# * LATITUDEA# / 180) * COS(PI# * LATITUDEB# / 180) * COS(PI# * (LONGITUDEA# - LONGITUDEB#) / 180)
        #X# = Z#
        #GOSUB 6200 #ARCCOS(Z#)
        #ZLONG# = (180 / PI#) * ARCCOS#

        #HIGH ACCURACY FORMULA
        Z = pow((math.sin(PI * (LATITUDEA - LATITUDEB) / 180) / 2), 2)
        Z = Z + math.cos(PI * LATITUDEA / 180) * math.cos(PI * LATITUDEB / 180) * pow( (math.sin((PI * (LONGITUDEA - LONGITUDEB) / 180) / 2)), 2)
        Z = math.sqrt(Z)
        X = Z
        ARCSIN = self.arcSin(X, PI)

        ZSHORT = 2 * (180 / PI) * ARCSIN
        Zkm = 111.1 * ZSHORT #DISTANCE IN KILOMETERS
        Zmiles = 69.06 * ZSHORT #DISTANCE IN MILES

        return Zkm, Zmiles

    #6100
    def arcSin(self, X,PI):

        if(abs(X) > 1):
            XMOD = X / abs(X)
        else:
            XMOD = X

        if(XMOD == 1):
            ASIN = PI / 2
        if(XMOD == -1):
            ASIN = -PI / 2
        if(abs(XMOD) < 1):
            ASIN = math.atan(XMOD / math.sqrt(1 - (XMOD * XMOD)))

        ARCSIN = ASIN

        return ARCSIN

    #6200 (never gets called)
    def arcCos(X, PI):

        if(abs(X) > 1):
            XMOD = X / abs(X)
        else:
            XMOD = X

        if(XMOD == 1):
            ACOS = 0

        if(XMOD == -1):
            ACOS = PI

        if(abs(XMOD) < 1):
            ACOS = (PI / 2) - math.atan(XMOD / math.sqrt(1 - (XMOD * XMOD)))

        ARCCOS = ACOS
        return ARCCOS

    #8000 (never gets called)
    def optimizeTower(TwrHtFlag,START1,END1,START2,END2,FolderPath,ProfileNumber,Site1Elevation,Site2Elevation,TwrHt1,TwrHt2,Site2Distance,SecondKFactor,ITURkFactor,ALUkFactor,FirstKFactor,DLaneTest,FirstFresnelFraction,SecondFresnelFraction,PathEval,WorstCaseObst,OpFreq,AddlClearance,Test2Flag):

        if(TwrHtFlag == 0):
            IISTART = START1
            IIEND = END1

        if(TwrHtFlag == 1):
            IISTART = START2
            IIEND = END2

        II = IISTART
        for II in range(IIEND):
            if(TwrHtFlag == 0):
                AntHt1 = IIEND& - II + IISTART
                if(self.FeetMeters == "M"):
                    AntHt1 = AntHt1 / 4
                AntHt2 = TwrHt2

            if(TwrHtFlag == 1):
                AntHt2 = IIEND& - II + IISTART
                if(self.FeetMeters == "M"):
                    AntHt2 = AntHt2 / 4
                AntHt1 = TwrHt1

            FileName = self.FolderPath + "\TempFile\PC" + ProfileNumber + ".CSV" #11
            pc_df = pd.read_csv(FileName, header=None)
            PointCount = 0
            FailFlag = 0

            for index, pcRow in pc_df.iterrows():
                EndOfFile =  (index == pc_df.index[-1])

                PointCount = PointCount + 1
                distance = pcRow[0]
                ELEVATION = pcRow[1]
                ObstructionHeight = pcRow[2]
                LUcode = pcRow[3]
                LANDUSECODE = pcRow[4]
            #957
                if(PointCount == 1):
                    continue
                if(EndOfFile):
                    continue
                else:
                    Eval = 2
                    evalPoint(distance,ELEVATION,ObstructionHeight,Eval,Site1Elevation,Site2Elevation,TwrHt1,TwrHt2,AntHt1,AntHt2,Site2Distance,SecondKFactor,ITURkFactor,self.FeetMeters,ALUkFactor,FirstKFactor,DLaneTest,FirstFresnelFraction,SecondFresnelFraction,PathEval,WorstCaseObst,OpFreq,AddlClearance,Test2Flag)

            del pc_df

            if(FailFlag == 0):
                WGrun = AntHt1 + AntHt2
                if(WGrun < ShortestWGrun):
                    ShortestWGrun = WGrun
                    ShortestAntHt1 = AntHt1
                    ShortestAntHt2 = AntHt2
                    ShortestAntHt1 = int((ShortestAntHt1 * 100) + .5)
                    ShortestAntHt1 = ShortestAntHt1 / 100
                    ShortestAntHt1 = str(ShortestAntHt1)
                    ShortestAntHt2 = int((ShortestAntHt2 * 100) + .5)
                    ShortestAntHt2 = ShortestAntHt2 / 100
                    ShortestAntHt2 = str(ShortestAntHt2)

            PerCent = 100 * (II / IIEND)
            PerCent = int((PerCent * 100) + .5)
            PerCent = PerCent / 100
            PerCent = str(PerCent)
            AntHt1 = str(AntHt1)
            AntHt2 = str(AntHt2)

            if(FailFlag == 0):
                Info = "Path Clear"
            if(FailFlag == 1):
                Info = "Path Obstructed"
            print("Path " + str(ProfileNumber) + " optimization =  " + PerCent + "%, (AntHt1 = " + AntHt1 + ", AntHt2 = " + AntHt2 + "," + str(Info) + ")")
            if(FailFlag == 1):
                break

        return

    #9000
    def initializeSubroutine(self, Criteria):

        inpFile = open(Criteria, "r")
        ans = []
        counter = 0

        for line in inpFile:
            currentline = line.split(",")
            if (counter == 6 or counter == 22):
                counter+=1
                continue

            if (counter == 7):
                ans.append(currentline[1])
                counter+=1
                continue

            ans.append(currentline[0])


            if(counter >= 8 and counter <= 13):
                ans.append(currentline[1])
                counter+=1

            counter += 1

        inpFile.close()
        ans.append(1000)#MaxDist1

        return ans

    #9999
    def endProgram(self):
        print("\nProgram Completed")
        # input("\nPress <Enter> key to clear this window")
        # sys.exit()

    ################################################# Start ###################################################



    def executeProgram(self):
        print("Reading <Criteria.ini> initialization file.\n")
        Criteria = (str(self.FolderPath) + "\Criteria.ini")
        self.Answers = self.initializeSubroutine(Criteria) #9000
        self.FeetMeters = self.Answers[3]
        if (self.FeetMeters == "f"):
            self.FeetMeters = "F"
        elif (self.FeetMeters == "m"):
            self.FeetMeters = "M"
        if (self.FeetMeters == "F" or self.FeetMeters == "M"):
            pass
        else:
            print("Fourth line of <Criteria.ini> not understood.")
            print("Line should be F or M.")
            print(" Program; Terminated.")
            self.endProgram()#9999

        if(self.CompChoice == 1):
            self.MaxDataPointsN = 1
            self.DistanceFraction = None
            self.makeFiles(self.FolderPath, self.Answers, self.LandUse, self.MaxDataPointsN, self.DistanceFraction)

        if(self.CompChoice == 2):
            self.MaxDataPointsN = 1
            # self.DistanceFraction = input("\nEnter approximate fraction of a mile or kilometer for path increments\n")
            self.makeFiles(self.FolderPath, self.Answers, self.LandUse, self.MaxDataPointsN, self.DistanceFraction)

        if(self.CompChoice == 3):
            self.DistanceFraction = None
            # print("\nEnter approximate maximum number of path profile data points (N).")
            # self.MaxDataPointsN = input("The final profile number of points will be between N and 2N ")
            self.makeFiles(self.FolderPath, self.Answers, self.LandUse, self.MaxDataPointsN, self.DistanceFraction)


# ### Test call the modules ###
# testPathA = PathsA()
# testPathA.setFolderPath("C:/Users/sixpa/tdx/ExampleStep2BN")
# testPathA.setLULC("Y")
# testPathA.setCompressionOption(1)
# testPathA.executeProgram()
# testPathA.makeFiles(self.FolderPath,Answers,LandUse,MaxDataPointsN,DistanceFraction)
