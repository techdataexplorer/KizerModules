import math
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

def initializeSubroutine(Criteria): #9000
    
    inpFile = open(Criteria, "r")          
    Answers = [] 
    counter = 0

    for line in inpFile:
        currentline = line.split(",")
        if (counter == 6 or counter == 22):
            counter+=1
            continue
        if (counter == 7):
            Answers.append(currentline[1])
            counter+=1
            continue

        Answers.append(currentline[0])

        if(counter >= 8 and counter <= 13):
            Answers.append(currentline[1])
            counter+=1
            
        counter += 1

    inpFile.close()
    Answers.append(1000)#MaxDist1
    return Answers

# KML map generator for paths and sites (took out delorme and mapinfo code)
def createKML(InputFileSites, InputFilePaths, OutputFileGoogle):

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
        SITE1 = row[0]
        LAT1 = row[1]
        LON1 = row[2]

        output_file_google_df.write("" + "\n")
        output_file_google_df.write("     <Placemark>" + "\n")
        output_file_google_df.write("     <name>" + str(SITE1) + "</name>" + "\n")
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
        SITE1 = row[1]
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
def point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag):

    if Eval == 1: 
        Site1AntennaElevation = float(Site1Elevation) + float(TwrHt1)
        Site2AntennaElevation = float(Site2Elevation) + float(TwrHt2)
    if Eval == 2: 
        Site1AntennaElevation = float(Site1Elevation) + float(AntHt1)
        Site2AntennaElevation = float(Site2Elevation) + float(AntHt2)


    PathHeight = Site1AntennaElevation + (((Site2AntennaElevation - Site1AntennaElevation) / Site2Distance) * distance)

    PathDistanceA = distance
    PathDistanceB = Site2Distance - PathDistanceA

    # Second (obstruction) K factor creation (ITU-R) or (ALU) modification
    SecondKFactorMod = float(SecondKFactor)

    if ITURkFactor == "Y":
        PD = distance
        if FeetMeters == "F": PD = PD * 1.609344
        if PD < 20: PD = 20
        if PD > 200: PD = 200
        SecondKFactorMod = .80379426 + (.0029438097 * PD) - (6.1701657 / PD)
        SecondKFactorMod = SecondKFactorMod - (.000013619815 * PD * PD) + (10.375301 / (PD * PD))
        SecondKFactorMod = SecondKFactorMod + (.000000022844768 * PD * PD * PD)

    if ALUkFactor == "Y":
        PD = distance
        if FeetMeters == "M": PD = PD / 1.609344
        if PD < 25: PD = 25
        if PD > 150: PD = 150

        if ALUkFactor == 1:
            SecondKFactorMod = 1.3525442 - (.0025870465 * PD) - (13.402012 / PD)
            SecondKFactorMod = SecondKFactorMod + (.000018703584 * PD * PD) + (148.40133 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod - (.000000045263631 * PD * PD * PD)

        if ALUkFactor == 2:
            SecondKFactorMod = 1.0561294 - (.0026434873 * PD) - (14.930824 / PD)
            SecondKFactorMod = SecondKFactorMod + (.000025692173 * PD * PD) + (161.86573 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod - (.00000007235408 * PD * PD * PD)

        if ALUkFactor == 3:
            SecondKFactorMod = .82999889 - (.0015503296 * PD) - (13.665673 / PD)
            SecondKFactorMod = SecondKFactorMod + (.0000172027 * PD * PD) + (152.99299 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod - (.000000046838057 * PD * PD * PD)

        if ALUkFactor == 4:
            SecondKFactorMod = .6454992899999999 - (.00116752 * PD) - (11.930858 / PD)
            SecondKFactorMod = SecondKFactorMod + (.000017371414 * PD * PD) + (156.48897 / (PD * PD))
            SecondKFactorMod = SecondKFactorMod - (.000000053622664 * PD * PD * PD)


    # Test 1 K factor Earth Bulge
    if FeetMeters == "F": EarthBulge1 = (float(PathDistanceA) * float(PathDistanceB)) / (1.5 * float(FirstKFactor))   # miles
    if FeetMeters == "M": EarthBulge1 = (float(PathDistanceA) * float(PathDistanceB)) / (12.75 * float(FirstKFactor))   # kilometers

    # Test 2 K factor Earth Bulge
    if SecondKFactor != "":
        if FeetMeters == "F": EarthBulge2 = (float(PathDistanceA) * float(PathDistanceB)) / (1.5 * SecondKFactorMod)   # miles
        if FeetMeters == "M": EarthBulge2 = (float(PathDistanceA) * float(PathDistanceB)) / (12.75 * SecondKFactorMod)  # kilometers
    

    # Alternate Test 2 Earth Bulge = 150 feet plus grazing (0 F1) at k = 1
    if DLaneTest == "Y":
        if FeetMeters == "F": 
            EarthBulge2 = (PathDistanceA * PathDistanceB) / (1.5 * 1)   # miles
            EarthBulge2 = EarthBulge2 + 150
        if FeetMeters == "M": 
            EarthBulge2 = (PathDistanceA * PathDistanceB) / (12.75 * 1)  # kilometers
            EarthBulge2 = EarthBulge2 + (150 * .3048)
    

    if FeetMeters == "F": FirstFresnelZone = 72.1 * math.sqrt((PathDistanceA * PathDistanceB) / (OpFreq * Site2Distance))
    if FeetMeters == "M": FirstFresnelZone = 17.3 * math.sqrt((PathDistanceA * PathDistanceB) / (OpFreq * Site2Distance))

    # Test 1 first Fresnel zone (F1) clearance
    FirstFresnelTestHeight = float(FirstFresnelFraction) * float(FirstFresnelZone)

    # Test 2 first Fresnel zone (F1) clearance
    if SecondKFactor != "": SecondFresnelTestHeight = float(SecondFresnelFraction) * float(FirstFresnelZone)
    if DLaneTest == "Y": SecondFresnelTestHeight = 0

    # Test 1
    EarthHeight1 = ELEVATION + EarthBulge1

    if int(PathEval) == 1: EarthHeight1 = float(EarthHeight1) + float(ObstructionHeight)
    if int(PathEval) == 2: EarthHeight1 = float(EarthHeight1) + float(WorstCaseObst)

    ModifiedPathHeight1 = PathHeight - FirstFresnelTestHeight - float(AddlClearance)
    Clearance1 = ModifiedPathHeight1 - EarthHeight1

    if Clearance1 < -1: FailFlag = 1

    if Test2Flag == 1:
        # Test 2
        EarthHeight2 = float(ELEVATION) + float(EarthBulge2)
        if int(PathEval) == 1: EarthHeight2 = float(EarthHeight2) + float(ObstructionHeight)
        if int(PathEval) == 2: EarthHeight2 = float(EarthHeight2) + float(WorstCaseObst)
        ModifiedPathHeight2 = float(PathHeight) - float(SecondFresnelTestHeight) - float(AddlClearance)
        Clearance2 = ModifiedPathHeight2 - EarthHeight2
        if Clearance2 < -1: FailFlag = 1
    

    return Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone   # add return values

#-------------------------------------------------------------------------- Line 1460
# 8000  'Optimize just one tower

def optimize_one_tower(ShortestWGrun):

    if TwrHtFlag == 0:
        IISTART = START1
        IIEND = END1
    
    if TwrHtFlag == 1:
        IISTART = START2
        IIEND = END2
    
    #FOR II = IISTART TO IIEND
    int_IIEND = int(IIEND)
    for II in range(IISTART, int_IIEND):
        if TwrHtFlag == 0:
            AntHt1 = IIEND - II + IISTART
            if FeetMeters == "M": AntHt1 = AntHt1 / 4
            AntHt2 = TwrHt2
        
        if TwrHtFlag == 1:
            AntHt2 = IIEND - II + IISTART
            if FeetMeters == "M": AntHt2 = AntHt2 / 4
            AntHt1 = TwrHt1
        
        #OPEN SysDataDrive$ + ":\" + Folder$ + "\TempFile\PC" + ProfileNumber$ + ".csv" FOR INPUT AS #11
        ProfileNumberFilePath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"
        profile_num_df = pd.read_csv(ProfileNumberFilePath, header=None)       #11

        PointCount = 0
        FailFlag = 0

        for index, row in profile_num_df.iterrows():
            PointCount = PointCount + 1

            distance = row[0]
            ELEVATION = row[1]
            ObstructionHeight = row[2]
            
            if PointCount == 1: continue    #GOTO 8400

            Eval = 2

            # call 2000 function here #### GOSUB 2000 # not sure why this is called here
            Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

        if FailFlag == 0:
            WGrun = AntHt1 + AntHt2
            if WGrun < ShortestWGrun:
                ShortestWGrun = WGrun
                ShortestAntHt1 = AntHt1
                ShortestAntHt2 = AntHt2
                ShortestAntHt1 = float((ShortestAntHt1 * 100) + .5)
                ShortestAntHt1 = ShortestAntHt1 / 100
                ShortestAntHt1 = str(ShortestAntHt1)
                ShortestAntHt2 = float((ShortestAntHt2 * 100) + .5)
                ShortestAntHt2 = ShortestAntHt2 / 100
                ShortestAntHt2 = str(ShortestAntHt2)
        
        PerCent = 100 * (II / IIEND)
        PerCent = float((PerCent * 100) + .5)
        PerCent = PerCent / 100
        PerCent = str(PerCent)
        AntHt1 = str(AntHt1)
        AntHt2 = str(AntHt2)

        if FailFlag == 0: Info = "Path Clear"
        if FailFlag == 1: Info = "Path Obstructed"

        print("Path " + str(ProfileNumber) + " optimization =  " + str(PerCent) + "%, (AntHt1 = " + str(AntHt1) + ", AntHt2 = " + str(AntHt2) + "," + str(Info) + ")")

        if FailFlag == 1: break     # GOTO 8500

    return     

################################################# PyQT GUI Class ###################################################
# Based on code from https://pythonspot.com/pyqt5-file-dialog/

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = ''
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

    def openFolderNameDialog(self, folderPrompt):
        folderName = QFileDialog.getExistingDirectory(self, folderPrompt)
        if folderName:
            return folderName

################################################# End PyQT GUI Class ###################################################

# Create PyQT Object
app = QApplication(sys.argv)
ex = App()

# Get ExampleS2A folder path from user's machine
ExampleS2AFolderPath = ex.openFolderNameDialog("Find ExampleS2A Folder")

print("Do the profiles contain use  land cover (LULC) data (Y or N)?")
LandUse = str(input("Enter Y or y for Yes, N or n for No or nothing to terminate program \n"))

if LandUse == "":
    sys.exit()

LandUse = LandUse.upper()
while LandUse != "Y" and LandUse != "N":
    if LandUse == "":
        sys.exit()
    LandUse = input("Enter Y or y for Yes, N or n for No or nothing to terminate program ")
    LandUse = LandUse.upper()

print("\nReading <Criteria.ini> initialization file.\n")

SysOpt = "N"
SysFail = "N"
SysPass = "N"

# 9000 Initialization subroutine, inserted here instead of calling the function
CriteriaFilePath = ExampleS2AFolderPath + "/Criteria.ini"
Answers = initializeSubroutine(CriteriaFilePath) #9000

TheDataFile = Answers[0]
TowerHt = Answers[1]
MilesKm = Answers[2]
FeetMeters = Answers[3]
BuildingHt = float(Answers[4])
TreeHt = float(Answers[5])
OpFreq1 = float(Answers[6])
MaxDist2 = float(Answers[7])
OpFreq2 = float(Answers[8])
MaxDist3 = float(Answers[9])
OpFreq3 = float(Answers[10])
MaxDist4 = float(Answers[11])
OpFreq4 = float(Answers[12])
FirstFresnelFraction = float(Answers[13])
FirstKFactor = float(Answers[14])
SecondFresnelFraction = float(Answers[15])
SecondKFactor = float(Answers[16])

DLaneTest = Answers[17]
if DLaneTest == '': DLaneTest = "N" 
AddlClearance = Answers[18]
if AddlClearance == '': AddlClearance = 0 

ITURkFactor = Answers[19]
ALUkFactor = Answers[20]
MaxDist1 = 1000

if FeetMeters == "":
    sys.exit()
FeetMeters = FeetMeters.upper()
if FeetMeters != "F" and FeetMeters != "M":
    print("Fourth line of <Criteria.ini> not understood.")
    print("Line should be F or M.")
    print("Program Terminated.")
    sys.exit()

# open all of the output files
PassStatFilePath = ExampleS2AFolderPath + "/Passed/PassStat.csv"        #51
pass_stat_df = open(PassStatFilePath, "w+")

FailStatFilePath = ExampleS2AFolderPath + "/Passed/FailStat.csv"        #52
fail_stat_df = open(FailStatFilePath, "w+")

PassSiteFilePath = ExampleS2AFolderPath + "/Passed/PassSite.csv"        #56
pass_site_df = open(PassSiteFilePath, "w+")

PassPathFilePath = ExampleS2AFolderPath + "/Passed/PassPath.csv"        #57
pass_path_df = open(PassPathFilePath, "w+")

FailSiteFilePath = ExampleS2AFolderPath + "/Passed/FailSite.csv"        #58
fail_site_df = open(FailSiteFilePath, "w+")

FailPathFilePath = ExampleS2AFolderPath + "/Passed/FailPath.csv"        #59
fail_path_df = open(FailPathFilePath, "w+")

print("Path evaluation will require a <Criteria.ini> file in the main folder.\n")
print("Input 1 to use path profile obstructions with assumed heights for evals.")
print("Input 2 to use worst case obstruction height for EACH path sample point.")
PathEval = input(":")

if PathEval != str(1) and PathEval != str(2):
    sys.exit()

WorstCaseObst = TreeHt
if BuildingHt > TreeHt:
    WorstCaseObst = BuildingHt

if PathEval == 1:
    print("\nPath profile obstructions with assumed heights will be used for evaluations.\n")
if PathEval == 2:
    print("\nAssumed tree (or building worst case) height will be used for evaluations.\n")

if DLaneTest != "N":
    DLaneTest = "Y"

Test2Flag = 0

if SecondFresnelFraction != "" or DLaneTest == "Y":
    Test2Flag = 1

print("\nPath evaluation criteria will be the following:")

DistUnits = " ."
if FeetMeters == "F":
    DistUnits = " miles."
if FeetMeters == "M":
    DistUnits = " km."

print("Maximum distance for " + str(OpFreq1) + " GHz is " + str(MaxDist1) + DistUnits)
print("Maximum distance for " + str(OpFreq2) + " GHz is " + str(MaxDist2) + DistUnits)
print("Maximum distance for " + str(OpFreq3) + " GHz is " + str(MaxDist3) + DistUnits)
print("Maximum distance for " + str(OpFreq4) + " GHz is " + str(MaxDist4) + DistUnits)

print(str(FirstFresnelFraction) + " of first Fresnel zone at K factor of " + str(FirstKFactor))
if SecondKFactor != "" and DLaneTest != "Y":
    print(str(SecondFresnelFraction) + " of first Fresnel zone at K factor of " + str(SecondKFactor))
if DLaneTest == "Y":
    print("150 feet plus grazing at K = 1")
if AddlClearance != "" and FeetMeters == "F":
    print(str(AddlClearance) + " feet will be added to the above criteria")
if AddlClearance != "" and FeetMeters == "M":
    print(str(AddlClearance) + " meters will be added to the above criteria")
print()

if FirstKFactor == "":
    print("The First Test K factor is missing.  It is required to procdeed.\n")
    sys.exit()

ITURkFactor = ITURkFactor.upper()
ALUkFactor = ALUkFactor.upper()

if ALUkFactor == "Y":
    ALUkFactor = 0
    TestValue = math.abs(float(SecondKFactor) - 1)
    
    if TestValue < .000001: ALUkFactor = 1
    TestValue = math.abs(float(SecondKFactor) - .66666667)
    if TestValue < .000001: ALUkFactor = 2
    TestValue = math.abs(float(SecondKFactor) - .5)
    if TestValue < .000001: ALUkFactor = 3
    TestValue = math.abs(float(SecondKFactor) - .4)
    if TestValue < .000001: ALUkFactor = 4
    if ALUkFactor == 0:
        print("ALU relaxation factor can only be applied to the following secondary K factors:")
        print("1, 2/3, 1/2, 4/10")
        print("The following defined value does not match any above value")
        print("Second K Factor = " + str(SecondKFactor))
        print("The program is terminated")
        sys.exit()

OptimizePaths = input("After evaluating the paths do you want to optimize the good paths (Y or N)\n")
OptimizePaths = OptimizePaths.upper()

FinalPathData = ExampleS2AFolderPath + "/Optimize/PathInfo.csv" 
if OptimizePaths == "Y":
    final_path_data_df = open(FinalPathData, "w+")      #14

FailedPathData = ExampleS2AFolderPath + "/Failed/PathInfo.csv"
failed_path_data_df = open(FailedPathData, "w+")        #15

PassedPathData = ExampleS2AFolderPath + "/Passed/PathInfo.csv"
passed_path_data_df = open(PassedPathData, "w+")        #16

# Open the file with the path definition data
PathFileFilePath = ExampleS2AFolderPath + "/" + TheDataFile + ".csv"
data_file_df = pd.read_csv(PathFileFilePath)         #10

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

if OptimizePaths == "Y":
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
    SITE1 = row[1]
    Latitude1 = row[2]
    Longitude1 = row[3]
    SITE2 = row[4]
    Latitude2 = row[5]
    Longitude2 = row[6]
    TwrHt1 = row[7]
    TwrHt2 = row[8]

    ProfileNumber = PathIndex
    ProfileNumber = str(ProfileNumber)

    if float(PathIndex) < 100000:
        ProfileNumber = "0" + ProfileNumber
    if float(PathIndex) < 10000:
        ProfileNumber = "0" + ProfileNumber
    if float(PathIndex) < 1000:
        ProfileNumber = "0" + ProfileNumber
    if float(PathIndex) < 100:
        ProfileNumber = "0" + ProfileNumber
    if float(PathIndex) < 10:
        ProfileNumber = "0" + ProfileNumber

    # Determine path operating frequency
    PathFreqFilePath = ExampleS2AFolderPath + "/TempFile/PathFreq.csv"
    path_freq_df = pd.read_csv(PathFreqFilePath, header=None)       #66

    OpFreq = "0"
    for i, line in path_freq_df.iterrows():
        ThePath = line[0]
        TheFreq = line[1]

        if ThePath == PathIndex:
            OpFreq = TheFreq

    if OpFreq == "0":
        print("Path operating frequency could not be identified.")
        print("Review PathFreq.csv file in TempFile folder.")
        print("Program terminated prematurely.")
        sys.exit()

    # Determine path data
    PathDataFilePath = ExampleS2AFolderPath + "/TempFile/PathData.csv"
    path_data_df = pd.read_csv(PathDataFilePath, header=None)       #66

    for i, line in path_data_df.iterrows():
        APathIndex = line[0]
        ASite1Elevation = line[1]
        ATwrHt1 = line[2]
        ASite2Elevation = line[3]
        ATwrHt2 = line[4]
        ASite2Distance = line[5]

        if APathIndex == PathIndex:
            Site1Elevation = ASite1Elevation
            TwrHt1 = ATwrHt1
            Site2Elevation = ASite2Elevation
            TwrHt2 = ATwrHt2
            Site2Distance = ASite2Distance

    os.system('cls' if os.name == 'nt' else 'clear')

    # Begin profile evaluation ++++++++++++++++++++++++++++++++++
    print("\n     Beginning Profile " + str(ProfileNumber) + " Evaluation\n")

    ProfileNumberFilePath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"
    profile_number_df = pd.read_csv(ProfileNumberFilePath, header=None)      #11

    PointCount = 0
    WorstCaseClearance1 = 999999
    WorstCaseClearance2 = 999999
    WorstCaseDistance1 = 0
    WorstCaseDistance2 = 0
    FailFlag = 0

    pcFileLength = len(profile_number_df.index)


    for i, line in profile_number_df.iterrows():

        PointCount = PointCount + 1 
        distance = line[0]
        ELEVATION = line[1]
        ObstructionHeight = line[2]
        LUcode = line[3]
        LANDUSECODE = line[4]
        
        if PointCount == 1:
            continue
        Eval = 1

        #Evaluate each point on the path
        Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

        if Clearance1 < WorstCaseClearance1:
            WorstCaseClearance1 = Clearance1
            WorstCaseDistance1 = distance
        if Test2Flag == 1 and Clearance2 < WorstCaseClearance2:
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

    FirstKFactor = float(FirstKFactor)
    SecondKFactorMod = float(SecondKFactorMod)
    FirstFresnelFraction = float(FirstFresnelFraction)
    SecondFresnelFraction = float(SecondFresnelFraction)

    FirstKFactor = float((FirstKFactor * 1000) + .5)
    FirstKFactor = FirstKFactor / 1000
    FirstKFactor = str(FirstKFactor)
    SecondKFactorMod = float((SecondKFactorMod * 1000) + .5)
    SecondKFactorMod = SecondKFactorMod / 1000
    SecondKFactorMod = str(SecondKFactorMod)
    FirstFresnelFraction = float((FirstFresnelFraction * 1000) + .5)
    FirstFresnelFraction = FirstFresnelFraction / 1000
    FirstFresnelFraction = str(FirstFresnelFraction)
    SecondFresnelFraction = float((SecondFresnelFraction * 1000) + .5)
    SecondFresnelFraction = SecondFresnelFraction / 1000
    SecondFresnelFraction = str(SecondFresnelFraction)

    PRINTPART2 = ",First 1st Fresnel Zone Factor  =," + str(FirstFresnelFraction) + ",Second 1st Fresnel Zone Factor  =," + str(SecondFresnelFraction)
    PRINTPART2 = PRINTPART2 + ",First K Factor  =," + str(FirstKFactor) + ",Second K Factor  =," + str(SecondKFactorMod)
    PRINTPART2 = PRINTPART2 + ",Frequency =," + str(OpFreq) + " GHz,Distance =," + str(Site2Distance)
    if FeetMeters == "F":
        PRINTPART2 = PRINTPART2 + " miles"
    if FeetMeters == "M":
        PRINTPART2 = PRINTPART2 + " km"

    if FeetMeters == "F":
        if FailFlag == 0:
            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
            if Test2Flag == 0:
                pass_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2) + "\n"

            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
            PRINTPART1 = PRINTPART1 + ",Worst Case Criterion 2 Clearance (feet) =," + str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
            if Test2Flag == 1:
                pass_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

        if FailFlag == 1:
            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
            if Test2Flag == 0:
                fail_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
            PRINTPART1 = PRINTPART1 + ",Worst Case Criterion 2 Clearance (feet) =," +str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
            if Test2Flag == 1:
                fail_stat_df.write(str(PathIndex) + "," + PRINTPART1 + PRINTPART2 + "\n")

    if FeetMeters == "M":
        if FailFlag == 0:
            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (meters) =," + str(WorstCaseClearance1) + ",at path distance (km) = ," + str(WorstCaseDistance1)
            if(Test2Flag == 0): fail_stat_df.write(PathIndex + "," + PRINTPART1 + PRINTPART2)
            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (feet) =," + str(WorstCaseClearance1) + ",at path distance (miles) = ," + str(WorstCaseDistance1)
            PRINTPART1 = str(PRINTPART1) + ",Worst Case Criterion 2 Clearance (feet) =," + str(WorstCaseClearance2) + ",at path distance (miles) = ," + str(WorstCaseDistance2)
            if Test2Flag == 1: fail_stat_df.write(PathIndex + "," + PRINTPART1 + PRINTPART2)

        if FailFlag == 1:
            PRINTPART1 = "PR" + str(ProfileNumber) + ".csv," + "Worst Case Criterion 1 Clearance (meters) =," + str(WorstCaseClearance1) + ",at path distance (km) = ," + str(WorstCaseDistance1)
            if Test2Flag == 0: fail_stat_df.write(str(PathIndex) + "," + str(PRINTPART1) + str(PRINTPART2))
            PRINTPART1 = str(PRINTPART1) + ",Worst Case Criterion 2 Clearance (meters) =," + str(WorstCaseClearance2) + ",at path distance (km) = ," + str(WorstCaseDistance2)
            if Test2Flag == 1: fail_stat_df.write(str(PathIndex) + "," + str(PRINTPART1) + str(PRINTPART2))


    ProfileNumberFilePath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"
    profile_number_df = pd.read_csv(ProfileNumberFilePath, header=None)      #11

    PointCount = 0
    for i, line in profile_number_df.iterrows():    #11
        PointCount = PointCount + 1

        distance = line[0]
        ELEVATION = line[1]
        ObstructionHeight = line[2]
        LUcode = line[3]
        LANDUSECODE = line[4]
        if PointCount == 1: TwrHt1 = float(ObstructionHeight)

    TwrHt2 = ObstructionHeight

    if FailFlag == 0:
        pass_site_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
        pass_site_df.write(str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "\n")
        pass_path_df.write(str(PathIndex) + "," + str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(Site2Distance) + "\n")
    
    if FailFlag == 1:
        fail_site_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
        fail_site_df.write(str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "\n")
        fail_path_df.write(str(PathIndex) + "," + str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(Site2Distance) + "\n")

    HoldFlag = FailFlag

    while True:     # this loop is intended to break on goto 500 statements -- scope in qbasic module is line 358 - 604
        if OptimizePaths != "Y": 
            break # goto 500
        
        if FailFlag == 0:       # Optimize the path

            SysOpt = "Y"
            ShortestTwr1 = TwrHt1
            ShortestTwr2 = TwrHt2
            ShortestWGrun = TwrHt1 + TwrHt2

            if FeetMeters == "F": 
                START1 = 10  #minimum tower height is 10 feet
                START2 = 10

            if FeetMeters == "M": 
                START1 = 3   #minimum tower height is 3 meters
                START2 = 3

            if START1 > float(TwrHt1 + .5): START1 = float(TwrHt1 + .5)     #tower heights in feet will increment in feet
            if START2 > float(TwrHt2 + .5): START2 = float(TwrHt2 + .5)

            if FeetMeters == "M": 
                START1 = START1 * 4 #tower heights in meters will increment in 0.25 m
                START2 = START2 * 4

            END1 = float(TwrHt1 + .5)
            END2 = float(TwrHt2 + .5)

            if FeetMeters == "M": 
                END1 = END1 * 4
                END2 = END2 * 4

            #Find buildings that can not move antenna heights
            SiteNoOpFilePath = ExampleS2AFolderPath + "/SiteNoOp.csv"
            site_no_op_df = pd.read_csv(SiteNoOpFilePath, header=None)      #88

            Site1Flag = 0
            Site2Flag = 0

            NUMBER_OF_LINES = site_no_op_df.shape[0] 
            for k in range(2, NUMBER_OF_LINES):
                SiteRow = site_no_op_df.iloc[k]  
                NoOpSite = SiteRow[0]
                if NoOpSite == SITE1: Site1Flag = 1
                if NoOpSite == SITE2: Site2Flag = 1

            while True: # goto 530 on break
                if Site1Flag == 1 and Site2Flag == 1:
                    ShortestAntHt1 = str(TwrHt1)
                    ShortestAntHt2 = str(TwrHt2)
                    break   #GOTO 530

                if Site1Flag == 1 or Site2Flag == 1: # unnecessary condition, left for easy comparison to original module

                    if Site1Flag == 1:
                        ShortestAntHt1 = str(TwrHt1)
                        TwrHtFlag = 1  # Optimize AntHt2#
                        optimize_one_tower(ShortestWGrun)
                        break     # GOTO 530

                    if Site2Flag == 1:
                        ShortestAntHt2 = str(TwrHt2)
                        TwrHtFlag = 0  # Optimize AntHt1#
                        optimize_one_tower(ShortestWGrun)
                        break   #GOTO 530

                TwrHtFlag = 0
                if TwrHt2 <= TwrHt1: TwrHtFlag = 1  # alway start optimization first with taller tower

                if TwrHtFlag == 0:
                    IISTART = START1
                    IIEND = END1
                    JJSTART = START2
                    JJEND = END2

                if TwrHtFlag == 1:
                    IISTART = START2
                    IIEND = END2
                    JJSTART = START1
                    JJEND = END1

                int_IIEND = int(IIEND)
                int_JJEND = int(JJEND)

                for II in range(IISTART, int_IIEND):
                    for JJ in range(JJSTART, int_JJEND, 10):
                        if TwrHtFlag == 0:
                            AntHt1 = IIEND - II + IISTART
                            if FeetMeters == "M": AntHt1 = AntHt1 / 4
                            AntHt2 = JJEND - JJ + JJSTART
                            if FeetMeters == "M": AntHt2 = AntHt2 / 4

                        if TwrHtFlag == 1:
                            AntHt2 = IIEND - II + IISTART
                            if FeetMeters == "M": AntHt2 = AntHt2 / 4
                            AntHt1 = JJEND - JJ + JJSTART
                            if FeetMeters == "M": AntHt1 = AntHt1 / 4
            
                        PCProfileFolderPath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"   #11
                        pc_profile_df = pd.read_csv(PCProfileFolderPath, header=None)

                        PointCount = 0
                        FailFlag = 0

                        for k, profile in pc_profile_df.iterrows():
                            PointCount = PointCount + 1

                            distance = profile[0]
                            ELEVATION = profile[1]
                            ObstructionHeight = profile[2]
                            LUcode = profile[3]
                            LANDUSECODE = profile[4]
                            
                            if PointCount == 1: 
                                continue    # GOTO 430
                            
                            Eval = 2
                            # call 2000 funciton here ########GOSUB 2000
                            Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

                        if FailFlag == 0: NewStart = JJ
                        if FailFlag == 1: break      # abandon current JJ loop and execute 510 restart code only if FailFlag = 1
                    
                    for JJ in range(NewStart, int_JJEND):
                        if TwrHtFlag == 0:
                            AntHt1 = IIEND - II + IISTART
                            if FeetMeters == "M": AntHt1 = AntHt1 / 4
                            AntHt2 = JJEND - JJ + JJSTART
                            if FeetMeters == "M": AntHt2 = AntHt2 / 4

                        if TwrHtFlag == 1:
                            AntHt2 = IIEND - II + IISTART
                            if FeetMeters == "M": AntHt2 = AntHt2 / 4
                            AntHt1 = JJEND - JJ + JJSTART
                            if FeetMeters == "M": AntHt1 = AntHt1 / 4

                        PerCent = 100 * (((II / IIEND) + (JJ / (IIEND * JJEND))) / (1 + (1 / JJEND)))
                        PerCent = float((PerCent * 100) + .5)
                        PerCent = PerCent / 100
                        PerCent = str(PerCent)
                        AntHt1 = str(AntHt1)
                        AntHt2 = str(AntHt2)

                        if FailFlag == 0: Info = "Path Clear"
                        if FailFlag == 1: Info = "Path Obstructed"

                        print("Path " + str(ProfileNumber) + " optimization = " + str(PerCent) + "%, (AntHt1 = " + str(AntHt1) + ", AntHt2 = " + str(AntHt2) + ", " + str(Info) + ")")

                        PCProfileFolderPath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"   #11
                        pc_profile_df = pd.read_csv(PCProfileFolderPath, header=None)

                        PointCount = 0
                        FailFlag = 0

                        for k, profile in pc_profile_df.iterrows():
                            PointCount = PointCount + 1

                            distance = profile[0]
                            ELEVATION = profile[1]
                            ObstructionHeight = profile[2]
                            LUcode = profile[3]
                            LANDUSECODE = profile[4]
                            
                            if PointCount == 1: continue

                            Eval = 2

                            # call 2000 here ########### GOSUB 2000
                            Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)
                        
                        if FailFlag == 0:
                            WGrun = float(AntHt1) + float(AntHt2)
                            if WGrun < ShortestWGrun:
                                ShortestWGrun = WGrun
                                ShortestAntHt1 = float(AntHt1)
                                ShortestAntHt2 = float(AntHt2)
                                ShortestAntHt1 = float((ShortestAntHt1 * 100) + .5)
                                ShortestAntHt1 = ShortestAntHt1 / 100
                                ShortestAntHt1 = str(ShortestAntHt1)
                                ShortestAntHt2 = float((ShortestAntHt2 * 100) + .5)
                                ShortestAntHt2 = ShortestAntHt2 / 100
                                ShortestAntHt2 = str(ShortestAntHt2)

                        if FailFlag == 1: break     # exit JJ loop and go to next II

                break   # break point where Goto 530 statments start

            #530 'Create the optimized link profile and link evaluation files
            # still within scope of if (failflag == 0)
            PCFolderPath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"      #11
            pc_df = pd.read_csv(PCFolderPath, header=None)

            PRFolderPath = ExampleS2AFolderPath + "/Optimize/PR" + str(ProfileNumber) + ".csv"      #12
            pr_df = open(PRFolderPath, "w")

            EVFolderPath = ExampleS2AFolderPath + "/Optimize/EV" + str(ProfileNumber) + ".csv"      #13
            ev_df = open(EVFolderPath, "w")

            PointCount = 0

            PRINTFILE = str(PathIndex) + "," + str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
            PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2) + ","
            PRINTFILE = PRINTFILE + str(ShortestAntHt1) + "," + str(ShortestAntHt2) + "," + str(Site2Distance) + "," + str(OpFreq)
            final_path_data_df.write(PRINTFILE + "\n")

            pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
            ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")

            for k, profile in pc_df.iterrows():
                PointCount = PointCount + 1

                distance = profile[0]
                ELEVATION = profile[1]
                ObstructionHeight = profile[2]
                LUcode = profile[3]
                LANDUSECODE = profile[4]

                if PointCount == 1: ObstructionHeight = ShortestAntHt1
                pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

                Eval = 2
                AntHt1 = ShortestAntHt1
                AntHt2 = ShortestAntHt2
                EarthHeight2 = 0
                ModifiedPathHeight2 = 0

                # call 2000 function here ######## GOSUB 2000
                Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

                TerrainHeight = ELEVATION + float(ObstructionHeight)

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
        SysFail = "Y"

        PCFolderPath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"      #11
        pc_df = pd.read_csv(PCFolderPath, header=None)

        PRFolderPath = ExampleS2AFolderPath + "/Failed/PR" + str(ProfileNumber) + ".csv"      #12
        pr_df = open(PRFolderPath, "w")

        EVFolderPath = ExampleS2AFolderPath + "/Failed/EV" + str(ProfileNumber) + ".csv"      #13
        ev_df = open(EVFolderPath, "w")    

        PointCount = 0
        ShortestAntHt1 = TwrHt1
        ShortestAntHt2 = TwrHt2

        PRINTFILE = str(PathIndex) + "," + str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
        PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2) + ","
        PRINTFILE = PRINTFILE + str(ShortestAntHt1) + "," + str(ShortestAntHt2) + "," + str(Site2Distance) + "," + str(OpFreq)
        failed_path_data_df.write(PRINTFILE + "\n")

        pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
        ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")

        
        for k, profile in pc_df.iterrows():
            PointCount = PointCount + 1

            distance = profile[0]
            ELEVATION = profile[1]
            ObstructionHeight = profile[2]
            LUcode = profile[3]
            LANDUSECODE = profile[4]

            if PointCount == 1: ObstructionHeight = ShortestAntHt1
            pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

            Eval = 2
            AntHt1 = ShortestAntHt1
            AntHt2 = ShortestAntHt2
            EarthHeight2 = 0
            ModifiedPathHeight2 = 0

            # call 2000 function here ######### GOSUB 2000
            Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone  = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

            TerrainHeight = ELEVATION + ObstructionHeight

            if PointCount == 1:
                PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(PathHeight) + ","
            else:
                PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(EarthHeight1) + "," + str(EarthHeight2) + "," + str(PathHeight) + ","
            PRINTFILE = str(PRINTFILE) + str(ModifiedPathHeight1) + "," + str(ModifiedPathHeight2)
            ev_df.write(PRINTFILE + "\n")

            EVDuplicatePath = ExampleS2AFolderPath + "/Passed/EV" + str(ProfileNumber) + ".csv"      
            PRDuplicatePath = ExampleS2AFolderPath + "/Passed/PR" + str(ProfileNumber) + ".csv"      

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
        SysPass = "Y"

        PCFolderPath = ExampleS2AFolderPath + "/TempFile/PC" + str(ProfileNumber) + ".csv"      #11
        pc_df = pd.read_csv(PCFolderPath, header=None)

        PRFolderPath = ExampleS2AFolderPath + "/Passed/PR" + str(ProfileNumber) + ".csv"      #12
        pr_df = open(PRFolderPath, "w")

        EVFolderPath = ExampleS2AFolderPath + "/Passed/EV" + str(ProfileNumber) + ".csv"      #13
        ev_df = open(EVFolderPath, "w")

        PointCount = 0
        ShortestAntHt1 = TwrHt1
        ShortestAntHt2 = TwrHt2

        PRINTFILE = str(PathIndex) + "," + str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(SITE2) + ","
        PRINTFILE = PRINTFILE + str(Latitude2) + "," + str(Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2) + ","
        PRINTFILE = PRINTFILE + str(ShortestAntHt1) + "," + str(ShortestAntHt2) + "," + str(Site2Distance) + "," + str(OpFreq)
        passed_path_data_df.write(PRINTFILE + "\n")

        pr_df.write("Distance,Elevation,ObstructionHeight,Obs Code, Obs Type" + "\n")
        ev_df.write("Distance,TerrainHeight,EarthHeight1,EarthHeight2,PathHeight,ModifiedPathHeight1,ModifiedPathHeight2" + "\n")

        for k, profile in pc_df.iterrows():
            PointCount = PointCount + 1

            distance = profile[0]
            ELEVATION = profile[1]
            ObstructionHeight = profile[2]
            LUcode = profile[3]
            LANDUSECODE = profile[4]

            if PointCount == 1: ObstructionHeight = ShortestAntHt1
            pr_df.write(str(distance) + "," + str(ELEVATION) + "," + str(ObstructionHeight) + "," + str(LUcode) + "," + str(LANDUSECODE) + "\n")

            Eval = 2
            AntHt1 = ShortestAntHt1
            AntHt2 = ShortestAntHt2
            EarthHeight2 = 0
            ModifiedPathHeight2 = 0

            # call 2000 function here ##### GOSUB 2000
            Clearance1, Clearance2, EarthHeight1, EarthHeight2, PathHeight, ModifiedPathHeight1, ModifiedPathHeight2, FirstFresnelTestHeight, SecondFresnelTestHeight, SecondKFactorMod, FailFlag, FirstFresnelZone = point_on_path(distance, ELEVATION, ObstructionHeight,FailFlag,AddlClearance,ITURkFactor,SecondKFactor,Test2Flag)

            TerrainHeight = ELEVATION + ObstructionHeight

            if PointCount == 1:
                PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(TerrainHeight) + "," + str(PathHeight) + ","
            else:
                PRINTFILE = str(distance) + "," + str(TerrainHeight) + "," + str(EarthHeight1) + "," + str(EarthHeight2) + "," + str(PathHeight) + ","
            PRINTFILE = str(PRINTFILE) + str(ModifiedPathHeight1) + "," + str(ModifiedPathHeight2)
            ev_df.write(PRINTFILE + "\n")


            EVDuplicatePath = ExampleS2AFolderPath + "/Failed/EV" + str(ProfileNumber) + ".csv"      
            PRDuplicatePath = ExampleS2AFolderPath + "/Failed/PR" + str(ProfileNumber) + ".csv"      
    
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

