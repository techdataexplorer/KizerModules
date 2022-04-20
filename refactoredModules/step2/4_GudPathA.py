import math
from queue import Empty
import sys
import os
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class GudPath(object):

    # constructor
    def __init__(self):
        # initialize the class attributes
        self.ExampleS2AFolderPath = ""
        self.FeetMeters = ""
        self.LandUse = "Y"
        self.OptimizePaths = "Y"
        self.SysOpt = "N"
        self.SysFail = "N"
        self.SysPass = "N"
        self.DLaneTest = ""
        self.FirstFresnelFraction = float("inf")
        self.FirstKFactor = float("inf")
        self.SecondFresnelFraction = float("inf")
        self.ITURkFactor = "N"
        self.ALUkFactor = 0
        self.ALUkFactorInput = "N"
        self.PathEval = 1
        self.WorstCaseObst = float("inf")
        self.Eval = 1
        self.Site1Elevation = float("inf")
        self.Site2Elevation = float("inf")
        self.ProfileNumberFilePath = ""
        self.TwrHt1 = float("inf")
        self.TwrHt2 = float("inf")
        self.Site2Distance = float("inf")
        self.OpFreq = float("inf")
        self.AntHt1 = float("inf")
        self.AntHt2 = float("inf")
        self.WGrun = float("inf")
        self.TwrHtFlag = float("inf")
        self.ShortestAntHt1 = float("inf")
        self.ShortestAntHt2 = float("inf")
        self.START1 = float("inf")
        self.START2 = float("inf")
        self.END1 = float("inf")
        self.END2 = float("inf")
        self.IISTART = float("inf")
        self.IIEND = float("inf")
        self.int_IIEND = float("inf")
        self.ProfileNumber = ""
        self.PerCent = float("inf")
        self.SITE1 = ""
        self.ObstructionHeight = float("inf")
        self.AddlClearance = float("inf")
        self.SecondKFactor = float("inf")
        self.Test2Flag = 0


    # Handle invalid values when assigning float
    def assignFloat(self, value):
        try:
            return float(value)
        except ValueError:
            return float("inf")

    # Handle invalid cases when assigning Y or N
    def assignYN(self, value):
        try:
            if str(value) == "":
                return "N"
            return str(value)
        except ValueError:
            print("Invalid value. Only 'Y' or 'N'")

    # Handle invalid cases when assigning Miles('M') or Kilometers('K')
    def assignMK(self, value):
        try:
            if str(value) == "":
                return "N"
            return str(value)
        except ValueError:
            print("Invalid value. Only 'M' or 'K'")

    # Handle invalid cases when assigning Feet('F') or Meters('M')
    def assignFM(self, value):
        try:
            if str(value) == "":
                sys.exit()
            return str(value).upper()
        except ValueError:
            print("Invalid value. Only 'F' or 'M'")
            print("Fourth line of <Criteria.ini> not understood.")
            print("Line should be F or M.")
            print("Program Terminated.")
            sys.exit()



    # Setter
    def setFolderPath(self, folderPath):
        self.ExampleS2AFolderPath = str(folderPath)

    def setLULC(self, landUse):
        self.landUse = str(landUse).upper()

    def setPathEval(self, pathEval):
        self.PathEval = int(pathEval)

    def setOptimizePathsOption(self, optimizeOption):
        self.OptimizePaths = str(optimizeOption).upper()

    def endProgram(self):
        sys.exit()


    def iniFileReader(self, iniFilePath): #9000

        fileData = []
        inputFile = open(iniFilePath, "r")
        counter = 0

        for line in inputFile:
            currentline = line.split(",")
            if (counter == 6 or counter == 22):
                counter+=1
                continue
            if (counter == 7):
                fileData.append(currentline[1])
                counter+=1
                continue

            fileData.append(currentline[0])

            if(counter >= 8 and counter <= 13):
                fileData.append(currentline[1])
                counter+=1

            counter += 1


        inputFile.close()

        fileData.append(1000)#MaxDist1

        return fileData




    def configResults(self, iniFileDataObj, pathEval, ALUkFactor, worstCaseObst):

        distanceUnit = " ."
        worstCaseObst = max(iniFileDataObj["buildingHeight"], iniFileDataObj["treeHeight"])

        if pathEval == 1:
            print("\nPath profile obstructions with assumed heights will be used for evaluations.\n")

        if pathEval == 2:
            print("\nAssumed tree (or building worst case) height will be used for evaluations.\n")

        if iniFileDataObj["DLaneTest"] != "N":
            iniFileDataObj["DLaneTest"] = "Y"


        if iniFileDataObj["secondFresnelFraction"] != float("inf") or iniFileDataObj["DLaneTest"] == "Y":
            self.Test2Flag = 1

        print("\nPath evaluation criteria will be the following:")


        if iniFileDataObj["heightElevationUnit"] == "F":
            distanceUnit = " miles."
        if iniFileDataObj["heightElevationUnit"] == "M":
            distanceUnit = " km."

        print("Maximum distance for " + str(iniFileDataObj["frequency1"]) + " GHz is " + str(iniFileDataObj["maxDist1"]) + distanceUnit)
        print("Maximum distance for " + str(iniFileDataObj["frequency2"]) + " GHz is " + str(iniFileDataObj["maxDist2"]) + distanceUnit)
        print("Maximum distance for " + str(iniFileDataObj["frequency3"]) + " GHz is " + str(iniFileDataObj["maxDist3"]) + distanceUnit)
        print("Maximum distance for " + str(iniFileDataObj["frequency4"]) + " GHz is " + str(iniFileDataObj["maxDist4"]) + distanceUnit)


        print(str(iniFileDataObj["firstFresnelFraction"]) + " of first Fresnel zone at K factor of " + str(iniFileDataObj["firstKFactor"]))

        if iniFileDataObj["secondKFactor"] != float("inf") and iniFileDataObj["DLaneTest"] != "Y":
            print(str(iniFileDataObj["secondFresnelFraction"]) + " of second Fresnel zone at K factor of " + str(iniFileDataObj["secondKFactor"]))

        if iniFileDataObj["DLaneTest"] == "Y":
            print("150 feet plus grazing at K = 1")

        if iniFileDataObj["addlClearance"] != float("inf") and iniFileDataObj["heightElevationUnit"] == "F":
            print(str(iniFileDataObj["secondFresnelFraction"]) + " feet will be added to the above criteria")

        if iniFileDataObj["addlClearance"] != float("inf") and iniFileDataObj["heightElevationUnit"] == "M":
            print(str(iniFileDataObj["secondFresnelFraction"]) + " meters will be added to the above criteria")

        print()

        if iniFileDataObj["firstKFactor"] == float("inf"):
            print("The First Test K factor is missing.  It is required to procdeed.\n")
            sys.exit()


        if iniFileDataObj["ALUkFactor"] == "Y":

            TestValue = math.abs(float(iniFileDataObj["secondKFactor"]) - 1)

            if TestValue < .000001:
                ALUkFactor = 1

            TestValue = math.abs(float(iniFileDataObj["secondKFactor"]) - .66666667)

            if TestValue < .000001:
                ALUkFactor = 2

            TestValue = math.abs(float(iniFileDataObj["secondKFactor"]) - .5)

            if TestValue < .000001:
                ALUkFactor = 3

            TestValue = math.abs(float(iniFileDataObj["secondKFactor"]) - .4)

            if TestValue < .000001:
                ALUkFactor = 4

            if ALUkFactor == 0:
                print("ALU relaxation factor can only be applied to the following secondary K factors:")
                print("1, 2/3, 1/2, 4/10")
                print("The following defined value does not match any above value")
                print("Second K Factor = " + str(iniFileDataObj["secondKFactor"]))
                print("The program is terminated")
                sys.exit()



    # KML map generator for paths and sites (took out delorme and mapinfo code)
    def createKML(self, InputFileSites, InputFilePaths, OutputFileGoogle):

        # Google Earth KML generator for paths and sites ************************************************************* line 918
        input_file_paths_df = pd.read_csv(InputFilePaths, header=None)      #1
        input_file_sites_df = pd.read_csv(InputFileSites, header=None)      #2
        output_file_google_df = open(OutputFileGoogle, "w")      #4

        output_file_google_df.write("<?xml version=" + chr(34) + "1.0" + chr(34) + " encoding=" + chr(34) + "UTF-8" + chr(34) + "?>" + "\n")
        output_file_google_df.write("<kml xmlns=" + chr(34) + "http://earth.google.com/kml/2.2" + chr(34) + ">" + "\n")
        output_file_google_df.write("<Document>" + "\n")
        output_file_google_df.write(" <name>Path Profile File.kml</name>" + "\n")
        output_file_google_df.write("" + "\n")
        output_file_google_df.write(" <StyleMap id=" + chr(34) + "msn_placemark_circle" + chr(34) + ">" + "\n")
        output_file_google_df.write("     <Pair>" + "\n")
        output_file_google_df.write("     <key>normal</key>" + "\n")
        output_file_google_df.write("     <styleUrl>#sn_placemark_circle</styleUrl>" + "\n")
        output_file_google_df.write("     </Pair>" + "\n")
        output_file_google_df.write("     <Pair>" + "\n")
        output_file_google_df.write("     <key>highlight</key>" + "\n")
        output_file_google_df.write("     <styleUrl>#sh_placemark_circle_highlight</styleUrl>" + "\n")
        output_file_google_df.write("     </Pair>" + "\n")
        output_file_google_df.write(" </StyleMap>" + "\n")
        output_file_google_df.write("" + "\n")
        output_file_google_df.write(" <Style id=" + chr(34) + "sn_placemark_circle" + chr(34) + ">" + "\n")
        output_file_google_df.write("     <IconStyle>" + "\n")
        output_file_google_df.write("     <scale>1.2</scale>" + "\n")
        output_file_google_df.write("     <color>ff3300ff</color>" + "\n")
        output_file_google_df.write("     <Icon>" + "\n")
        output_file_google_df.write("     <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>" + "\n")
        output_file_google_df.write("     </Icon>" + "\n")
        output_file_google_df.write("     </IconStyle>" + "\n")
        output_file_google_df.write("     <ListStyle>" + "\n")
        output_file_google_df.write("     </ListStyle>" + "\n")
        output_file_google_df.write(" </Style>" + "\n")
        output_file_google_df.write("" + "\n")
        output_file_google_df.write(" <Folder>" + "\n")
        output_file_google_df.write("     <name>Temporary Places</name>" + "\n")
        output_file_google_df.write("     <open>1</open>" + "\n")


        for index, row in input_file_sites_df.iterrows():
            self.SITE1 = row[0]
            LAT1 = row[1]
            LON1 = row[2]

            output_file_google_df.write("" + "\n")
            output_file_google_df.write("     <Placemark>" + "\n")
            output_file_google_df.write("     <name>" + str(self.SITE1) + "</name>" + "\n")
            output_file_google_df.write("     <address>Site Address</address>" + "\n")
            output_file_google_df.write("     <description>Other Information</description>" + "\n")
            output_file_google_df.write("     <styleUrl>#msn_placemark_circle</styleUrl>" + "\n")
            output_file_google_df.write("     <Point>" + "\n")
            output_file_google_df.write("     <coordinates>" + str(LON1) + "," + str(LAT1) + ",0</coordinates>" + "\n")
            output_file_google_df.write("     </Point>" + "\n")
            output_file_google_df.write("     </Placemark>" + "\n")

        output_file_google_df.write("" + "\n")
        output_file_google_df.write("     <name>Temporary Places</name>" + "\n")
        output_file_google_df.write("     <open>1</open>" + "\n")
        output_file_google_df.write("" + "\n")
        output_file_google_df.write(" <Style id=" + chr(34) + "msn_placemark_circle" + chr(34) + ">" + "\n")
        output_file_google_df.write("     <LineStyle>" + "\n")
        output_file_google_df.write("     <color>ffff0033</color>" + "\n")
        output_file_google_df.write("     <width>4</width>" + "\n")
        output_file_google_df.write("     </LineStyle>" + "\n")
        output_file_google_df.write(" </Style>" + "\n")

        for index, row in input_file_paths_df.iterrows():
            self.SITE1 = row[1]
            LAT1 = row[2]
            LON1 = row[3]
            LAT2 = row[5]
            LON2 = row[6]

            output_file_google_df.write("" + "\n")
            output_file_google_df.write("     <Placemark>" + "\n")
            output_file_google_df.write("     <name>Untitled Path</name>" + "\n")
            output_file_google_df.write("     <styleUrl>#msn_placemark_circle</styleUrl>" + "\n")
            output_file_google_df.write("     <LineString>" + "\n")
            output_file_google_df.write("     <tessellate>1</tessellate>" + "\n")
            output_file_google_df.write("     <coordinates>" + "\n")
            output_file_google_df.write("     " + str(LON1) + "," + str(LAT1) + ",0 " + str(LON2) + "," + str(LAT2) + ",0 </coordinates>" + "\n")
            output_file_google_df.write("     </LineString>" + "\n")
            output_file_google_df.write("     </Placemark>" + "\n")

        output_file_google_df.write("" + "\n")
        output_file_google_df.write(" </Folder>" + "\n")
        output_file_google_df.write("" + "\n")
        output_file_google_df.write("</Document>" + "\n")
        output_file_google_df.write("</kml>" + "\n")

        output_file_google_df.close()  # CLOSE #4
        return


    # 2000  'Evaluate each point on the path
    def point_on_path(self, distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag):

        if self.Eval == 1:
            Site1AntennaElevation = float(self.Site1Elevation) + float(self.TwrHt1)
            Site2AntennaElevation = float(self.Site2Elevation) + float(self.TwrHt2)
        if self.Eval == 2:
            Site1AntennaElevation = float(self.Site1Elevation) + float(self.AntHt1)
            Site2AntennaElevation = float(self.Site2Elevation) + float(self.AntHt2)


        PathHeight = Site1AntennaElevation + (((Site2AntennaElevation - Site1AntennaElevation) / self.Site2Distance) * distance)

        PathDistanceA = distance
        PathDistanceB = self.Site2Distance - PathDistanceA

        # Second (obstruction) K factor creation (ITU-R) or (ALU) modification
        SecondKFactorMod = float(SecondKFactor)

        if ITURkFactor == "Y":
            PD = distance
            if self.FeetMeters == "F": PD = PD * 1.609344
            if PD < 20: PD = 20
            if PD > 200: PD = 200
            SecondKFactorMod = .80379426 + (.0029438097 * PD) - (6.1701657 / PD)
            SecondKFactorMod = SecondKFactorMod - (.000013619815 * PD * PD) + (10.375301 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod + (.000000022844768 * PD * PD * PD)

        if self.ALUkFactorInput == "Y":
            PD = distance
            if self.FeetMeters == "M": PD = PD / 1.609344
            if PD < 25: PD = 25
            if PD > 150: PD = 150

            if self.ALUkFactor == 1:
                SecondKFactorMod = 1.3525442 - (.0025870465 * PD) - (13.402012 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000018703584 * PD * PD) + (148.40133 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000045263631 * PD * PD * PD)

            if self.ALUkFactor == 2:
                SecondKFactorMod = 1.0561294 - (.0026434873 * PD) - (14.930824 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000025692173 * PD * PD) + (161.86573 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.00000007235408 * PD * PD * PD)

            if self.ALUkFactor == 3:
                SecondKFactorMod = .82999889 - (.0015503296 * PD) - (13.665673 / PD)
                SecondKFactorMod = SecondKFactorMod + (.0000172027 * PD * PD) + (152.99299 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000046838057 * PD * PD * PD)

            if self.ALUkFactor == 4:
                SecondKFactorMod = .6454992899999999 - (.00116752 * PD) - (11.930858 / PD)
                SecondKFactorMod = SecondKFactorMod + (.000017371414 * PD * PD) + (156.48897 / (PD * PD))
                SecondKFactorMod = SecondKFactorMod - (.000000053622664 * PD * PD * PD)


        # Test 1 K factor Earth Bulge
        if self.FeetMeters == "F": EarthBulge1 = (float(PathDistanceA) * float(PathDistanceB)) / (1.5 * float(self.FirstKFactor))   # miles
        if self.FeetMeters == "M": EarthBulge1 = (float(PathDistanceA) * float(PathDistanceB)) / (12.75 * float(self.FirstKFactor))   # kilometers

        # Test 2 K factor Earth Bulge
        if SecondKFactor != float("inf"):
            if self.FeetMeters == "F": EarthBulge2 = (float(PathDistanceA) * float(PathDistanceB)) / (1.5 * SecondKFactorMod)   # miles
            if self.FeetMeters == "M": EarthBulge2 = (float(PathDistanceA) * float(PathDistanceB)) / (12.75 * SecondKFactorMod)  # kilometers


        # Alternate Test 2 Earth Bulge = 150 feet plus grazing (0 F1) at k = 1
        if self.DLaneTest == "Y":
            if self.FeetMeters == "F":
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (1.5 * 1)   # miles
                EarthBulge2 = EarthBulge2 + 150
            if self.FeetMeters == "M":
                EarthBulge2 = (PathDistanceA * PathDistanceB) / (12.75 * 1)  # kilometers
                EarthBulge2 = EarthBulge2 + (150 * .3048)


        if self.FeetMeters == "F": FirstFresnelZone = 72.1 * math.sqrt((PathDistanceA * PathDistanceB) / (self.OpFreq * self.Site2Distance))
        if self.FeetMeters == "M": FirstFresnelZone = 17.3 * math.sqrt((PathDistanceA * PathDistanceB) / (self.OpFreq * self.Site2Distance))

        # Test 1 first Fresnel zone (F1) clearance
        FirstFresnelTestHeight = float(self.FirstFresnelFraction) * float(FirstFresnelZone)

        # Test 2 first Fresnel zone (F1) clearance
        if SecondKFactor != float("inf"): SecondFresnelTestHeight = float(self.SecondFresnelFraction) * float(FirstFresnelZone)
        if self.DLaneTest == "Y": SecondFresnelTestHeight = 0

        # Test 1
        EarthHeight1 = ELEVATION + EarthBulge1

        if int(self.PathEval) == 1: EarthHeight1 = float(EarthHeight1) + float(ObstructionHeight)
        if int(self.PathEval) == 2: EarthHeight1 = float(EarthHeight1) + float(self.WorstCaseObst)

        ModifiedPathHeight1 = PathHeight - FirstFresnelTestHeight - float(AddlClearance)
        Clearance1 = ModifiedPathHeight1 - EarthHeight1

        if Clearance1 < -1: FailFlag = 1

        if Test2Flag == 1:
            # Test 2
            EarthHeight2 = float(ELEVATION) + float(EarthBulge2)
            if int(self.PathEval) == 1: EarthHeight2 = float(EarthHeight2) + float(ObstructionHeight)
            if int(self.PathEval) == 2: EarthHeight2 = float(EarthHeight2) + float(self.WorstCaseObst)
            ModifiedPathHeight2 = float(PathHeight) - float(SecondFresnelTestHeight) - float(AddlClearance)
            Clearance2 = ModifiedPathHeight2 - EarthHeight2
            if Clearance2 < -1: FailFlag = 1


        return Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone   # add return values



    def optimize_one_tower(self, ShortestWGrun):

        if self.TwrHtFlag == 0:
            self.IISTART = self.START1
            self.IIEND = self.END1

        if self.TwrHtFlag == 1:
            self.IISTART = self.START2
            self.IIEND = self.END2

        #FOR II = IISTART TO IIEND
        self.int_IIEND = int(self.IIEND)
        for II in range(self.IISTART, self.int_IIEND):
            if self.TwrHtFlag == 0:
                self.AntHt1 = self.IIEND - II + self.IISTART
                if self.FeetMeters == "M": self.AntHt1 = self.AntHt1 / 4
                self.AntHt2 = self.TwrHt2

            if self.TwrHtFlag == 1:
                self.AntHt2 = self.IIEND - II + self.IISTART
                if self.FeetMeters == "M": self.AntHt2 = self.AntHt2 / 4
                self.AntHt1 = self.TwrHt1

            #OPEN SysDataDrive$ + ":\" + Folder$ + "\TempFile\PC" + ProfileNumber$ + ".csv" FOR INPUT AS #11
            self.ProfileNumberFilePath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"
            profile_num_df = pd.read_csv(self.ProfileNumberFilePath, header=None)       #11

            PointCount = 0
            FailFlag = 0

            for index, row in profile_num_df.iterrows():
                PointCount = PointCount + 1

                distance = row[0]
                ELEVATION = row[1]
                self.ObstructionHeight = row[2]

                if PointCount == 1: continue    #GOTO 8400

                self.Eval = 2

                # call 2000 function here #### GOSUB 2000 # not sure why this is called here
                Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

            if FailFlag == 0:
                self.WGrun = self.AntHt1 + self.AntHt2
                if self.WGrun < ShortestWGrun:
                    ShortestWGrun = self.WGrun
                    self.ShortestAntHt1 = self.AntHt1
                    self.ShortestAntHt2 = self.AntHt2
                    self.ShortestAntHt1 = float((self.ShortestAntHt1 * 100) + .5)
                    self.ShortestAntHt1 = self.ShortestAntHt1 / 100
                    self.ShortestAntHt1 = str(self.ShortestAntHt1)
                    self.ShortestAntHt2 = float((self.ShortestAntHt2 * 100) + .5)
                    self.ShortestAntHt2 = self.ShortestAntHt2 / 100
                    self.ShortestAntHt2 = str(self.ShortestAntHt2)

            self.PerCent = 100 * (II / self.IIEND)
            self.PerCent = float((self.PerCent * 100) + .5)
            self.PerCent = self.PerCent / 100
            self.PerCent = str(self.PerCent)
            self.AntHt1 = str(self.AntHt1)
            self.AntHt2 = str(self.AntHt2)

            if FailFlag == 0: Info = "Path Clear"
            if FailFlag == 1: Info = "Path Obstructed"

            print("Path " + str(self.ProfileNumber) + " optimization =  " + str(self.PerCent) + "%, (AntHt1 = " + str(self.AntHt1) + ", AntHt2 = " + str(self.AntHt2) + "," + str(Info) + ")")

            if FailFlag == 1: break     # GOTO 8500

        return


    def execute(self):

        print("\nReading <Criteria.ini> initialization file.\n")

        # 9000 Initialization subroutine, inserted here instead of calling the function
        CriteriaFilePath = self.ExampleS2AFolderPath + "/Criteria.ini"
        iniFileData = self.iniFileReader(CriteriaFilePath) #9000


        iniFileDataObj = {
            "fileName": iniFileData[0], # string
            "containTowerHeight": self.assignYN(iniFileData[1]), # yes/no
            "distanceUnit": self.assignMK(iniFileData[2]), # miles/km
            "heightElevationUnit": self.assignFM(iniFileData[3]), # originally-self.Feet-Meters
            "buildingHeight": self.assignFloat(iniFileData[4]),
            "treeHeight": self.assignFloat(iniFileData[5]),
            "frequency1": self.assignFloat(iniFileData[6]),
            "frequency2": self.assignFloat(iniFileData[8]),
            "frequency3": self.assignFloat(iniFileData[10]),
            "frequency4": self.assignFloat(iniFileData[12]),
            "maxDist1": float(1000),
            "maxDist2": self.assignFloat(iniFileData[7]),
            "maxDist3": self.assignFloat(iniFileData[9]),
            "maxDist4": self.assignFloat(iniFileData[11]),
            "firstFresnelFraction":  self.assignFloat(iniFileData[13]),
            "secondFresnelFraction":  self.assignFloat(iniFileData[15]),
            "firstKFactor":  self.assignFloat(iniFileData[14]),
            "secondKFactor":  self.assignFloat(iniFileData[16]),
            "DLaneTest":  self.assignYN(iniFileData[17]),
            "addlClearance":  self.assignFloat(iniFileData[18]),
            "ITURkFactor": self.assignYN(iniFileData[19]),
            "ALUkFactor": self.assignYN(iniFileData[20])
        }

        TheDataFile = iniFileDataObj["fileName"]
        TowerHt     = iniFileDataObj["containTowerHeight"]
        MilesKm     = iniFileDataObj["distanceUnit"]
        self.FeetMeters = iniFileDataObj["heightElevationUnit"]
        BuildingHt  = iniFileDataObj["buildingHeight"]
        TreeHt      = iniFileDataObj["treeHeight"]
        MaxDist1    = 1000
        OpFreq1     = iniFileDataObj["frequency1"]
        MaxDist2    = iniFileDataObj["maxDist2"]
        OpFreq2     = iniFileDataObj["frequency2"]
        MaxDist3    = iniFileDataObj["maxDist3"]
        OpFreq3     = iniFileDataObj["frequency3"]
        MaxDist4    = iniFileDataObj["maxDist4"]
        OpFreq4     = iniFileDataObj["frequency4"]
        self.FirstFresnelFraction   = iniFileDataObj["firstFresnelFraction"]
        self.FirstKFactor           = iniFileDataObj["firstKFactor"]
        self.SecondFresnelFraction  = iniFileDataObj["secondFresnelFraction"]
        self.SecondKFactor          = iniFileDataObj["secondKFactor"]
        self.DLaneTest              = iniFileDataObj["DLaneTest"]
        self.AddlClearance          = iniFileDataObj["addlClearance"]

        if self.AddlClearance == float("inf"):
            self.AddlClearance = 0

        self.ITURkFactor    = iniFileData[19]
        self.ALUkFactorInput= iniFileData[20]


        # open all of the output files
        PassStatFilePath = self.ExampleS2AFolderPath + "/Passed/PassStat.csv"        #51
        pass_stat_df = open(PassStatFilePath, "w+")

        FailStatFilePath = self.ExampleS2AFolderPath + "/Passed/FailStat.csv"        #52
        fail_stat_df = open(FailStatFilePath, "w+")

        PassSiteFilePath = self.ExampleS2AFolderPath + "/Passed/PassSite.csv"        #56
        pass_site_df = open(PassSiteFilePath, "w+")

        PassPathFilePath = self.ExampleS2AFolderPath + "/Passed/PassPath.csv"        #57
        pass_path_df = open(PassPathFilePath, "w+")

        FailSiteFilePath = self.ExampleS2AFolderPath + "/Passed/FailSite.csv"        #58
        fail_site_df = open(FailSiteFilePath, "w+")

        FailPathFilePath = self.ExampleS2AFolderPath + "/Passed/FailPath.csv"        #59
        fail_path_df = open(FailPathFilePath, "w+")



        self.configResults(iniFileDataObj, self.PathEval, self.ALUkFactor, self.WorstCaseObst)


        # self.OptimizePaths = input("After evaluating the paths do you want to optimize the good paths (Y or N)\n")
        # self.OptimizePaths = self.OptimizePaths.upper()

        FinalPathData = self.ExampleS2AFolderPath + "/Optimize/PathInfo.csv"
        if self.OptimizePaths == "Y":
            final_path_data_df = open(FinalPathData, "w+")      #14

        FailedPathData = self.ExampleS2AFolderPath + "/Failed/PathInfo.csv"
        failed_path_data_df = open(FailedPathData, "w+")        #15

        PassedPathData = self.ExampleS2AFolderPath + "/Passed/PathInfo.csv"
        passed_path_data_df = open(PassedPathData, "w+")        #16

        # Open the file with the path definition data
        PathFileFilePath = self.ExampleS2AFolderPath + "/" + TheDataFile + ".csv"
        data_file_df = pd.read_csv(PathFileFilePath)            #10

        # Begin path profile evaluation
        Headers = list(data_file_df.columns)
        HEADER1 = Headers[0]
        HEADER2 = Headers[1]
        HEADER3 = Headers[2]
        HEADER4 = Headers[3]
        HEADER5 = Headers[4]
        HEADER6 = Headers[5]
        HEADER7 = Headers[6]
        HEADER8 = Headers[7]
        HEADER9 = Headers[8]

        PRINTFILE = HEADER1 + "," + HEADER2 + "," + HEADER3 + "," + HEADER4 + "," + HEADER5 + ","
        PRINTFILE = PRINTFILE + HEADER6 + "," + HEADER7 + "," + HEADER8 + "," + HEADER9
        PRINTFILE = PRINTFILE + ",AntennaHeight1,AntennaHeight2,PathDistance,Frequency" + "\n"

        if self.OptimizePaths == "Y":
            final_path_data_df.write(PRINTFILE)

        failed_path_data_df.write(PRINTFILE)
        passed_path_data_df.write(PRINTFILE)

        if HEADER1 != "Index" or HEADER8 != "TowerHeight1" or HEADER9 != "TowerHeight2":
            print("File does not match required file format.")
            print("The left most column should be labeled <Index>.")
            print("The two right columns should be labeled <TowerHeight1> and <TowerHeight2> respectively.")
            sys.exit()

        PathCounter = 0

        for index, row in data_file_df.iterrows():    # Walk through the path definitions
            PathCounter = PathCounter + 1

            PathIndex = row[0]
            self.SITE1 = row[1]
            Latitude1 = row[2]
            Longitude1 = row[3]
            SITE2 = row[4]
            Latitude2 = row[5]
            Longitude2 = row[6]
            self.TwrHt1 = row[7]
            self.TwrHt2 = row[8]

            self.ProfileNumber = PathIndex
            self.ProfileNumber = str(self.ProfileNumber)

            if float(PathIndex) < 100000:
                self.ProfileNumber = "0" + self.ProfileNumber
            if float(PathIndex) < 10000:
                self.ProfileNumber = "0" + self.ProfileNumber
            if float(PathIndex) < 1000:
                self.ProfileNumber = "0" + self.ProfileNumber
            if float(PathIndex) < 100:
                self.ProfileNumber = "0" + self.ProfileNumber
            if float(PathIndex) < 10:
                self.ProfileNumber = "0" + self.ProfileNumber

            # Determine path operating frequency
            PathFreqFilePath = self.ExampleS2AFolderPath + "/TempFile/PathFreq.csv"
            path_freq_df = pd.read_csv(PathFreqFilePath, header=None)       #66

            self.OpFreq = float("inf")
            for i, line in path_freq_df.iterrows():
                ThePath = line[0]
                TheFreq = line[1]

                if ThePath == PathIndex:
                    self.OpFreq = TheFreq

            if self.OpFreq == float("inf"):
                print("Path operating frequency could not be identified.")
                print("Review PathFreq.csv file in TempFile folder.")
                print("Program terminated prematurely.")
                sys.exit()

            # Determine path data
            PathDataFilePath = self.ExampleS2AFolderPath + "/TempFile/PathData.csv"
            path_data_df = pd.read_csv(PathDataFilePath, header=None)       #66

            for i, line in path_data_df.iterrows():
                APathIndex = line[0]
                ASite1Elevation = line[1]
                ATwrHt1 = line[2]
                ASite2Elevation = line[3]
                ATwrHt2 = line[4]
                ASite2Distance = line[5]

                if APathIndex == PathIndex:
                    self.Site1Elevation = ASite1Elevation
                    self.TwrHt1 = ATwrHt1
                    self.Site2Elevation = ASite2Elevation
                    self.TwrHt2 = ATwrHt2
                    self.Site2Distance = ASite2Distance

            os.system('cls' if os.name == 'nt' else 'clear')

            # Begin profile evaluation ++++++++++++++++++++++++++++++++++
            print("\n     Beginning Profile " + str(self.ProfileNumber) + " Evaluation\n")

            self.ProfileNumberFilePath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"
            profile_number_df = pd.read_csv(self.ProfileNumberFilePath, header=None)      #11

            PointCount = 0
            WorstCaseClearance1 = 999999
            WorstCaseClearance2 = 999999
            WorstCaseDistance1 = 0
            WorstCaseDistance2 = 0
            FailFlag = 0

            for i, line in profile_number_df.iterrows():

                PointCount = PointCount + 1
                distance = line[0]
                ELEVATION = line[1]
                self.ObstructionHeight = line[2]
                LUcode = line[3]
                LANDUSECODE = line[4]

                if PointCount == 1:
                    continue
                self.Eval = 1

                #Evaluate each point on the path
                Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                if Clearance1 < WorstCaseClearance1:
                    WorstCaseClearance1 = Clearance1
                    WorstCaseDistance1 = distance
                if self.Test2Flag == 1 and Clearance2 < WorstCaseClearance2:
                    WorstCaseClearance2 = Clearance2
                    WorstCaseDistance2 = distance


            if float(WorstCaseClearance1) >= 0:
                WorstCaseClearance1 = str(float(WorstCaseClearance1 + .5))
            if float(WorstCaseClearance1) < 0:
                WorstCaseClearance1 = str(float(WorstCaseClearance1 - .5))
            if float(WorstCaseClearance2) >= 0:
                WorstCaseClearance2 = str(float(WorstCaseClearance2 + .5))
            if float(WorstCaseClearance2) < 0:
                WorstCaseClearance2 = str(float(WorstCaseClearance2 - .5))

            self.FirstKFactor = float(self.FirstKFactor)
            SecondKFactorMod = float(SecondKFactorMod)
            self.FirstFresnelFraction = float(self.FirstFresnelFraction)
            self.SecondFresnelFraction = float(self.SecondFresnelFraction)

            self.FirstKFactor = float((self.FirstKFactor * 1000) + .5)
            self.FirstKFactor = self.FirstKFactor / 1000
            self.FirstKFactor = str(self.FirstKFactor)
            SecondKFactorMod = float((SecondKFactorMod * 1000) + .5)
            SecondKFactorMod = SecondKFactorMod / 1000
            SecondKFactorMod = str(SecondKFactorMod)
            self.FirstFresnelFraction = float((self.FirstFresnelFraction * 1000) + .5)
            self.FirstFresnelFraction = self.FirstFresnelFraction / 1000
            self.FirstFresnelFraction = str(self.FirstFresnelFraction)
            self.SecondFresnelFraction = float((self.SecondFresnelFraction * 1000) + .5)
            self.SecondFresnelFraction = self.SecondFresnelFraction / 1000
            self.SecondFresnelFraction = str(self.SecondFresnelFraction)

            PRINTPART2 = ",First 1st Fresnel Zone Factor  =," + str(self.FirstFresnelFraction) + ",Second 1st Fresnel Zone Factor  =," + str(self.SecondFresnelFraction)
            PRINTPART2 = PRINTPART2 + ",First K Factor  =," + str(self.FirstKFactor) + ",Second K Factor  =," + str(SecondKFactorMod)
            PRINTPART2 = PRINTPART2 + ",Frequency =," + str(self.OpFreq) + " GHz,Distance =," + str(self.Site2Distance)
            if self.FeetMeters == "F":
                PRINTPART2 = PRINTPART2 + " miles"
            if self.FeetMeters == "M":
                PRINTPART2 = PRINTPART2 + " km"

            if self.FeetMeters == "F":
                if FailFlag == 0:
                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
                    if self.Test2Flag == 0:
                        pass_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2) + "\n"

                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
                    PRINTPART1 = PRINTPART1 + ",Worst Case Criterion 2 Clearance (feet) =," + str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
                    if self.Test2Flag == 1:
                        pass_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

                if FailFlag == 1:
                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
                    if self.Test2Flag == 0:
                        fail_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
                    PRINTPART1 = PRINTPART1 + ",Worst Case Criterion 2 Clearance (feet) =," +str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
                    if self.Test2Flag == 1:
                        fail_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

            if self.FeetMeters == "M":
                if FailFlag == 0:
                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (meters) =," + str(WorstCaseClearance1) + ",at path distance (km) = ," + str(WorstCaseDistance1)
                    if(self.Test2Flag == 0): fail_stat_df.write(PathIndex + "," + PRINTPART1 + PRINTPART2)
                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
                    PRINTPART1 = str(PRINTPART1) + ",Worst Case Criterion 2 Clearance (feet) =," + str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
                    if self.Test2Flag == 1: fail_stat_df.write(PathIndex + "," + PRINTPART1 + PRINTPART2)

                if FailFlag == 1:
                    PRINTPART1 = "PR" + str(self.ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (meters) =," + str(WorstCaseClearance1) + ",at path distance (km) = ," + str(WorstCaseDistance1)
                    if self.Test2Flag == 0: fail_stat_df.write(str(PathIndex) + "," + str(PRINTPART1) + str(PRINTPART2))
                    PRINTPART1 = str(PRINTPART1) + ",Worst Case Criterion 2 Clearance (meters) =," + str(WorstCaseClearance2) + ",at path distance (km) = ," + str(WorstCaseDistance2)
                    if self.Test2Flag == 1: fail_stat_df.write(str(PathIndex) + "," + str(PRINTPART1) + str(PRINTPART2))


            self.ProfileNumberFilePath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"
            profile_number_df = pd.read_csv(self.ProfileNumberFilePath, header=None)      #11

            PointCount = 0
            for i, line in profile_number_df.iterrows():    #11
                PointCount = PointCount + 1

                distance = line[0]
                ELEVATION = line[1]
                self.ObstructionHeight = line[2]
                LUcode = line[3]
                LANDUSECODE = line[4]
                if PointCount == 1: self.TwrHt1 = float(self.ObstructionHeight)

            self.TwrHt2 = self.ObstructionHeight

            if FailFlag == 0:
                pass_site_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
                pass_site_df.write(str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "\n")
                pass_path_df.write(str(PathIndex) + "," + str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(self.Site2Distance) + "\n")

            if FailFlag == 1:
                fail_site_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
                fail_site_df.write(str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "\n")
                fail_path_df.write(str(PathIndex) + "," + str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(self.Site2Distance) + "\n")

            HoldFlag = FailFlag

            while True:     # this loop is intended to break on goto 500 statements -- scope in qbasic module is line 358 - 604
                if self.OptimizePaths != "Y":
                    break # goto 500

                if FailFlag == 0:       # Optimize the path
                    self.SysOpt = "Y"
                    ShortestWGrun = self.TwrHt1 + self.TwrHt2

                    if self.FeetMeters == "F":
                        self.START1 = 10  #minimum tower height is 10 feet
                        self.START2 = 10

                    if self.FeetMeters == "M":
                        self.START1 = 3   #minimum tower height is 3 meters
                        self.START2 = 3

                    if self.START1 > float(self.TwrHt1 + .5): self.START1 = float(self.TwrHt1 + .5)     #tower heights in feet will increment in feet
                    if self.START2 > float(self.TwrHt2 + .5): self.START2 = float(self.TwrHt2 + .5)

                    if self.FeetMeters == "M":
                        self.START1 = self.START1 * 4 #tower heights in meters will increment in 0.25 m
                        self.START2 = self.START2 * 4

                    self.END1 = float(self.TwrHt1 + .5)
                    self.END2 = float(self.TwrHt2 + .5)

                    if self.FeetMeters == "M":
                        self.END1 = self.END1 * 4
                        self.END2 = self.END2 * 4

                    #Find buildings that can not move antenna heights
                    SiteNoOpFilePath = self.ExampleS2AFolderPath + "/SiteNoOp.csv"
                    site_no_op_df = pd.read_csv(SiteNoOpFilePath, header=None)      #88

                    Site1Flag = 0
                    Site2Flag = 0

                    NUMBER_OF_LINES = site_no_op_df.shape[0]
                    for k in range(2, NUMBER_OF_LINES):
                        SiteRow = site_no_op_df.iloc[k]
                        NoOpSite = SiteRow[0]
                        if NoOpSite == self.SITE1: Site1Flag = 1
                        if NoOpSite == SITE2: Site2Flag = 1

                    while True: # goto 530 on break
                        if Site1Flag == 1 and Site2Flag == 1:
                            self.ShortestAntHt1 = str(self.TwrHt1)
                            self.ShortestAntHt2 = str(self.TwrHt2)
                            break   #GOTO 530

                        if Site1Flag == 1 or Site2Flag == 1: # unnecessary condition, left for easy comparison to original module

                            if Site1Flag == 1:
                                self.ShortestAntHt1 = str(self.TwrHt1)
                                self.TwrHtFlag = 1  # Optimize AntHt2#
                                self.optimize_one_tower(ShortestWGrun)
                                break     # GOTO 530

                            if Site2Flag == 1:
                                self.ShortestAntHt2 = str(self.TwrHt2)
                                self.TwrHtFlag = 0  # Optimize AntHt1#
                                self.optimize_one_tower(ShortestWGrun)
                                break   #GOTO 530

                        self.TwrHtFlag = 0
                        if self.TwrHt2 <= self.TwrHt1: self.TwrHtFlag = 1  # alway start optimization first with taller tower

                        if self.TwrHtFlag == 0:
                            self.IISTART = self.START1
                            self.IIEND = self.END1
                            JJSTART = self.START2
                            JJEND = self.END2

                        if self.TwrHtFlag == 1:
                            self.IISTART = self.START2
                            self.IIEND = self.END2
                            JJSTART = self.START1
                            JJEND = self.END1

                        self.int_IIEND = int(self.IIEND)
                        int_JJEND = int(JJEND)

                        for II in range(self.IISTART, self.int_IIEND):
                            for JJ in range(JJSTART, int_JJEND, 10):
                                if self.TwrHtFlag == 0:
                                    self.AntHt1 = self.IIEND - II + self.IISTART
                                    if self.FeetMeters == "M": self.AntHt1 = self.AntHt1 / 4
                                    self.AntHt2 = JJEND - JJ + JJSTART
                                    if self.FeetMeters == "M": self.AntHt2 = self.AntHt2 / 4

                                if self.TwrHtFlag == 1:
                                    self.AntHt2 = self.IIEND - II + self.IISTART
                                    if self.FeetMeters == "M": self.AntHt2 = self.AntHt2 / 4
                                    self.AntHt1 = JJEND - JJ + JJSTART
                                    if self.FeetMeters == "M": self.AntHt1 = self.AntHt1 / 4

                                PCProfileFolderPath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"   #11
                                pc_profile_df = pd.read_csv(PCProfileFolderPath, header=None)

                                PointCount = 0
                                FailFlag = 0

                                for k, profile in pc_profile_df.iterrows():
                                    PointCount = PointCount + 1

                                    distance = profile[0]
                                    ELEVATION = profile[1]
                                    self.ObstructionHeight = profile[2]
                                    LUcode = profile[3]
                                    LANDUSECODE = profile[4]

                                    if PointCount == 1:
                                        continue    # GOTO 430

                                    self.Eval = 2
                                    # call 2000 funciton here ########GOSUB 2000
                                    Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                                if FailFlag == 0: NewStart = JJ
                                if FailFlag == 1: break      # abandon current JJ loop and execute 510 restart code only if FailFlag = 1

                            for JJ in range(NewStart, int_JJEND):
                                if self.TwrHtFlag == 0:
                                    self.AntHt1 = self.IIEND - II + self.IISTART
                                    if self.FeetMeters == "M": self.AntHt1 = self.AntHt1 / 4
                                    self.AntHt2 = JJEND - JJ + JJSTART
                                    if self.FeetMeters == "M": self.AntHt2 = self.AntHt2 / 4

                                if self.TwrHtFlag == 1:
                                    self.AntHt2 = self.IIEND - II + self.IISTART
                                    if self.FeetMeters == "M": self.AntHt2 = self.AntHt2 / 4
                                    self.AntHt1 = JJEND - JJ + JJSTART
                                    if self.FeetMeters == "M": self.AntHt1 = self.AntHt1 / 4

                                self.PerCent = 100 * (((II / self.IIEND) + (JJ / (self.IIEND * JJEND))) / (1 + (1 / JJEND)))
                                self.PerCent = float((self.PerCent * 100) + .5)
                                self.PerCent = self.PerCent / 100
                                self.PerCent = str(self.PerCent)
                                self.AntHt1 = str(self.AntHt1)
                                self.AntHt2 = str(self.AntHt2)

                                if FailFlag == 0: Info = "Path Clear"
                                if FailFlag == 1: Info = "Path Obstructed"

                                print("Path " + str(self.ProfileNumber) + " optimization = " + str(self.PerCent) + "%, (AntHt1 = " + str(self.AntHt1) + ", AntHt2 = " + str(self.AntHt2) + ", " + str(Info) + ")")

                                PCProfileFolderPath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"   #11
                                pc_profile_df = pd.read_csv(PCProfileFolderPath, header=None)

                                PointCount = 0
                                FailFlag = 0

                                for k, profile in pc_profile_df.iterrows():
                                    PointCount = PointCount + 1

                                    distance = profile[0]
                                    ELEVATION = profile[1]
                                    self.ObstructionHeight = profile[2]
                                    LUcode = profile[3]
                                    LANDUSECODE = profile[4]

                                    if PointCount == 1: continue

                                    self.Eval = 2

                                    # call 2000 here ########### GOSUB 2000
                                    Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                                if FailFlag == 0:
                                    self.WGrun = float(self.AntHt1) + float(self.AntHt2)
                                    if self.WGrun < ShortestWGrun:
                                        ShortestWGrun = self.WGrun
                                        self.ShortestAntHt1 = float(self.AntHt1)
                                        self.ShortestAntHt2 = float(self.AntHt2)
                                        self.ShortestAntHt1 = float((self.ShortestAntHt1 * 100) + .5)
                                        self.ShortestAntHt1 = self.ShortestAntHt1 / 100
                                        self.ShortestAntHt1 = str(self.ShortestAntHt1)
                                        self.ShortestAntHt2 = float((self.ShortestAntHt2 * 100) + .5)
                                        self.ShortestAntHt2 = self.ShortestAntHt2 / 100
                                        self.ShortestAntHt2 = str(self.ShortestAntHt2)

                                if FailFlag == 1: break     # exit JJ loop and go to next II

                        break   # break point where Goto 530 statments start

                    #530 'Create the optimized link profile and link evaluation files
                    # still within scope of if (failflag == 0)
                    PCFolderPath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"      #11
                    pc_df = pd.read_csv(PCFolderPath, header=None)

                    PRFolderPath = self.ExampleS2AFolderPath + "/Optimize/PR" + str(self.ProfileNumber) + ".csv"      #12
                    pr_df = open(PRFolderPath, "w")

                    EVFolderPath = self.ExampleS2AFolderPath + "/Optimize/EV" + str(self.ProfileNumber) + ".csv"      #13
                    ev_df = open(EVFolderPath, "w")

                    PointCount = 0

                    PRINTFILE = str(PathIndex) + "," + str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
                    PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(self.TwrHt1) + "," + str(self.TwrHt2) + ","
                    PRINTFILE = PRINTFILE + str(self.ShortestAntHt1) + "," + str(self.ShortestAntHt2) + "," + str(self.Site2Distance) + "," + str(self.OpFreq)
                    final_path_data_df.write(PRINTFILE + "\n")

                    pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
                    ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")

                    for k, profile in pc_df.iterrows():
                        PointCount = PointCount + 1

                        distance = profile[0]
                        ELEVATION = profile[1]
                        self.ObstructionHeight = profile[2]
                        LUcode = profile[3]
                        LANDUSECODE = profile[4]

                        if PointCount == 1: self.ObstructionHeight = self.ShortestAntHt1
                        pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(self.ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

                        self.Eval = 2
                        self.AntHt1 = self.ShortestAntHt1
                        self.AntHt2 = self.ShortestAntHt2
                        EarthHeight2 = 0
                        ModifiedPathHeight2 = 0

                        # call 2000 function here ######## GOSUB 2000
                        Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                        TerrainHeight = ELEVATION + float(self.ObstructionHeight)

                        if PointCount == 1:
                            PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(PathHeight) + ","
                        else:
                            PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(EarthHeight1) + "," + str(EarthHeight2) + "," + str(PathHeight) + ","
                        PRINTFILE = PRINTFILE + str(ModifiedPathHeight1) + "," + str(ModifiedPathHeight2)
                        ev_df.write(PRINTFILE + "\n")

                    pr_df.close()
                    ev_df.close()


                break
            # 500   'Work on non-optimized paths
            FailFlag = HoldFlag
            if FailFlag == 1:

                # Create the failed link profile and link evaluation files
                self.SysFail = "Y"

                PCFolderPath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"      #11
                pc_df = pd.read_csv(PCFolderPath, header=None)

                PRFolderPath = self.ExampleS2AFolderPath + "/Failed/PR" + str(self.ProfileNumber) + ".csv"      #12
                pr_df = open(PRFolderPath, "w")

                EVFolderPath = self.ExampleS2AFolderPath + "/Failed/EV" + str(self.ProfileNumber) + ".csv"      #13
                ev_df = open(EVFolderPath, "w")

                PointCount = 0
                self.ShortestAntHt1 = self.TwrHt1
                self.ShortestAntHt2 = self.TwrHt2

                PRINTFILE = str(PathIndex) + "," + str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
                PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(self.TwrHt1) + "," + str(self.TwrHt2) + ","
                PRINTFILE = PRINTFILE + str(self.ShortestAntHt1) + "," + str(self.ShortestAntHt2) + "," + str(self.Site2Distance) + "," + str(self.OpFreq)
                failed_path_data_df.write(PRINTFILE + "\n")

                pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
                ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")


                for k, profile in pc_df.iterrows():
                    PointCount = PointCount + 1

                    distance = profile[0]
                    ELEVATION = profile[1]
                    self.ObstructionHeight = profile[2]
                    LUcode = profile[3]
                    LANDUSECODE = profile[4]

                    if PointCount == 1: self.ObstructionHeight = self.ShortestAntHt1
                    pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(self.ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

                    self.Eval = 2
                    self.AntHt1 = self.ShortestAntHt1
                    self.AntHt2 = self.ShortestAntHt2
                    EarthHeight2 = 0
                    ModifiedPathHeight2 = 0

                    # call 2000 function here ######### GOSUB 2000
                    Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                    TerrainHeight = ELEVATION + self.ObstructionHeight

                    if PointCount == 1:
                        PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(PathHeight) + ","
                    else:
                        PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(EarthHeight1) + "," + str(EarthHeight2) + "," + str(PathHeight) + ","
                    PRINTFILE = str(PRINTFILE) + str(ModifiedPathHeight1) + "," + str(ModifiedPathHeight2)
                    ev_df.write(PRINTFILE + "\n")

                    EVDuplicatePath = self.ExampleS2AFolderPath + "/Passed/EV" + str(self.ProfileNumber) + ".csv"
                    PRDuplicatePath = self.ExampleS2AFolderPath + "/Passed/PR" + str(self.ProfileNumber) + ".csv"

                    try:
                        os.remove(EVDuplicatePath)
                    except FileNotFoundError:
                        pass

                    try:
                        os.remove(PRDuplicatePath)
                    except FileNotFoundError:
                        pass

                pr_df.close()   #CLOSE #12
                ev_df.close()   #CLOSE #13

            if FailFlag == 0:

                # Create the passed link profile and link evaluation files
                self.SysPass = "Y"

                PCFolderPath = self.ExampleS2AFolderPath + "/TempFile/PC" + str(self.ProfileNumber) + ".csv"      #11
                pc_df = pd.read_csv(PCFolderPath, header=None)

                PRFolderPath = self.ExampleS2AFolderPath + "/Passed/PR" + str(self.ProfileNumber) + ".csv"      #12
                pr_df = open(PRFolderPath, "w")

                EVFolderPath = self.ExampleS2AFolderPath + "/Passed/EV" + str(self.ProfileNumber) + ".csv"      #13
                ev_df = open(EVFolderPath, "w")

                PointCount = 0
                self.ShortestAntHt1 = self.TwrHt1
                self.ShortestAntHt2 = self.TwrHt2

                PRINTFILE = str(PathIndex) + "," + str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
                PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(self.TwrHt1) + "," + str(self.TwrHt2) + ","
                PRINTFILE = PRINTFILE + str(self.ShortestAntHt1) + "," + str(self.ShortestAntHt2) + "," + str(self.Site2Distance) + "," + str(self.OpFreq)
                passed_path_data_df.write(PRINTFILE + "\n")

                pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
                ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")

                for k, profile in pc_df.iterrows():
                    PointCount = PointCount + 1

                    distance = profile[0]
                    ELEVATION = profile[1]
                    self.ObstructionHeight = profile[2]
                    LUcode = profile[3]
                    LANDUSECODE = profile[4]

                    if PointCount == 1: self.ObstructionHeight = self.ShortestAntHt1
                    pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(self.ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

                    self.Eval = 2
                    self.AntHt1 = self.ShortestAntHt1
                    self.AntHt2 = self.ShortestAntHt2
                    EarthHeight2 = 0
                    ModifiedPathHeight2 = 0

                    # call 2000 function here ##### GOSUB 2000
                    Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone = self.point_on_path(distance, ELEVATION, self.ObstructionHeight,FailFlag,self.AddlClearance,self.ITURkFactor,self.SecondKFactor,self.Test2Flag)

                    TerrainHeight = ELEVATION + self.ObstructionHeight

                    if PointCount == 1:
                        PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(PathHeight) + ","
                    else:
                        PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(EarthHeight1) + "," + str(EarthHeight2) + "," + str(PathHeight) + ","
                    PRINTFILE = str(PRINTFILE) + str(ModifiedPathHeight1) + "," + str(ModifiedPathHeight2)
                    ev_df.write(PRINTFILE + "\n")


                    EVDuplicatePath = self.ExampleS2AFolderPath + "/Failed/EV" + str(self.ProfileNumber) + ".csv"
                    PRDuplicatePath = self.ExampleS2AFolderPath + "/Failed/PR" + str(self.ProfileNumber) + ".csv"

                    try:
                        os.remove(EVDuplicatePath)
                    except FileNotFoundError:
                        pass

                    try:
                        os.remove(PRDuplicatePath)
                    except FileNotFoundError:
                        pass

                pr_df.close()   #CLOSE #12
                ev_df.close()   #CLOSE #13

        StatusFilePath = self.ExampleS2AFolderPath + "/TempFile/Status.csv"      #57
        status_df = open(StatusFilePath, "w")

        status_df.write("Optimized Paths?," + str(self.SysOpt) + "\n")
        status_df.write("Failed Paths?," + str(self.SysFail) + "\n")
        status_df.write("Passed Paths?," + str(self.SysPass) + "\n")

        status_df.close()

        pass_path_df.flush()
        pass_path_df.close()

        # Eliminate duplicates from passed sites list
        print("     Eliminating duplicates from passed sites list")

        pass_site_df.close()    # attempted bug fix

        PassSiteFilePath2 = self.ExampleS2AFolderPath + "/Passed/PassSite.csv"
        pass_site_df = pd.read_csv(PassSiteFilePath2, header=None)       #56

        Temp1FilePath = self.ExampleS2AFolderPath + "/TempFile/Temp1.csv"
        temp1_df = open(Temp1FilePath, "w")         #57

        for i, row in pass_site_df.iterrows():
            self.SITE1 = row[0]
            Latitude1 = row[1]
            Longitude1 = row[2]

            temp1_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")

        pass_site_df = open(PassSiteFilePath2, "w")              #57
        pass_site_df.close()

        temp1_df.close()
        temp1_df = pd.read_csv(Temp1FilePath, header=None)       #56

        for i, row in temp1_df.iterrows():
            self.SITE1 = row[0]
            Latitude1 = row[1]
            Longitude1 = row[2]
            length = len(temp1_df.index)

            Flag = 0

            if i != 0:  # dont try to read from this file on first pass (its empty at first)
                pass_site_df = pd.read_csv(PassSiteFilePath2, header=None)      #57

                for k, line in pass_site_df.iterrows():
                    SiteA = line[0]
                    LATITUDEA = line[1]
                    LONGITUDEA = line[2]

                    if self.SITE1 == SiteA:
                        Flag = 1

            if Flag == 0:
                pass_site_df = open(PassSiteFilePath2, "a")      #57
                pass_site_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
                pass_site_df.flush()
                pass_site_df.close()

        # Eliminate duplicates from failed sites list
        print("     Eliminating duplicates from failed sites list")
        fail_site_df.flush()
        fail_site_df.close()

        FailSiteFilePath2 = self.ExampleS2AFolderPath + "/Failed/FailSite.csv"

        try:
            failed_site_df = pd.read_csv(FailSiteFilePath2, header=None)       #56
        
            Temp1FilePath2 = self.ExampleS2AFolderPath + "/TempFile/Temp1.csv"
            temp1_df = open(Temp1FilePath2, "w")        #57

            for i, row in failed_site_df.iterrows():
                self.SITE1 = row[0]
                Latitude1 = row[1]
                Longitude1  = row[2]

                temp1_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")

            temp1_df.flush()
            temp1_df.close()
            temp1_df = pd.read_csv(Temp1FilePath2, header=None)     #56

            for i, row in temp1_df.iterrows():
                self.SITE1 = row[0]
                Latitude1 = row[1]
                Longitude1 = row[2]

                failed_site_df = pd.read_csv(FailSiteFilePath2, header=None)        #57

                Flag = 0
                for k, line in failed_site_df.iterrows():
                    SiteA = line[0]
                    LATITUDEA = line[1]
                    LONGITUDEA = line[2]

                    if self.SITE1 == SiteA:
                        Flag = 1

                if Flag == 0:
                    failed_site_df = open(FailSiteFilePath2, "a")       #57
                    failed_site_df.write(str(self.SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
                    failed_site_df.flush()
                    failed_site_df.close()  # CLOSE #57 
        except pd.errors.EmptyDataError:
            print(FailSiteFilePath2 + " is empty")
            pass
        # Create the Google Earth/KML mapping files '+++++++++++++++++++++++++++++
        os.system('cls' if os.name == 'nt' else 'clear')
        # Passed sites and paths
        InputFileSites = self.ExampleS2AFolderPath + "/Passed/PassSite.csv"
        InputFilePaths = self.ExampleS2AFolderPath + "/Passed/PassPath.csv"
        OutputFileGoogle = self.ExampleS2AFolderPath + "/Passed/Google/GEPaths.KML"
        # Create Maps
        self.createKML(InputFileSites, InputFilePaths, OutputFileGoogle)

        # Failed sites and paths
        InputFileSites = self.ExampleS2AFolderPath + "/Failed/FailSite.csv"
        InputFilePaths = self.ExampleS2AFolderPath + "/Failed/FailPath.csv"
        OutputFileGoogle = self.ExampleS2AFolderPath + "/Failed/Google/GEPaths.KML"
        # Create Maps
        try:
            self.createKML(InputFileSites, InputFilePaths, OutputFileGoogle)
        except pd.errors.EmptyDataError:
            print("EmptyDataError Occured: No columns to parse from file")
            pass

        print("\nProgram Completed\n")
        # =======



# test the class
test = GudPath()
test.setFolderPath("C:\ExampleStep2BN(Eric)")
test.setLULC("y")
test.setPathEval(1)
test.setOptimizePathsOption("n")
test.execute()
