# Path Spider Web Creation Program

import math
import numpy
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

def Label4000(ExampleS2AFolderPath, TowerHt, Both):
    SitesFilePath = ExampleS2AFolderPath + "/Sites.csv"
    sites_df = pd.read_csv(SitesFilePath)

    Temp1FilePath = ExampleS2AFolderPath + "/TempFile/Temp1.csv"
    temp1_df = open(Temp1FilePath, "w") 

    Temp2FilePath = ExampleS2AFolderPath + "/TempFile/Temp2.csv"
    temp2_df = open(Temp2FilePath, "w") 

    # grab corresponding headers from sites file
    headers = list(sites_df.columns)      

    if TowerHt.upper() == "N" and Both.upper() == "N":
        HEADER1 = headers[0]
        HEADER2 = headers[1]
        HEADER3 = headers[2]

        if HEADER1 != "Site" and HEADER2 != "Latitude" and HEADER3 != "Longitude":
            print("Input file header descriptions are not as expected.")
            print("They should be <Site>, <Latitude> and <Longitude> respectively.")
            print("The program has been terminated.")
            sys.exit()

    # i think this block should test header4, but the basic module doesn't
    if TowerHt.upper() == "Y" and Both.upper() == "N":
        HEADER1 = headers[0]
        HEADER2 = headers[1]
        HEADER3 = headers[2]
        HEADER4 = headers[3]  

        if HEADER1 != "Site" and HEADER2 != "Latitude" and HEADER3 != "Longitude":
            print("Input file header descriptions are not as expected.")
            print("They should be <Site>, <Latitude> and <Longitude> respectively.")
            print("The program has been terminated.")
            sys.exit()

    # i think this block should test header4 and header5, but the basic module doesn't
    if TowerHt.upper() == "N" and Both.upper() == "Y":
        HEADER1 = headers[0]
        HEADER2 = headers[1]
        HEADER3 = headers[2]
        HEADER4 = headers[3]        
        HEADER5 = headers[4] 

        if HEADER1 != "Site" and HEADER2 != "Latitude" and HEADER3 != "Longitude" and HEADER4 != "TowerHeight":
            print("Input file header descriptions are not as expected.")
            print("They should be <Site>, <Latitude> and <Longitude> respectively.")
            print("The program has been terminated.")
            sys.exit()

    # line 206
    # grab corresponding first row of sites file
    if TowerHt == "N" and Both == "N":
        SitesRow = sites_df.iloc[0] 

        Site = SitesRow[0]
        Latitude = SitesRow[1]
        Longitude = SitesRow[2]

        PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "\n"
        temp1_df.write(PrintFile)
        
    if TowerHt == "Y" and Both == "N":
        SitesRow = sites_df.iloc[0] 

        Site = SitesRow[0]
        Latitude = SitesRow[1]
        Longitude = SitesRow[2]
        TwrHt = SitesRow[3]

        PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "\n"
        temp1_df.write(PrintFile)

    if TowerHt == "N" and Both == "Y":
        SitesRow = sites_df.iloc[0] 

        Site = SitesRow[0]
        Latitude = SitesRow[1]
        Longitude = SitesRow[2]
        TwrHt = SitesRow[3]
        State = SitesRow[4]

        PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "," + str(State) + "\n"
        temp1_df.write(PrintFile)

    NUMBER_OF_SITES = sites_df.shape[0]
    for index in range(1, NUMBER_OF_SITES):    
        SitesRow = sites_df.iloc[index] 

        if TowerHt == "N" and Both == "N":
            Site = SitesRow[0]
            Latitude = SitesRow[1]
            Longitude = SitesRow[2]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "\n"
            temp1_df.write(PrintFile)
            temp2_df.write(PrintFile)
            
        if TowerHt == "Y" and Both == "N":
            Site = SitesRow[0]
            Latitude = SitesRow[1]
            Longitude = SitesRow[2]
            TwrHt = SitesRow[3]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "\n"
            temp1_df.write(PrintFile)
            temp2_df.write(PrintFile)

        if TowerHt == "N" and Both == "Y": 
            Site = SitesRow[0]
            Latitude = SitesRow[1]
            Longitude = SitesRow[2]
            TwrHt = SitesRow[3]
            State = SitesRow[4]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "," + str(State) + "\n"
            temp1_df.write(PrintFile)
            temp2_df.write(PrintFile)

    temp1_df.close()
    temp2_df.close()

    return NUMBER_OF_SITES

