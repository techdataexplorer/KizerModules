#Make KML for paths
#FILE IS IN SPRINT FORMAT
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

def printToKml(output,temp,TEMPFILE,row,PathColor,FenceColor,PathInfo,ThePath,Altitude,Range,Tilt,Azimuth,PathsOnlyYN,SiteTitleYN,FlagS1,FlagS2,HEIGHT1,HEIGHT2): 

    temp.close()
    temp = open(TEMPFILE, "a")            

    if (FlagS1 == 0):
        temp.write(row[1])
        temp.write("\n")
    if (FlagS2 == 0):
        temp.write(row[4])
        temp.write("\n")
    temp.close()

    output.write("\n<Style id=" + chr(34) + "blackLineGreenPoly" + chr(34) + ">")
    output.write("\n<LineStyle>\n")
    output.write(PathColor)
    output.write("\n<width>4</width>")
    output.write("\n</LineStyle>")
    output.write("\n<PolyStyle>\n")
    output.write(FenceColor)
    output.write("\n</PolyStyle>")
    output.write("\n</Style>")
    output.write("\n<Placemark>")  
    output.write("\n<name>" + PathInfo + "</name>")
    output.write("\n<description>Path Between " + ThePath + "</description>")
    output.write("\n<LookAt>")
    output.write("\n<longitude>{}</longitude>".format(row[3]))
    output.write("\n<latitude>{}</latitude>".format(row[2]))
    output.write("\n<altitude>{}</altitude>".format(Altitude))
    output.write("\n<range>{}</range>".format(Range))
    output.write("\n<tilt>{}</tilt>".format(Tilt))
    output.write("\n<heading>{}</heading>".format(Azimuth))
    output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
    output.write("\n</LookAt>")
    output.write("\n<styleUrl>#blackLineGreenPoly</styleUrl>")
    output.write("\n<LineString>")
    output.write("\n<extrude>1</extrude>")
    output.write("\n<tessellate>1</tessellate>")
    output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
    output.write("\n<coordinates>{},{},{}".format(row[3],row[2],HEIGHT1))#height in feet
    output.write("\n{},{},{}".format(row[6],row[5],HEIGHT2))
    output.write("\n</coordinates>")
    output.write("\n</LineString>")
    output.write("\n</Placemark>")
    output.write("\n")

    #Sites
    if(PathsOnlyYN=="Y"):
        printToKml(output,temp,TEMPFILE,row,PathColor,FenceColor,PathInfo,ThePath,Altitude,Range,Tilt,Azimuth,PathsOnlyYN,SiteTitleYN,FlagS1,FlagS2,HEIGHT1,HEIGHT2)
        
    output.write("\n<Placemark>")
    output.write("\n<description>Microwave Site</description>")
    output.write("\n<name>{}</name>".format(row[1]))
    if(SiteTitleYN=="Y"):
        output.write("\n<visibility>1</visibility>")
    if(SiteTitleYN != "Y" ):
        output.write("\n<visibility>0</visibility>")
    output.write("\n<Style>")
    output.write("\n<IconStyle>")
    output.write("\n<color>ff0000ff</color>")
    output.write("\n<scale>0.7</scale>")
    output.write("\n<Icon>")
    output.write("\n<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>")
    output.write("\n</Icon>")
    output.write("\n</IconStyle>")
    output.write("\n<LabelStyle>")
    output.write("\n<scale>0.9</scale>")
    output.write("\n</LabelStyle>")
    output.write("\n</Style>")
    output.write("\n<Point>")
    output.write("\n<IconAltitude>1</IconAltitude>")
    output.write("\n<extrude>1</extrude>")
    output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
    output.write("\n<coordinates>{},{},0</coordinates>".format(row[3],row[2]))
    output.write("\n</Point>")
    output.write("\n</Placemark>")
    output.write("\n<Placemark>")
    output.write("\n<description>Microwave Site</description>")
    output.write("\n<name>{}</name>".format(row[4]))
    if(SiteTitleYN=="Y"):
        output.write("\n<visibility>1</visibility>")
    if(SiteTitleYN!="Y" ):
        output.write("\n<visibility>0</visibility>")
    output.write("\n<Style>")
    output.write("\n<IconStyle>")
    output.write("\n<color>ff0000ff</color>")
    output.write("\n<scale>0.7</scale>")
    output.write("\n<Icon>")
    output.write("\n<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>")
    output.write("\n</Icon>")
    output.write("\n</IconStyle>")
    output.write("\n<LabelStyle>")
    output.write("\n<scale>0.9</scale>")
    output.write("\n</LabelStyle>")
    output.write("\n</Style>")
    output.write("\n<Point>")
    output.write("\n<IconAltitude>1</IconAltitude>")
    output.write("\n<extrude>1</extrude>")
    output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
    output.write("\n<coordinates>{},{},0</coordinates>".format(row[6],row[5]))
    output.write("\n</Point>")
    output.write("\n</Placemark>")
    output.write("\n")


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

os.system('cls' if os.name == 'nt' else 'clear')

FolderPath = ex.openFolderNameDialog("Select Folder Name")

print("\nKML Path Creater")
print("DEVELOPED BY George Kizer, TeleVision.Inc")
print("COPYRIGHT 2011")
print("ALL RIGHTS RESERVED")
print("\nSPRINT SPECIAL FORMAT\n")
print("INPUT FILE:")
print("C:\FOLDER\XXXX.CSV")
print("XXXX.CSV is 9 column file format")
print("Input Format: Index,Site1,Latitude1,Longitude1,Site2,Latitude2,Longitude2,TowerHeight1,TowerHeight2\n")
print("OUTPUT FILE:")
print("C:\FOLDER\XXXX.kml\n")