StatusFilePath = ExampleS2AFolderPath + "/TempFile/Status.csv"      #57
status_df = open(StatusFilePath, "w")

status_df.write("Optimized Paths?," + str(SysOpt) + "\n")
status_df.write("Failed Paths?," + str(SysFail) + "\n")
status_df.write("Passed Paths?," + str(SysPass) + "\n")

status_df.close()

pass_path_df.flush()
pass_path_df.close()

# Eliminate duplicates from passed sites list
print("     Eliminating duplicates from passed sites list")

pass_site_df.close()    # attempted bug fix

PassSiteFilePath2 = ExampleS2AFolderPath + "/Passed/PassSite.csv"
pass_site_df = pd.read_csv(PassSiteFilePath2, header=None)       #56

Temp1FilePath = ExampleS2AFolderPath + "/TempFile/Temp1.csv"
temp1_df = open(Temp1FilePath, "w")         #57 

for i, row in pass_site_df.iterrows():
    SITE1 = row[0]
    Latitude1 = row[1]
    Longitude1 = row[2]

    temp1_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")

pass_site_df = open(PassSiteFilePath2, "w")              #57
pass_site_df.close()        

temp1_df.close()    
temp1_df = pd.read_csv(Temp1FilePath, header=None)       #56

for i, row in temp1_df.iterrows():
    SITE1 = row[0]
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
            
            if SITE1 == SiteA:
                Flag = 1     

    if Flag == 0:
        pass_site_df = open(PassSiteFilePath2, "a")      #57
        pass_site_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
        pass_site_df.flush()
        pass_site_df.close()    