def Label5000(ExampleS2AFolderPath, TowerHt, Both):
    Temp2FilePath = ExampleS2AFolderPath + "/TempFile/Temp2.csv"    # temp2_df == #11 in the basic module
    temp2_df = pd.read_csv(Temp2FilePath, header=None)

    Temp1FilePath = ExampleS2AFolderPath + "/TempFile/Temp1.csv"    # temp1_df == #12 in the basic module
    temp1_df = open(Temp1FilePath, "w+") 

    SiteCount = 0

    for i, row in temp2_df.iterrows():
        SiteCount += 1

        if TowerHt == "N" and Both == "N":
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "\n"
            temp1_df.write(PrintFile)

        if TowerHt == "Y" and Both == "N":
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]
            TwrHt = row[3]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "\n"
            temp1_df.write(PrintFile)

        if TowerHt == "N" and Both == "Y": 
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]
            TwrHt = row[3]
            State = row[4]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "," + str(State) + "\n"
            temp1_df.write(PrintFile)
            
    temp1_df.close()
            
    Temp1FilePath = ExampleS2AFolderPath + "/TempFile/Temp1.csv"    # temp1_df == #11 in the basic module
    temp1_df = pd.read_csv(Temp1FilePath, header=None)

    Temp2FilePath = ExampleS2AFolderPath + "/TempFile/Temp2.csv"    # temp2_df == #12 in the basic module
    temp2_df = open(Temp2FilePath, "w+") 
            
    row = temp1_df.iloc[0] 
    
    if TowerHt == "N" and Both == "N":
        Site = row[0]
        Latitude = row[1]
        Longitude = row[2]

    if TowerHt == "Y" and Both == "N":
        Site = row[0]
        Latitude = row[1]
        Longitude = row[2]
        TwrHt = row[3]

    if TowerHt == "N" and Both == "Y":
        Site = row[0]
        Latitude = row[1]
        Longitude = row[2]
        TwrHt = row[3]
        State = row[4] 

    NUMBER_OF_ROWS = temp1_df.shape[0]              # line 316
    for index in range(1, NUMBER_OF_ROWS):      
        row = temp1_df.iloc[index] 

        if TowerHt == "N" and Both == "N":
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "\n"
            temp2_df.write(PrintFile)

        if TowerHt == "Y" and Both == "N":
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]
            TwrHt = row[3]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "\n"
            temp2_df.write(PrintFile)

        if TowerHt == "N" and Both == "Y":
            Site = row[0]
            Latitude = row[1]
            Longitude = row[2]
            TwrHt = row[3]
            State = row[4]

            PrintFile = str(Site) + "," + str(Latitude) + "," + str(Longitude) + "," + str(TwrHt) + "," + str(State) + "\n"
            temp2_df.write(PrintFile)

    temp2_df.close()
    return SiteCount
    

# INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
# OUTPUT: Zmiles# (DISTANCE IN MILES), Zkm# (DISTANCE IN KILOMETERS)
def Label6000(LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB, MilesKm):
    # HIGH ACCURACY FORMULA
    Z = (math.sin((math.pi * (LATITUDEA - LATITUDEB) / 180) / 2)) ** 2
    Z = Z + math.cos(math.pi * LATITUDEA / 180) * math.cos(math.pi * LATITUDEB / 180) * ((math.sin((math.pi * (LONGITUDEA - LONGITUDEB) / 180) / 2)) ** 2)
    Z = math.sqrt(Z)
    X = Z

    ARCSIN = numpy.arcsin(Z)

    ZSHORT = 2 * (180 / math.pi) * ARCSIN
    Zkm = 111.1 * ZSHORT            # DISTANCE IN KILOMETERS
    Zmiles = 69.06 * ZSHORT         # DISTANCE IN MILES

    Distance = -1       # bad MilesKm value flag
    DistanceExp = -1 

    if MilesKm.upper() == "M":
        Distance = Zmiles
        DistanceExp = 5280 * Distance

    if MilesKm == "K":
        Distance = Zkm
        DistanceExp = 1000 * Distance

    return Distance, DistanceExp


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

