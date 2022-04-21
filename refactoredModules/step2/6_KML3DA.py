#
# KML3DA.py
# Kizer Modules API
# Created by Che Blankenship on 07/28/2021
#

import sys
import json
import io
import os
import csv
import math
import requests
import pandas as pd
import urllib.request
from geopy.distance import geodesic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class KML3DA:
    # Directory and file paths
    downloadPath    = ""        # path where user wants to download the kml file
    inputFilePath   = ""        # csv file path (user input)
    output          = ""        # save result
    # Config variables
    dotColor        = "Black"   # default as black
    pathColor       = "Red"     # default as red
    headerYN        = "Yes"     # default as yes
    siteTitleYN     = "Yes"     # default as yes
    pathsOnlyYN     = "No"      # default as no
    # hash set to store site names uniquely
    uniqueSiteList  = set()
    # Site 1 data
    site1Data = {
        "name": None,
        "lat": None,
        "lon": None,
        "height": None
    }
    # Site 2 data
    site2Data = {
        "name": None,
        "lat": None,
        "lon": None,
        "height": None
    }
    # hard coded data
    FREQ        = ""
    DISTANCE    = ""
    RANGE       = "3000"
    ALTITUDE    = "300"
    AZIMUTH     = "0"
    TILT        = "45"

    # Open folder on user's PC and get user's folder location.
    def getDownloadLocation(self, folderPrompt):
        folderName = QFileDialog.getExistingDirectory(self, folderPrompt)
        if folderName:
            return folderName

    # convert path and dot color string to hex
    def convertColorToHex(self, color):
        # [Black, Red, Green, Blue, Yellow, Brown, Orange, LtGreen]
        colors = ['7f000000', '7f0000ff', '7f00ff00', '7fff0000', '7f00ffff', '7f000040', '7f0080ff', '7f00ff80']
        if color == "Black":
            return '<color>'+str(colors[0])+'</color>'
        if color == "Red":
            return '<color>'+str(colors[1])+'</color>'
        if color == "Green":
            return '<color>'+str(colors[2])+'</color>'
        if color == "Blue":
            return '<color>'+str(colors[3])+'</color>'
        if color == "Yellow":
            return '<color>'+str(colors[4])+'</color>'
        if color == "Brown":
            return '<color>'+str(colors[5])+'</color>'
        if color == "Orange":
            return '<color>'+str(colors[6])+'</color>'
        if color == "LtGreen":
            return '<color>'+str(colors[7])+'</color>'
        else:
            return '<color>'+str(colors[0])+'</color>'

    # Get file name from path (i.e: ./dir-path/path1.csv will be "path1")
    def getFileNameFromPath(self, importedFilePath):
        splitedPath = os.path.basename(importedFilePath)
        fileName = splitedPath.split(".")
        return str(fileName[0])

    def checkInputHeader(self, inputCSVRead):
        if self.headerYN == 'Yes':
            return list(inputCSVRead.columns)
        return None

    def writeKMLHeader(self, inputFileName):
        self.output.write("<?xml version=" + chr(34) + "1.0" + chr(34) + " encoding=" + chr(34) + "UTF-8" + chr(34) + "?>")
        self.output.write("\n<kml xmlns=" + chr(34) + "http://www.opengis.net/kml/2.2" + chr(34) + ">")
        self.output.write("\n<Document>")
        self.output.write("\n<name>" + inputFileName + " System Map</name>")
        self.output.write("\n<description>Microwave Paths</description>")
        self.output.write("\n")

    def writeKMLFooter(self, inputCSVRead):
        self.output.write("\n</Document>")
        self.output.write("\n</kml>\n")
        # Delete file
        del inputCSVRead
        self.output.close()
        print("\nProgram Completed")

    # Generate KML file
    def generateKML(self, downloadLocation, inputFilePath, selectedDotColor, selectedPathColor):
        outPutFile  = downloadLocation + "/" + "result.kml"     # kml file to save results
        inputCSVRead = pd.read_csv(inputFilePath)               # read the csv file using pandas lib
        # Open files with python file system
        self.output = open(outPutFile, "w")
        # update path and dot colors
        self.dotColor = self.convertColorToHex(selectedDotColor)
        self.pathColor = self.convertColorToHex(selectedPathColor)
        # check if header exist
        headers = self.checkInputHeader(inputCSVRead)
        ### start creating KML file ###
        inputFileName = self.getFileNameFromPath(inputFilePath)
        # Write the header content
        self.writeKMLHeader(inputFileName)
        # iterate through the input csv file
        for index, row in inputCSVRead.iterrows():
            # site 1
            self.site1Data["name"]      = str(row[1])
            self.site1Data["lat"]       = float(row[2])
            self.site1Data["lon"]       = float(row[3])
            self.site1Data["height"]    = float(row[7])
            # site 2
            self.site2Data["name"]      = str(row[4])
            self.site2Data["lat"]       = float(row[5])
            self.site2Data["lon"]       = float(row[6])
            self.site2Data["height"]    = float(row[8])
            #Convert heights in feet to heights in meters
            self.site1Data["height"]    = self.site1Data["height"] / 3.28084
            self.site2Data["height"]    = self.site2Data["height"] / 3.28084
            # Generate point-to-point path string (e.g: Site 1 - Site 2 )
            thePath = self.site1Data["name"] + " - " + self.site2Data["name"]
            pathInfo = thePath + self.DISTANCE + self.FREQ
            # Suppress multiple site names
            flagS1 = 0
            flagS2 = 0
            try:
                if self.site1Data["name"] in self.uniqueSiteList:
                    flagS1 = 1
                    self.site1Data["name"] = ""
                if self.site2Data["name"] in self.uniqueSiteList:
                    flagS1 = 1
                    self.site2Data["name"] = ""
            except pd.errors.EmptyDataError:
                pass
            self.writeKMLBody(pathInfo, thePath, flagS1, flagS2)
        # write the footer
        self.writeKMLFooter(inputCSVRead)

    # Write the paths data into output KML file.
    def writeKMLPaths(self, pathInfo, thePath):
        self.output.write("\n<Style id=" + chr(34) + "blackLineGreenPoly" + chr(34) + ">")
        self.output.write("\n<LineStyle>\n")
        self.output.write(self.pathColor)
        self.output.write("\n<width>4</width>")
        self.output.write("\n</LineStyle>")
        self.output.write("\n<PolyStyle>\n")
        self.output.write(self.dotColor)
        self.output.write("\n</PolyStyle>")
        self.output.write("\n</Style>")
        self.output.write("\n<Placemark>")
        self.output.write("\n<name>" + pathInfo + "</name>")
        self.output.write("\n<description>Path Between " + thePath + "</description>")
        self.output.write("\n<LookAt>")
        self.output.write("\n<longitude>{}</longitude>".format(self.site1Data["lon"]))
        self.output.write("\n<latitude>{}</latitude>".format(self.site1Data["lat"]))
        self.output.write("\n<altitude>{}</altitude>".format(self.ALTITUDE))
        self.output.write("\n<range>{}</range>".format(self.RANGE))
        self.output.write("\n<tilt>{}</tilt>".format(self.TILT))
        self.output.write("\n<heading>{}</heading>".format(self.AZIMUTH))
        self.output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
        self.output.write("\n</LookAt>")
        self.output.write("\n<styleUrl>#blackLineGreenPoly</styleUrl>")
        self.output.write("\n<LineString>")
        self.output.write("\n<extrude>1</extrude>")
        self.output.write("\n<tessellate>1</tessellate>")
        self.output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
        self.output.write("\n<coordinates>{},{},{}".format(self.site1Data["lon"], self.site1Data["lat"], self.site1Data["height"])) #height in feet
        self.output.write("\n{},{},{}".format(self.site2Data["lon"], self.site2Data["lat"], self.site2Data["height"]))
        self.output.write("\n</coordinates>")
        self.output.write("\n</LineString>")
        self.output.write("\n</Placemark>")
        self.output.write("\n")

    # Write the dots (sites) data into output KML file
    def writeKMLDots(self, pathInfo, thePath):
        self.output.write("\n<Placemark>")
        self.output.write("\n<description>Microwave Site</description>")
        self.output.write("\n<name>{}</name>".format(self.site1Data["name"]))
        if(self.siteTitleYN == "Yes"):
            self.output.write("\n<visibility>1</visibility>")
        if(self.siteTitleYN != "Yes"):
            self.output.write("\n<visibility>0</visibility>")
        self.output.write("\n<Style>")
        self.output.write("\n<IconStyle>")
        self.output.write("\n<color>ff0000ff</color>")
        self.output.write("\n<scale>0.7</scale>")
        self.output.write("\n<Icon>")
        self.output.write("\n<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>")
        self.output.write("\n</Icon>")
        self.output.write("\n</IconStyle>")
        self.output.write("\n<LabelStyle>")
        self.output.write("\n<scale>0.9</scale>")
        self.output.write("\n</LabelStyle>")
        self.output.write("\n</Style>")
        self.output.write("\n<Point>")
        self.output.write("\n<IconAltitude>1</IconAltitude>")
        self.output.write("\n<extrude>1</extrude>")
        self.output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
        self.output.write("\n<coordinates>{},{},0</coordinates>".format(self.site1Data["lon"], self.site1Data["lat"]))
        self.output.write("\n</Point>")
        self.output.write("\n</Placemark>")
        self.output.write("\n<Placemark>")
        self.output.write("\n<description>Microwave Site</description>")
        self.output.write("\n<name>{}</name>".format(self.site2Data["name"]))
        if(self.siteTitleYN=="Yes"):
            self.output.write("\n<visibility>1</visibility>")
        if(self.siteTitleYN!="Yes"):
            self.output.write("\n<visibility>0</visibility>")
        self.output.write("\n<Style>")
        self.output.write("\n<IconStyle>")
        self.output.write("\n<color>ff0000ff</color>")
        self.output.write("\n<scale>0.7</scale>")
        self.output.write("\n<Icon>")
        self.output.write("\n<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>")
        self.output.write("\n</Icon>")
        self.output.write("\n</IconStyle>")
        self.output.write("\n<LabelStyle>")
        self.output.write("\n<scale>0.9</scale>")
        self.output.write("\n</LabelStyle>")
        self.output.write("\n</Style>")
        self.output.write("\n<Point>")
        self.output.write("\n<IconAltitude>1</IconAltitude>")
        self.output.write("\n<extrude>1</extrude>")
        self.output.write("\n<altitudeMode>relativeToGround</altitudeMode>")
        self.output.write("\n<coordinates>{},{},0</coordinates>".format(self.site2Data["lon"], self.site2Data["lat"]))
        self.output.write("\n</Point>")
        self.output.write("\n</Placemark>")
        self.output.write("\n")

    # Write body data into output KML file
    def writeKMLBody(self, pathInfo, thePath, flagS1, flagS2):
        # Write site 1 or site 2 based on the falg statement.
        if (flagS1 == 0):
            self.uniqueSiteList.add(self.site1Data["name"])
        if (flagS2 == 0):
            self.uniqueSiteList.add(self.site2Data["name"])
        # Write path data into KML file
        self.writeKMLPaths(pathInfo, thePath)
        # If it's set to paths only, skip the dot writng process
        if(self.pathsOnlyYN=="Yes"):
            self.writeKMLBody(pathInfo, thePath, flagS1, flagS2)
        # Write the dot data into the KML file
        self.writeKMLDots(pathInfo, thePath)

# ### Test call the modules ###
testkml = KML3DA()
#start_time = time.time()
testkml.generateKML('C:/ExampleStep2BN(Eric)', 'C:/ExampleStep2BN(Eric)/Paths1.CSV', "Blue", "LtGreen")
#print("---New: %s seconds ---" % (time.time() - start_time))