# Eliminate duplicates from failed sites list
print("     Eliminating duplicates from failed sites list")
fail_site_df.flush()
fail_site_df.close()   

FailSiteFilePath2 = ExampleS2AFolderPath + "/Failed/FailSite.csv"
failed_site_df = pd.read_csv(FailSiteFilePath2, header=None)       #56

Temp1FilePath2 = ExampleS2AFolderPath + "/TempFile/Temp1.csv"
temp1_df = open(Temp1FilePath2, "w")        #57

for i, row in failed_site_df.iterrows():
    SITE1 = row[0]
    Latitude1 = row[1]
    Longitude1  = row[2]

    temp1_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")

temp1_df.flush()
temp1_df.close()
temp1_df = pd.read_csv(Temp1FilePath2, header=None)     #56

for i, row in temp1_df.iterrows():
    SITE1 = row[0]
    Latitude1 = row[1]
    Longitude1 = row[2]
    
    failed_site_df = pd.read_csv(FailSiteFilePath2, header=None)        #57

    Flag = 0
    for k, line in failed_site_df.iterrows():
        SiteA = line[0]
        LATITUDEA = line[1]
        LONGITUDEA = line[2]
        
        if SITE1 == SiteA: 
            Flag = 1

    if Flag == 0:
        failed_site_df = open(FailSiteFilePath2, "a")       #57
        failed_site_df.write(str(SITE1) + "," + str(Latitude1) + "," + str(Longitude1) + "\n")
        failed_site_df.flush()
        failed_site_df.close()  # CLOSE #57

# Create the Google Earth/KML mapping files '+++++++++++++++++++++++++++++
os.system('cls' if os.name == 'nt' else 'clear')
# Passed sites and paths
InputFileSites = ExampleS2AFolderPath + "/Passed/PassSite.csv"
InputFilePaths = ExampleS2AFolderPath + "/Passed/PassPath.csv"
OutputFileGoogle = ExampleS2AFolderPath + "/Passed/Google/GEPaths.KML"
# Create Maps
createKML(InputFileSites, InputFilePaths, OutputFileGoogle)

# Failed sites and paths
InputFileSites = ExampleS2AFolderPath + "/Failed/FailSite.csv"
InputFilePaths = ExampleS2AFolderPath + "/Failed/FailPath.csv"
OutputFileGoogle = ExampleS2AFolderPath + "/Failed/Google/GEPaths.KML"
# Create Maps
createKML(InputFileSites, InputFilePaths, OutputFileGoogle)

print("\nProgram Completed\n")
input("Press <Enter> key to clear this window")