# open main folder
ExampleS2AFolderPath = ex.openFolderNameDialog("Find ExampleS2A Folder")

print("Input file format is <Site$,Latitude$,Longitude$>")
print("or <Site$,Latitude$,Longitude$,TwrHt$>")
print("or <Site$,Latitude$,Longitude$,TwrHt$,State$>")
print()
print("Input file has a header with the first three (or four) header labels:")
print("<Site>, <Latitude>, <Longitude> (and <TowerHeight)>")
print("Input file may have three, four or five columns.")
print()
print("The folder containing the site data also requires a <TempFile> folder.")
print()

# Label 50
print("Does the input file contain a tower height column but no State column?")
TowerHt = str(input("Enter Y or y for Yes, N or n for No or nothing to terminate program: "))
TowerHt = TowerHt.upper()  

while(TowerHt.upper() != "N" and TowerHt.upper() != "Y" and TowerHt != ""):
    print("\nDoes the input file contain a tower height column but no State column?")
    TowerHt = str(input("Enter Y or y for Yes, N or n for No or nothing to terminate program: "))

if(TowerHt == ""):
    sys.exit()

# Label 55
print("\nDoes the input file contain a tower height column AND a State column?")
Both = input("Enter Y or y for Yes, N or n for No or nothing to terminate program: ")
Both = Both.upper() 

while(Both.upper() != "N" and Both.upper() != "Y" and Both != ""):
    print("\nDoes the input file contain a tower height column AND a State column?")
    Both = input("Enter Y or y for Yes, N or n for No or nothing to terminate program: ")

if(Both == ""):
    sys.exit()

# Label 60

if TowerHt.upper() == "N" and Both.upper() == "N":
    print("\nThe input file does NOT contain tower or state columns.")
if TowerHt.upper() == "Y" and Both.upper() == "N":
    print("\nThe input file contains ONLY a tower column.")
if TowerHt.upper() == "N" and Both.upper() == "Y":
    print("\nThe input file contains both tower AND state columns.")

MaxDistance = input("\nEnter the maximum path distance (miles or kilometers): ")

# Label 70
print("\nIs the distance in miles (M) or kilometers (K)?")
MilesKm = input("Enter M or m for miles, K or k for kilometers: ")

while(MilesKm.upper() != "M" and MilesKm.upper() != "K" and MilesKm != ""):
    print("\nIs the distance in miles (M) or kilometers (K)?")
    MilesKm = input("Enter M or m for miles, K or k for kilometers: ")

print()

if(MilesKm == ""):
    sys.exit()

# Label 80
SiteCount = Label4000(ExampleS2AFolderPath, TowerHt.upper(), Both.upper())

PathsFilePath = ExampleS2AFolderPath + "/Paths.csv"
paths_df = open(PathsFilePath, "w+") 

if TowerHt == "N" and Both == "N":
    paths_df.write("Site1,Latitude1,Longitude1,Site2,Latitude2,Longitude2,Distance(m or km),Distance(ft or m)\n")
if TowerHt == "Y" and Both == "N":
    paths_df.write("Site1,Latitude1,Longitude1,Site2,Latitude2,Longitude2,TowerHeight1,TowerHeight2,Distance(m or km),Distance(ft or m)\n")
if TowerHt == "N" and Both == "Y":
    paths_df.write("Site1,Latitude1,Longitude1,Site2,Latitude2,Longitude2,TowerHeight1,TowerHeight2,State1,State2,Distance(m or km),Distance(ft or m)\n")

PathsFilePath = ExampleS2AFolderPath + "/Paths1.csv"
paths1_df = open(PathsFilePath, "w+") 

paths1_df.write("Site1,Latitude1,Longitude1,Site2,Latitude2,Longitude2,TowerHeight1,TowerHeight2\n")