print("INPUT THE FOLDER NAME (e.g.,Working\LA) ")
print("C:\ in front of folder name is implied. ")
print("Output file PATHS.KML will appear in this file.")

ROOTFILE = FolderPath  

print("\nINPUT PATHS FILE NAME (e.g., ThePaths) ")
PathsName = input(".CSV file name extension is implied. \n")

os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("Choose a FENCE color:\n")

    print("1 = Black")
    print("2 = Red")
    print("3 = Green")
    print("4 = Blue")
    print("5 = Yellow")
    print("6 = Brown")
    print("7 = Orange")
    print("8 = LtGreen\n")

    TheColor = int(input())
    if(TheColor >= 1 and TheColor <= 8):
        break
        
if TheColor == 1:
    FenceColor = "<color>7f000000</color>"
elif TheColor == 2:
    FenceColor = "<color>7f0000ff</color>"
elif TheColor == 3:
    FenceColor = "<color>7f00ff00</color>"
elif TheColor == 4:
    FenceColor = "<color>7fff0000</color>"
elif TheColor == 5:
    FenceColor = "<color>7f00ffff</color>"
elif TheColor == 6:
    FenceColor = "<color>7f000040</color>"
elif TheColor == 7:
    FenceColor = "<color>7f0080ff</color>"
elif TheColor == 8:
    FenceColor = "<color>7f00ff80</color>"

os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("Choose a PATH color:\n")

    print("1 = Black")
    print("2 = Red")
    print("3 = Green")
    print("4 = Blue")
    print("5 = Yellow")
    print("6 = Brown")
    print("7 = Orange")
    print("8 = LtGreen\n")

    TheColor = int(input())
    if(TheColor >= 1 and TheColor <= 8):
        break
        
if TheColor == 1:
    PathColor = "<color>7f000000</color>"
elif TheColor == 2:
    PathColor = "<color>7f0000ff</color>"
elif TheColor == 3:
    PathColor = "<color>7f00ff00</color>"
elif TheColor == 4:
    PathColor = "<color>7fff0000</color>"
elif TheColor == 5:
    PathColor = "<color>7f00ffff</color>"
elif TheColor == 6:
    PathColor = "<color>7f000040</color>"
elif TheColor == 7:
    PathColor = "<color>7f0080ff</color>"
elif TheColor == 8:
    PathColor = "<color>7f00ff80</color>"

print("Does your file have a header (Y/N)?")
HeaderYN = input()
if HeaderYN == "y":
    HeaderYN = "Y"

print("Do you want site titles (Y/N)?")
SiteTitleYN = input()
if SiteTitleYN == "y":
    SiteTitleYN = "Y"

print("Do you want to avoid sites altogether (Y/N)?")
print("(only paths without any site markings)")
PathsOnlyYN = input()
if PathsOnlyYN == "y":
    PathsOnlyYN = "Y"

PRIMARYFILE = ROOTFILE + "/" + PathsName +".CSV"                     
OUTPUTFILE = ROOTFILE + "/" + PathsName + ".KML" #KML file
TEMPFILE = FolderPath + "/TempFile.csv" 



primary_df = pd.read_csv(PRIMARYFILE)   
output = open(OUTPUTFILE, "w")          
temp = open(TEMPFILE, "w")              
temp.close() #create an empty file

if HeaderYN == 'Y':
    headers = list(primary_df.columns)

#begin creating KML file

output.write("<?xml version=" + chr(34) + "1.0" + chr(34) + " encoding=" + chr(34) + "UTF-8" + chr(34) + "?>")
output.write("\n<kml xmlns=" + chr(34) + "http://www.opengis.net/kml/2.2" + chr(34) + ">")
output.write("\n<Document>")
output.write("\n<name>" + PathsName + " System Map</name>")
output.write("\n<description>Microwave Paths</description>")
output.write("\n")

DISTANCE = ""
FREQ = ""

ROW = None
for index, row in primary_df.iterrows():
    ROW = row
    INDEX = int(row[0])
    SITE1 = str(row[1])
    LAT1 = float(row[2])
    LON1 = float(row[3])
    SITE2 = str(row[4])
    LAT2 = float(row[5])
    LON2 = float(row[6])
    HEIGHT1 = float(row[7])
    HEIGHT2 = float(row[8])

    #Convert heights in feet to heights in meters
    HEIGHT1 = HEIGHT1 / 3.28084
    HEIGHT2 = HEIGHT2 / 3.28084

    ThePath = SITE1 + " - " + SITE2
    PathInfo = ThePath + DISTANCE + FREQ
    
    Range = "3000"
    Altitude = "300"
    Azimuth = "0"
    Tilt = "45"

    print("Working on " + ThePath)

    #Suppress multiple site names

    FlagS1 = 0
    FlagS2 = 0

    try:
        temp_df = pd.read_csv(TEMPFILE, header=None)

        for index, row in temp_df.iterrows():
            ASITE = row[0]

            if (SITE1 == ASITE): #this site name has been used previously
                FlagS1 = 1
                #SITE1 = ""
                ROW[1]=""
            
            if (SITE2 == ASITE): #this site name has been used previously
                FlagS2 = 1
                #SITE2 = ""
                ROW[4]= ""

    except pd.errors.EmptyDataError:
        pass

    #Path
    printToKml(output,temp,TEMPFILE,ROW,PathColor,FenceColor,PathInfo,ThePath,Altitude,Range,Tilt,Azimuth,PathsOnlyYN,SiteTitleYN, FlagS1, FlagS2,HEIGHT1,HEIGHT2)


output.write("\n</Document>")
output.write("\n</kml>\n")

del primary_df
output.close()

print("\nProgram Completed")
input("\nPress <Enter> key to clear this window")