# Label 100

while(SiteCount > 1):     # defined in 4000/5000 functions
    
    # Begin path creation
    Temp1FilePath = ExampleS2AFolderPath + "/TempFile/Temp1.CSV"
    temp1_df = pd.read_csv(Temp1FilePath, header=None)

    row1 = temp1_df.iloc[0]

    TowerHeight1 = ""
    State1 = ""

    if TowerHt.upper() == "N" and Both.upper() == "N":
        Site1 = str(row1[0])
        Latitude1 = float(row1[1])
        Longitude1 = float(row1[2])

    if TowerHt.upper() == "Y" and Both.upper() == "N":
        Site1 = str(row1[0])
        Latitude1 = float(row1[1])
        Longitude1 = float(row1[2])
        TowerHeight1 = row1[3]

    if TowerHt.upper() == "N" and Both.upper() == "Y":
        Site1 = str(row1[0])
        Latitude1 = float(row1[1])
        Longitude1 = float(row1[2])
        TowerHeight1 = row1[3]
        State1 = row1[4]

    NUMBER_OF_ROWS = temp1_df.shape[0]          # number of paths is equal to the number of rows in "temp1" file
    for index in range(1, NUMBER_OF_ROWS):      # skip row 1 of csv
        row2 = temp1_df.iloc[index]

        TowerHeight2 = ""
        State2 = ""

        if TowerHt.upper() == "N" and Both.upper() == "N":
            Site2 = str(row2[0])
            Latitude2 = float(row2[1])
            Longitude2 = float(row2[2])

        if TowerHt.upper() == "Y" and Both.upper() == "N":
            Site2 = str(row2[0])
            Latitude2 = float(row2[1])
            Longitude2 = float(row2[2])
            TowerHeight2 = row2[3]

        if TowerHt.upper() == "N" and Both.upper() == "Y":
            Site2 = str(row2[0])
            Latitude2 = float(row2[1])
            Longitude2 = float(row2[2])
            TowerHeight2 = row2[3]
            State2 = row2[4]

        ########################################## Line 114 ##########################################

        LATITUDEA = Latitude1
        LATITUDEB = Latitude2
        LONGITUDEA = Longitude1
        LONGITUDEB = Longitude2

        Distance, DistanceExp = Label6000(LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB, MilesKm.upper()) 

        if Distance < 0.1:     
            Distance = 0.0
        if DistanceExp < 0.1:
            DistanceExp = 0.0

        if Distance <= float(MaxDistance):
            PrintFile1 = str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + ","
            PrintFile1 = str(PrintFile1) + str(Latitude2) + "," + str(Longitude2) + "," + str(Distance) + "," + str(DistanceExp) + "\n"

            PrintFile2 = str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + ","
            PrintFile2 = str(PrintFile2) + str(Longitude2) + "," + str(TowerHeight1) + "," + str(TowerHeight2) + "," + str(Distance) + "," + str(DistanceExp) + "\n"
            
            PrintFile3 = str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + ","
            PrintFile3 = str(PrintFile3) + str(Longitude2) + "," + str(TowerHeight1) + "," + str(TowerHeight2) + ","
            PrintFile3 = str(PrintFile3) + str(State1) + "," + str(State2) + "," + str(Distance) + "," + str(DistanceExp) + "\n"

            if TowerHt == "N" and Both == "N":
                paths_df.write(PrintFile1)
            if TowerHt == "Y" and Both == "N":
                paths_df.write(PrintFile2)
            if TowerHt == "N" and Both == "Y":
                paths_df.write(PrintFile3)

            PrintFile4 = str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + ","
            PrintFile4 = str(PrintFile4) + str(Longitude2) + "," + str(TowerHeight1) + "," + str(TowerHeight2) + "\n"
            paths1_df.write(PrintFile4)

            print(str(Site1) + "," + str(Site2) + "," + str(Distance))
        
    SiteCount = Label5000(ExampleS2AFolderPath, TowerHt.upper(), Both.upper())

print("\nProgram Completed")
print("\nPress <Enter> key to clear this window")
input()
