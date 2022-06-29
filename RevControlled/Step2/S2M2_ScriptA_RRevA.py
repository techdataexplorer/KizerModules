import math
import numpy
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd




class ScriptA(object):

    def __init__(self):
        # users' inputs
        self.ExampleS2AFolderPath = ""
        self.TerrainFolderPath = ""
        self.TheMainOption = 1
        self.RetainIndex = "Y"

        #
        # Global Variables
        self.NewGlobalFile = [""] * 201 # bug fix
        self.GlobalTerrain = [""] * 201
        self.GlobalLandUse = [None] * 201
        self.UsgsIndex = [None] * 510
        self.UsgsLat = [None] * 27
        self.UsgsLong = [None] * 31
        self.LulcLat = [[None]* 20 for i in range(2)]
        self.LulcLong = [[None]* 20 for i in range(2)]
        self.Usgs = [[None]* 26 for i in range(31)]
        self.Srtm = [[None]* 5 for i in range(15)]
        self.Gtopo30 = [[None]* 2 for i in range(2)]
        self.LandUseFlag = 0
        self.LandUse = "Y"
        self.FeetMeters = "F"
        self.Samples = 50
        self.MaxGlobal = 101
        self.T1 = None
        self.T2 = None
        self.TheOption = 0
        self.Latitude1 = float("inf")
        self.Latitude2 = float("inf")
        self.Longitude1 = float("inf")
        self.Longitude2 = float("inf")


    def setFolderPath(self, folderPath):
        self.ExampleS2AFolderPath = str(folderPath)


    def setTerrainDataPath(self, folderPath):
        self.TerrainFolderPath = str(folderPath)


    def setLULC(self, landUse):
        self.LandUse = str(landUse).upper()


    def setTerrainOption(self, selectedOption):
        self.TheMainOption = int(selectedOption)


    def setRetainIndex(self, retainOption):
        self.RetainIndex = str(retainOption).upper()


    # FIND TOPOGRAPHIC MAPS FOR END POINTS AND MIDPOINTS
    # USE MAP CROSSING METHOD TO FIND TOPOGRAPHIC MAP FOR MIDPOINT
    # Find Maps
    #def Lable1000(self.Latitude1, self.Longitude1, self.TheOption):
    def findMaps(self, LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles):

        Latitude = LATITUDEA
        Longitude = LONGITUDEA # WEST = NEGATIVE IN GLOBAL MAPPER
        FirstFlag = 1
        LatInc, LongInc = None, None
        Lat2 = LATITUDEB
        Long2 = LONGITUDEB

        # GOSUB 1050 AddGlobalFile
        self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)

        if self.TheOption == 4:
            self.Gtopo30[0][0] = self.T1
            self.Gtopo30[0][1] = self.T2
        else:
            if self.LandUseFlag == 0:
                LatInc = 1
                LongInc = 1
                if self.TheOption == 10:     # CANADA CDED 1: 50,000
                    LatInc = .25
                    if Latitude <= 68:      # 40 <= Latitude <= 68
                        LongInc = .5
                    #END if
                    if 68 < Latitude and Latitude <= 80:        # 68 < Latitude <= 80
                        LongInc = 1
                    #END if
                    if 80 < Latitude:       # 80 < Latitude <= 84
                        LongInc = 2
                    #END if
                #END if
                if self.TheOption == 11:         # CANADA CDED 1: 250,000
                    LatInc = 1
                    if Latitude <= 68:      # 40 <= Latitude <= 68
                        LongInc = 2
                    #END if
                    if 68 < Latitude and Latitude <= 80:        # 68 < Latitude <= 80
                        LongInc = 4
                    #END if
                    if 80 < Latitude:       # 80 < Latitude <= 84
                        LongInc = 8
                    #END if
                #END if
            else:  # self.LandUseFlag = 1
                LatInc = 1
                LongInc = 2
            #END if

            if self.Latitude2 < self.Latitude1:
                LatInc = -LatInc

            if self.Longitude2 < self.Longitude1:
                LongInc = -LongInc

            for ACase in range(1, 3):
                if ACase == 1:#  CALCULATE LATITUDE CROSSING
                    Lat2 = self.Latitude1
                    Long2 = int(abs(self.Longitude1) / abs(LongInc)) * abs(LongInc) * numpy.sign(self.Longitude1)
                    if LongInc > 0 and Long2 < self.Longitude1 or LongInc < 0 and Long2 > self.Longitude1:Long2 = Long2 + LongInc
                else:       #  CALCULATE LONGITUDE CROSSING
                    Lat2 = int(abs(self.Latitude1) / abs(LatInc)) * abs(LatInc) * numpy.sign(self.Latitude1)
                    if LatInc > 0 and Lat2 < self.Latitude1 or LatInc < 0 and Lat2 > self.Latitude1:Lat2 = Lat2 + LatInc
                    Long2 = self.Longitude1
                #END if
                EndFlag = 0

                while(EndFlag != 1): #DO
                    if ACase == 1:
                        if LongInc > 0 and Long2 >= self.Longitude2 or LongInc < 0 and Long2 <= self.Longitude2:
                            EndFlag = 1
                        else:
                            Lat2 = (((self.Latitude2 - self.Latitude1) / (self.Longitude2 - self.Longitude1)) * (Long2 - self.Longitude1)) + self.Latitude1
                            Latitude = Lat2
                            Longitude = Long2 + abs(LongInc / 2)
                            #GOSUB 1050 # AddGlobalFile
                            self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                            Longitude = Long2 - abs(LongInc / 2)
                            #GOSUB 1050 # AddGlobalFile
                            self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                            Long2 = Long2 + LongInc
                        #END if
                    else:
                        if LatInc > 0 and Lat2 >= self.Latitude2 or LatInc < 0 and Lat2 <= self.Latitude2:
                            EndFlag = 1
                        else:
                            Long2 = (((self.Longitude2 - self.Longitude1) / (self.Latitude2 - self.Latitude1)) * (Lat2 - self.Latitude1)) + self.Longitude1
                            Latitude = Lat2 + abs(LatInc / 2)
                            Longitude = Long2
                            #GOSUB 1050 # AddGlobalFile
                            self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                            Latitude = Lat2 - abs(LatInc / 2)
                            #GOSUB 1050 # AddGlobalFile
                            self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                            Lat2 = Lat2 + LatInc
                        #END if
                    #END if

        Latitude = LATITUDEB    # self.Latitude2
        Longitude = LONGITUDEB   # self.Longitude2      #  WEST = NEGATIVE IN GLOBAL MAPPER
        FirstFlag = 1
        #GOSUB 1050 AddGlobalFile
        self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)

        if self.TheOption == 4:
            self.Gtopo30[1][0] = self.T1
            self.Gtopo30[1][1] = self.T2
            if self.Gtopo30[0][0] != self.Gtopo30[1][0] and self.Gtopo30[0][1] != self.Gtopo30[1][1]:
                FirstFlag = 2
                #GOSUB 1050 # AddGlobalFile
                self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                FirstFlag = 3
                #GOSUB 1050 # AddGlobalFile
                self.AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
            #END if
        #END if


    # AddGlobalFile
    #def Lable1050(self.LandUseFlag):
    #    if self.LandUseFlag == 0:
    #        if self.TheOption == 4:
    #            if FirstFlag == 1:
    #                GOSUB 1400  # FindGtopo30
    #            if FirstFlag == 2:
    #                self.NewGlobalFile(1) = "Gtopo30\" + Gtopo30$(1, 1) + Gtopo30$(2, 2) + ".tar.gz"
    #            if FirstFlag == 3:
    #                self.NewGlobalFile(1) = "Gtopo30\" + Gtopo30$(2, 1) + Gtopo30$(1, 2) + ".tar.gz"
    #        elif self.TheOption == 5:
    #            GOSUB 1200  # FindNed30m
    #        elif self.TheOption == 6:
    #            self.NewGlobalFile(1) = "USned30m\PuertoRicoVirginIslands30m\PRVI" + "\PR.bil"  # FindPRVI
    #        elif self.TheOption == 7:
    #            GOSUB 1500  # FindWorldSrtm
    #        elif self.TheOption == 8:
    #            GOSUB 1600  # FindUsSrtm
    #        elif self.TheOption == 10 or self.TheOption == 11:
    #            GOSUB 1700  # FindCanada
    #        elif self.TheOption == 12:
    #            GOSUB 2100  # FindNED10m
    #
    #        if self.NewGlobalFile(1) != "":
    #            #FOR T = 1 TO self.MaxGlobal
    #            for T in range(1, self.MaxGlobal):
    #                if self.GlobalTerrain(T) == "":
    #                    GOTO 1060
    #                if self.GlobalTerrain(T) == self.NewGlobalFile(1):
    #                    GOTO 1070

    def AddGlobalFile(self, FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles):
        if self.LandUseFlag == 0:
            if self.TheOption == 4:
                if FirstFlag == 1:
                    self.FindGtopo30(Latitude, Longitude) # returning T1, T2
                elif FirstFlag == 2:
                    self.NewGlobalFile[0] = "Gtopo30\\" + str(self.Gtopo30[0][0]) + str(self.Gtopo30[1][1]) + ".tar.gz"
                elif FirstFlag == 3:
                    self.NewGlobalFile[0] = "Gtopo30\\" + str(self.Gtopo30[1][0]) + str(self.Gtopo30[0][1]) + ".tar.gz"

            elif self.TheOption == 5:
                self.FindNed30m(Latitude, Longitude)

            elif self.TheOption == 6:
                self.NewGlobalFile[0] = "USned30m\\PuertoRicoVirginIslands30m\\PRVI" + "\\PR.bil"  # FindPRVI

            elif self.TheOption == 7:
                self.FindWorldSrtm(Latitude, Longitude)

            elif self.TheOption == 8:
                self.FindUsSrtm(Latitude, Longitude)

            elif self.TheOption == 10 or self.TheOption == 11:
                self.FindCanada(Latitude, Longitude)

            elif self.TheOption == 12:
                self.FindNED10m(Latitude, Longitude)

            if self.NewGlobalFile[0] != "":
                for T in range(self.MaxGlobal):
                    if self.GlobalTerrain[T] == "":
                        self.GlobalTerrain[T] = self.NewGlobalFile[0]
                        NumTerrainFiles = T
                        break
                    if self.GlobalTerrain[T] == self.NewGlobalFile[0]:
                        if NumTerrainFiles > (self.MaxGlobal - 1):
                            print("Number of terrain files meets or exceeds self.MaxGlobal limit")
                            print("Program terminated")
                            exit(0)
                        break

        else:  # self.LandUseFlag = 1
           #FIND USGS LANDUSE (LULC) FILE
            Flag = 0
            if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
                Flag = 1 # ' CONTINENTAL US
            if 50 <= Latitude and Latitude <= 72 and -169 <= Longitude and Longitude <= -129:
                Flag = 0 # ' ALASKA
            if 18 <= Latitude and Latitude <= 23 and -161 <= Longitude and Longitude <= -154:
                Flag = 0 # ' HAWAII
            if Flag == 0:
                print("Site coordinates outside the continental US limits")
                return

            UsgsMax = 510
            UsgsFile = "LandUse"

            df = pd.read_csv(USGSindxFilePath)
            self.UsgsIndex = df.iloc[:,1].tolist()

            # usgs lat is the first column and the usgs lon are the other columns
            df = pd.read_csv(USGS250kFilePath, header=None)

            self.UsgsLat = df.iloc[:,0].tolist()[1:]
            self.UsgsLong = df.iloc[0].tolist()[1:]

            temp_df = df.iloc[1:]
            temp_df = temp_df.drop(df.columns[0], axis=1)
            self.Usgs = temp_df.to_numpy()

            # 'READ USGS LULC INDEX FOR 250k SCALE MAPS
            data = [434,467,434,499,383,504,383,507,431,431,431,496,361,493,361,485,352,495,352,476,469,474,480,486,375,502,375,375,90,90,90,473,90,498,90,479,506,494,503,376,489,488,497,471,468,377,377,377,68,68,68,482,491,500,483,481,505,478,466,492,461,461,508,461,484,487,465,475,477,490,501,472,470,6,6,6,0,0,0,0,124,122,49,48,124,122,48,47,124,122,46,45,124,122,45,44,124,122,44,43,124,122,43,42,124,122,38,37,126,124,44,43,126,124,43,42,122,120,38,37,122,120,37,36,122,120,36,35,114,112,38,37,112,110,40,39,112,110,32,31,106,104,49,48,96,94,35,34,94,92,36,35,108,106,36,35,0,0,0,0]

            Lulc = [[ [0 for col in range(2)] for col in range(2)] for row in range(20)]
            self.LulcLong = [[0 for i in range(2)] for j in range(20)]
            self.LulcLat = [[0 for i in range(2)] for j in range(20)]

            j = 0
            for i in range(20):
                Lulc[i][0][0] = data[j]
                Lulc[i][0][1] = data[j + 1]
                Lulc[i][1][0] = data[j + 2]
                Lulc[i][1][1] = data[j + 3]
                j += 4

            j = 80
            for i in range(20):
                self.LulcLong[i][0] = data[j]
                self.LulcLong[i][1] = data[j + 1]
                self.LulcLat[i][0] = data[j + 2]
                self.LulcLat[i][1] = data[j + 3]
                j += 4

            #  FIND USGS LULC FILE
            self.NewGlobalFile[0] = ""
            self.NewGlobalFile[1] = ""
            Flag = 0
            if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
                Flag = 1
            if Flag == 0:
                return('Site is not in the continental United States')

            if Flag == 1:
                UsgsRow = 26
                UsgsColumn = 31
                I = 0 # SEARCH FOR LATITUDE
                T = int(((1 / (self.UsgsLat[1] - self.UsgsLat[0]) * (Latitude - self.UsgsLat[0]) + 1)))

                if (T < 1):
                    T = 1

                if T > UsgsRow:
                    T = UsgsRow

                while(I != 0 or T == 0 or T == UsgsRow + 1):
                    if self.UsgsLat[T] >= Latitude and Latitude >= self.UsgsLat[T + 1]:
                        I = T
                    else:
                        if Latitude > self.UsgsLat[T]:
                            T = T - 1
                        else:
                            T = T + 1

                J = 0 # SEARCH FOR LONGITUDE
                T = int(((1 / (self.UsgsLong[1] - self.UsgsLong[0]) * (abs(Longitude) - self.UsgsLong[0]) + 1)))

                if (T < 1):
                    T = 1

                if T > (UsgsColumn - 1):
                    T = UsgsColumn - 1

                while J != 0 or T == 0 or T == UsgsColumn:
                    if self.UsgsLong[T] >= abs(Longitude) and abs(Longitude) >= self.UsgsLong[T + 1]:
                        J = T
                    else:
                        if abs(Longitude) > self.UsgsLong[T]:
                            T = T - 1
                        else:
                            T = T + 1

                if I == 0 or J == 0:
                    return
                T1 = self.Usgs[I, J]

            else:
                T1 = 0

            if T1 > 0: # 250k DATA
                T2 = T1
            if T1 < 0: # 100k DATA
                I = abs(T1)
                if Latitude >= (self.LulcLat[I][0] + self.LulcLat[I][1]) / 2:
                    J = 1
                else:
                    J = 2

                if abs(Longitude) >= (self.LulcLong[I][0] + self.LulcLong[I][1]) / 2:
                    K = 1
                else:
                    K = 2

                T2 = Lulc[I][J][K]
            if T1 == 0:
                if 61 <= Latitude and Latitude <= 62 and -147 <= Longitude and Longitude <= -144:
                    T2 = 428 # VALDEZ ALASKA
                else:
                    T2 = 0

            if T2 > 0:
                if T2 == 291 or T2 == 310 or T2 ==  382: # NEWARK, PENSACOLA, and SCRANTON
                    self.NewGlobalFile[0] = "LandUse\\" + self.UsgsIndex[T2] + "\\land_use1.gz"
                    self.NewGlobalFile[1] = "LandUse\\" + self.UsgsIndex[T2] + "\\land_use2.gz"
                else:
                    self.NewGlobalFile[0] = "LandUse\\" + self.UsgsIndex[T2] + "\\land_use.gz"
                    self.NewGlobalFile[1] = ""

            # finishing AddGlobalFile scope
            for T1 in range(1, 3):
                if self.NewGlobalFile != "":
                    for T in range(1, self.MaxGlobal):
                        if self.GlobalLandUse == "":
                            # do 1080
                            self.GlobalLandUse[T] = self.NewGlobalFile[T1]
                            NumLandUseFiles = T
                            break
                        if self.GlobalLandUse == self.NewGlobalFile[T1]:
                            # do 1090
                            if NumLandUseFiles > (self.MaxGlobal - 1):
                                print("Number of LULC files meets or exceeds self.MaxGlobal limit")
                                print("Program terminated")
                                sys.exit()
                            break


    def FindNed30m(self, Latitude, Longitude):
        Flag = 0
        if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
            Flag = 1 # CONTINENTAL US
        if 50 <= Latitude and Latitude <= 72 and -169 <= Longitude and Longitude <= -129:
            Flag = 2 # ALASKA
        if 18 <= Latitude and Latitude <= 23 and -161 <= Longitude and Longitude <= -154:
            Flag = 3 # HAWAII

        if Flag == 0:
            print("Site coordinates outside the limits of CONUS, Hawaii and Alaska")
            return

        if Flag == 2:
            self.LandUse = "N"
        if Flag == 3:
            self.LandUse = "N"

        LatitudeIndex = str(int(abs(Latitude)) + 1)
        LongitudeIndex = str(int(abs(Longitude)) + 1)

        NS, EW = None, None

        if Latitude >= 0:
            NS = "n"
        if Latitude < 0:
            NS = "s"
        if Longitude >= 0:
            EW = "e"
        if Longitude < 0:
            EW = "w"

        if Flag == 1:
            if int(LongitudeIndex) < 100:
                LongitudeIndex = "0" + LongitudeIndex
            if int(LongitudeIndex) < 10:
                LongitudeIndex = "0" + LongitudeIndex
            if int(LatitudeIndex) < 10:
                LatitudeIndex = "0" + LatitudeIndex
            self.NewGlobalFile[0] = "USned30m\\" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "_1\\W001001.adf"

        if Flag == 2:
            self.NewGlobalFile[0] = "USned30m\\Alaska60m\\" + "dem" + LongitudeIndex + LatitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "\\W001001.adf"

        if Flag == 3:
            self.NewGlobalFile[0] = "USned30m\\Hawaii30m\\" + "dem" + LongitudeIndex + LatitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "\\W001001.adf"

    def FindGtopo30(self, Latitude, Longitude):
        if Latitude >= -60:
            if Longitude >= -180 and Longitude <= -140:
                T1 = "w180"
            elif Longitude >= -140 and Longitude <= -100:
                T1 = "w140"
            elif Longitude >= -100 and Longitude <= -60:
                T1 = "w100"
            elif Longitude >= -60 and Longitude <= -20:
                T1 = "w060"
            elif Longitude >= -20 and Longitude <= 20:
                T1 = "w020"
            elif Longitude >= 20 and Longitude <= 60:
                T1 = "e020"
            elif Longitude >= 60 and Longitude <= 100:
                T1 = "e060"
            elif Longitude >= 100 and Longitude <= 140:
                T1 = "e100"
            else:
                T1 = "e140"

            if Latitude >= 40 and Latitude <= 90:
                T2 = "n90"
            elif Latitude >= -10 and Latitude <= 40:
                T2 = "n40"
            else:
                T2 = "s10"

        else:
            if Longitude >= -180 and Longitude <= -120:
                T1 = "w180"
            elif Longitude >= -120 and Longitude <= -60:
                T1 = "w120"
            elif Longitude >= -60 and Longitude <= 0:
                T1 = "w060"
            elif Longitude >= 0 and Longitude <= 60:
                T1 = "e000"
            elif Longitude >= 60 and Longitude <= 120:
                T1 = "e060"
            else:
                T1 = "e120"
            T2 = "s60"

        self.NewGlobalFile[0] = "Gtopo30\\" + str(T1) + str(T2) + ".tar.gz"
        self.NewGlobalFile[1] = ""

    def FindWorldSrtm(self, Latitude, Longitude):
        SrtmMax = 13
        areaNumber = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        minLat = [42,14,-12,-56,42,30,14,-12,-56,42,14,-12,-56]
        maxLat = [60,42,14,-12,60,42,30,14,-12,60,42,14,-12]
        minLong = [-180,-180,-180,-180,-30,-30,-30,-30,-30,82,82,82,82]
        maxLong = [-30,-30,-30,-30,82,82,82,82,82,180,180,180,180]

        data = areaNumber + minLat + maxLat + minLong + maxLong

        k = 0
        for j in range(5):
            for i in range(SrtmMax):
                self.Srtm[i][j] = data[k]
                k += 1

        for T in range(SrtmMax):
            if self.Srtm[T][0] <= Latitude and Latitude <= self.Srtm[T][1] and self.Srtm[T][2] <= Longitude and Longitude <= self.Srtm[T][3]:
                T3 = str(self.Srtm[T][0])
                if float(T3) < 10:
                    T3 = "0" + T3
                T1 = "area" + T3

                T2 = "s"
                T2_num = 1

                if Latitude >= 0:
                    T2 = "n"
                    T2_num = 0

                T = str(int(abs(Latitude) + T2_num))
                T2 = T2 + T
                if Longitude >= 0:
                    T2 = T2 + "e"
                    T2_num = 0
                else:
                    T2 = T2 + "w"
                    T2_num = 1

                T = str(int(abs(Longitude) + T2_num))

                if float(T) < 100:
                    T = "0" + T
                if float(T) < 10:
                    T = "0" + T

                T2 = T2 + T
                self.NewGlobalFile[0] = "WorldSRTM\\" + T1 + "\\" + T2 + ".bil"
                self.NewGlobalFile[1] = ""
                return
        return

    def FindUsSrtm(self, Latitude, Longitude):
        Flag = 0
        if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
            Flag = 1 # CONTINENTAL US
        elif 50 <= Latitude and Latitude <= 72 and -169 <= Longitude and Longitude <= -129:
            Flag = 0 # ALASKA
        elif 18 <= Latitude and Latitude <= 23 and -161 <= Longitude and Longitude <= -154:
            Flag = 3 # HAWAII

        if Flag == 0:
            print("Site coordinates outside the limits of CONUS and Hawaii")
            return

        if Flag == 3:
            self.LandUse = "N"

        SrtmMax = 8

        areaNum = [1,2,3,4,5,6,7,7]
        minLat = [38,38,38,30,27,17,-15,51]
        maxLat = [49,49,49,38,38,48,60,60]
        minLong = [-126,-111,-97,-124,-100,-83,-180,178]
        maxLong = [-111,-97,-83,-100,-83,-64,-130,179]

        data = areaNum + minLat + maxLat + minLong + maxLong

        k = 0
        for j in range(5):
            for i in range(SrtmMax):
                self.Srtm[i][j] = data[k]
                k += 1

        for T in range(SrtmMax):
            if self.Srtm[T][0] <= Latitude and Latitude <= self.Srtm[T][1] and self.Srtm[T][2] <= Longitude and Longitude <= self.Srtm[T][3]:
                T1 = "area0" + str(self.Srtm[T][0])

                T2 = "s"
                T2_num = 1

                if Latitude >= 0:
                    T2 = "n"
                    T2_num = 0

                T = str(int(abs(Latitude) + T2_num))
                T2 = T2 + T
                if Longitude >= 0:
                    T2 = T2 + "e"
                    T2_num = 0
                else:
                    T2 = T2 + "w"
                    T2_num = 1

                T = str(int(abs(Longitude) + T2_num))

                if float(T) < 100:
                    T = "0" + T
                if float(T) < 10:
                    T = "0" + T

                T2 = T2 + T
                self.NewGlobalFile[0] = "USSRTM\\" + T1 + "\\" + T2 + ".bil"
                self.NewGlobalFile[1] = ""
                return


    def FindCanada(self, Latitude, Longitude):
        Flag = 0
        if 40 <= Latitude and Latitude <= 84 and -144 <= Longitude and Longitude <= -48:
            Flag = 1
        if Flag == 0:
            print("Site coordinates outside the limits of Canada")
            return

        if abs(Latitude) > 80:
            if abs(Longitude) >= 88:
                T1 = "560"
            elif abs(Longitude) < 72:
                T1 = "120"
            else:
                T1 = "340"
        else:
            T1 = int((1.25 * abs(Longitude) - 60) / 10) * 10
            T2 = int(.25 * abs(Latitude) - 10)
            T1 = T1 + T2
            if int(T1) < 10:
                T1 = "00" + str(T1)
            if 9 < T1 and T1 < 100:
                T1 = "0" + str(T1)

        if Latitude <= 68:
            # 40 <= Latitude <= 68
            T1 = int(((int(abs(Longitude) - 48)) % 8) / 2) + 1
            T2 = int(((int(abs(Latitude) - 40)) % 4)) + 1
            T = "abcdhgfeijklponm"
            StartValue = (4 * (T2 - 1) + T1)
            T2 = T[StartValue - 1 : StartValue]

        elif 68 < Latitude and Latitude <= 80:
            # 68 < Latitude <= 80
            T1 = int(((int(abs(Longitude) - 48)) % 8) / 4) + 1
            T2 = int(((int(abs(Latitude) - 40)) % 4)) + 1
            T = "abdcefhg"
            StartValue = (2 * (T2 - 1) + T1)
            T2 = T[StartValue - 1 : StartValue]

        elif 80 < Latitude:
            # 80 < Latitude <= 84
            T1 = int(((int(abs(Longitude) - 56)) % 16) / 8) + 1
            T2 = int(((int(abs(Latitude) - 40)) % 4)) + 1
            T = "abdcefhg"
            StartValue = (2 * (T2 - 1) + T1)
            T2 = T[StartValue - 1 : StartValue]

        if self.TheOption == 10: # changed from option
            # 1:50k data
            # #T1 goes right to left across the grid from 1 to 4
            # #T2 goes bottom to top up the grid from 1 to 4
            if Latitude <= 68:
                #40 <= Latitude <= 68
                LONGA = abs(Longitude)
                LONGI = int(LONGA)
                LONGIREM = LONGI % 2
                LONGDELTA = (LONGA - LONGI) + LONGIREM  # 0 to 2
                T1 = int((2 * LONGDELTA) + 1) # 1 to 5
                if T1 == 0:
                    T1 = 1
                if T1 == 5:
                    T1 = 4
                LATI = int(Latitude)
                LATDELTA = Latitude - LATI  # 0 to 1
                T2 = int((4 * LATDELTA) + 1)# 1 to 5
                if T2 == 0:
                    T1 = 1
                if T2 == 5:
                    T1 = 4

            if 68 < Latitude and Latitude <= 80:
                #68 < Latitude <= 80
                LONGA = abs(Longitude)
                LONGI = int(LONGA)
                LONGIREM = LONGI % 4
                LONGDELTA = (LONGA - LONGI) + LONGIREM  # 0 to 4
                T1 = int(LONGDELTA + 1)  #1 to 5
                if T1 == 0:
                    T1 = 1
                if T1 == 5:
                    T1 = 4
                LATI = int(Latitude)
                LATDELTA = Latitude - LATI  # 0 to 1
                T2 = int((4 * LATDELTA) + 1)#1 to 5
                if T2 == 0:
                    T1 = 1
                if T2 == 5:
                    T1 = 4

            if 80 < Latitude:
            # 80 < Latitude <= 84
                LONGA = abs(Longitude)
                LONGI = int(LONGA)
                LONGIREM = LONGI % 8
                LONGDELTA = (LONGA - LONGI) + LONGIREM  # 0 to 8
                T1 = int((LONGDELTA / 2) + 1)  #1 to 5
                if T1 == 0:
                    T1 = 1
                if T1 == 5:
                    T1 = 4
                LATI = int(Latitude)
                LATDELTA = Latitude - LATI  # 0 to 1
                T2 = int((4 * LATDELTA) + 1) #1 to 5
                if T2 == 0:
                    T1 = 1
                if T2 == 5:
                    T1 = 4

            T = "01020304080706050910111216151413"
            StartValue = (8 * (T2 - 1) + (2 * T1) - 1)
            T3 = T[StartValue - 1 : StartValue + 1]
            self.NewGlobalFile[0] = "Canada\\50kdem\\" + str(T1) + "\\" + str(T1) + str(T2) + str(T3) + ".zip"

        else:
            #1:250k data, option=11
            self.NewGlobalFile[0] = "Canada\\250kdem\\" + str(T1) + "\\" + str(T1) + str(T2) + ".zip"

        return

    def FindNED10m(self, Latitude, Longitude):
        Flag = 0
        if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
            Flag = 1 # ' CONTINENTAL US
        if 18 <= Latitude and Latitude <= 23 and -161 <= Longitude and Longitude <= -154:
            Flag = 2 # ' HAWAII

        if Flag == 0:
            print("Site coordinates outside the limits of CONUS and Hawaii")
            return

        if Flag == 2:
            self.LandUse = "N"

        NS, EW = None, None

        LatitudeIndex = str(int(abs(Latitude)) + 1)
        LongitudeIndex = str(int(abs(Longitude)) + 1)
        if int(LongitudeIndex) < 100:
            LongitudeIndex = "0" + str(LongitudeIndex)
        if int(LongitudeIndex) < 10:
            LongitudeIndex = "0" + str(LongitudeIndex)
        if int(LatitudeIndex) < 10:
            LatitudeIndex = "0" + str(LatitudeIndex)
        if Latitude >= 0:
            NS = "n"
        if Latitude < 0:
            NS = "s"
        if Longitude >= 0:
            EW = "e"
        if Longitude < 0:
            EW = "w"

        if Flag == 1:
            self.NewGlobalFile[0] = "USned10m\\" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "_13\\W001001.adf"

        if Flag == 2:
            self.NewGlobalFile[0] = "USned10m\\Hawaii\\" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
            self.NewGlobalFile[0] = self.NewGlobalFile[0] + "_13\\W001001.adf"

        if Flag == 1:
            NEWFLAG = 1
            if LatitudeIndex == 50 and LongitudeIndex > 96:
                NEWFLAG = 0
            elif LatitudeIndex == 50 and LongitudeIndex < 95:
                NEWFLAG = 0
            elif LatitudeIndex == 49 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 49 and LongitudeIndex < 89:
                NEWFLAG = 0
            elif LatitudeIndex == 48 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 48 and LongitudeIndex < 68:
                NEWFLAG = 0
            elif LatitudeIndex == 48 and LongitudeIndex < 87 and LongitudeIndex > 70:
                NEWFLAG = 0
            elif LatitudeIndex == 47 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 47 and LongitudeIndex < 68:
                NEWFLAG = 0
            elif LatitudeIndex == 47 and LongitudeIndex < 84 and LongitudeIndex > 71:
                NEWFLAG = 0
            elif LatitudeIndex == 46 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 46 and LongitudeIndex < 72:
                NEWFLAG = 0
            elif LatitudeIndex == 46 and LongitudeIndex < 84 and LongitudeIndex > 75:
                NEWFLAG = 0
            elif LatitudeIndex == 45 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 45 and LongitudeIndex < 67:
                NEWFLAG = 0
            elif LatitudeIndex == 45 and LongitudeIndex < 83 and LongitudeIndex > 77:
                NEWFLAG = 0
            elif LatitudeIndex == 44 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 44 and LongitudeIndex < 69:
                NEWFLAG = 0
            elif LatitudeIndex == 44 and LongitudeIndex < 83 and LongitudeIndex > 81:
                NEWFLAG = 0
            elif LatitudeIndex == 43 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 43 and LongitudeIndex < 71:
                NEWFLAG = 0
            elif LatitudeIndex == 42 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 42 and LongitudeIndex < 70:
                NEWFLAG = 0
            elif LatitudeIndex == 41 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 41 and LongitudeIndex < 73:
                NEWFLAG = 0
            elif LatitudeIndex == 40 and LongitudeIndex > 125:
                NEWFLAG = 0
            elif LatitudeIndex == 40 and LongitudeIndex < 75:
                NEWFLAG = 0
            elif LatitudeIndex == 39 and LongitudeIndex > 124:
                NEWFLAG = 0
            elif LatitudeIndex == 39 and LongitudeIndex < 75:
                NEWFLAG = 0
            elif LatitudeIndex == 38 and LongitudeIndex > 124:
                NEWFLAG = 0
            elif LatitudeIndex == 38 and LongitudeIndex < 76:
                NEWFLAG = 0
            elif LatitudeIndex == 37 and LongitudeIndex > 123:
                NEWFLAG = 0
            elif LatitudeIndex == 37 and LongitudeIndex < 76:
                NEWFLAG = 0
            elif LatitudeIndex == 36 and LongitudeIndex > 122:
                NEWFLAG = 0
            elif LatitudeIndex == 36 and LongitudeIndex < 76:
                NEWFLAG = 0
            elif LatitudeIndex == 35 and LongitudeIndex > 121:
                NEWFLAG = 0
            elif LatitudeIndex == 35 and LongitudeIndex < 76:
                NEWFLAG = 0
            elif LatitudeIndex == 34 and LongitudeIndex > 121:
                NEWFLAG = 0
            elif LatitudeIndex == 34 and LongitudeIndex < 78:
                NEWFLAG = 0
            elif LatitudeIndex == 33 and LongitudeIndex > 119:
                NEWFLAG = 0
            elif LatitudeIndex == 33 and LongitudeIndex < 80:
                NEWFLAG = 0
            elif LatitudeIndex == 32 and LongitudeIndex > 114:
                NEWFLAG = 0
            elif LatitudeIndex == 32 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 31 and LongitudeIndex > 106:
                NEWFLAG = 0
            elif LatitudeIndex == 31 and LongitudeIndex < 82:
                NEWFLAG = 0
            elif LatitudeIndex == 30 and LongitudeIndex > 105:
                NEWFLAG = 0
            elif LatitudeIndex == 30 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 30 and LongitudeIndex < 89 and LongitudeIndex > 86:
                NEWFLAG = 0
            elif LatitudeIndex == 29 and LongitudeIndex > 104:
                NEWFLAG = 0
            elif LatitudeIndex == 29 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 29 and LongitudeIndex < 104 and LongitudeIndex > 101:
                NEWFLAG = 0
            elif LatitudeIndex == 29 and LongitudeIndex < 96 and LongitudeIndex > 90:
                NEWFLAG = 0
            elif LatitudeIndex == 29 and LongitudeIndex < 90 and LongitudeIndex > 83:
                NEWFLAG = 0
            elif LatitudeIndex == 28 and LongitudeIndex > 100:
                NEWFLAG = 0
            elif LatitudeIndex == 28 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 28 and LongitudeIndex < 97 and LongitudeIndex > 83:
                NEWFLAG = 0
            elif LatitudeIndex == 27 and LongitudeIndex > 100:
                NEWFLAG = 0
            elif LatitudeIndex == 27 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 27 and LongitudeIndex < 98 and LongitudeIndex > 83:
                NEWFLAG = 0
            elif LatitudeIndex == 26 and LongitudeIndex > 99:
                NEWFLAG = 0
            elif LatitudeIndex == 26 and LongitudeIndex < 81:
                NEWFLAG = 0
            elif LatitudeIndex == 26 and LongitudeIndex < 98 and LongitudeIndex > 82:
                NEWFLAG = 0
            elif LatitudeIndex == 25 and LongitudeIndex > 83:
                NEWFLAG = 0
            elif LatitudeIndex == 25 and LongitudeIndex < 81:
                NEWFLAG = 0

            if NEWFLAG == 0:
                print("Data is outside CONUS limits")
                return

        if Flag == 2:
            NEWFLAG = 1
            if LatitudeIndex == 23 and LongitudeIndex > 161:
                NEWFLAG = 0
            elif LatitudeIndex == 23 and LongitudeIndex < 160:
                NEWFLAG = 0
            elif LatitudeIndex == 22 and LongitudeIndex > 161:
                NEWFLAG = 0
            elif LatitudeIndex == 22 and LongitudeIndex < 157:
                NEWFLAG = 0
            elif LatitudeIndex == 21 and LongitudeIndex > 158:
                NEWFLAG = 0
            elif LatitudeIndex == 21 and LongitudeIndex < 156:
                NEWFLAG = 0
            elif LatitudeIndex == 20 and LongitudeIndex > 157:
                NEWFLAG = 0
            elif LatitudeIndex == 20 and LongitudeIndex < 155:
                NEWFLAG = 0
            elif LatitudeIndex == 19 and LongitudeIndex > 156:
                NEWFLAG = 0
            elif LatitudeIndex == 19 and LongitudeIndex < 156:
                NEWFLAG = 0
            elif NEWFLAG == 0:
                print("Data is outside HAWAII limits")

        return

    def distance_between_a_and_b(self, LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB):
        # 'CALCULATE DISTANCE BETWEEN SITE A and SITE B
        # 'INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
        # 'OUTPUT: Z# (DISTANCE IN MILES)

        # 'HIGH ACCURACY FORMULA
        Z = math.pow((math.sin((math.pi * (LATITUDEA - LATITUDEB) / 180) / 2)), 2)
        Z = Z + math.cos(math.pi * LATITUDEA / 180) * math.cos(math.pi * LATITUDEB / 180) * math.pow((math.sin((math.pi * (LONGITUDEA - LONGITUDEB) / 180) / 2)), 2)
        Z = math.pow(Z, 0.5)
        X = Z

        ZSHORT = 2 * (180 / math.pi) * math.asin(Z)
        Zkm = 111.1 * ZSHORT #DISTANCE IN KILOMETERS
        Zmiles = 69.06 * ZSHORT #DISTANCE IN MILES

        return Zmiles, Zkm

    def InitSubRoutine(self, ExampleS2AFolderPath):
        CriteriaFilePath = ExampleS2AFolderPath + "/Criteria.ini"
        criteria_df = pd.read_csv(CriteriaFilePath)

        TheDataFile = criteria_df.iloc[0,0]
        TowerHt = criteria_df.iloc[1,0]
        MilesKm = criteria_df.iloc[2,0]
        self.FeetMeters = criteria_df.iloc[3,0]
        BuildingHt = criteria_df.iloc[4,0]
        TreeHt = criteria_df.iloc[5,0]
        OpFreq1 = criteria_df.iloc[7,1]
        MaxDist2 = criteria_df.iloc[8,0]
        OpFreq2 = criteria_df.iloc[8,1]
        MaxDist3 = criteria_df.iloc[9,0]
        OpFreq3 = criteria_df.iloc[9,1]
        MaxDist4 = criteria_df.iloc[10,0]
        OpFreq4 = criteria_df.iloc[10,1]
        FirstFresnelFraction = criteria_df.iloc[11,0]
        SecondFresnelFraction = criteria_df.iloc[12,0]
        SecondKFactor = criteria_df.iloc[13,0]
        DLaneTest = criteria_df.iloc[14,0]
        AddlClearance = criteria_df.iloc[15,0]
        ITURkFactor = criteria_df.iloc[16,0]
        ALUkFactor = criteria_df.iloc[17,0]



    def execute(self):

        # Get ExampleS2A folder path from user's machine
        # ExampleS2AFolderPath = "C:/Users/sixpa/tdx/ExampleStep2BN"

        # Get Terrain folder path from user's machine
        # TerrainFolderPath = "E:/Terrain"

        # Use Terrain folder path to create USGSindx.csv file path
        USGSindxFilePath = self.TerrainFolderPath + "/LandUse/Data/USGSindx.csv"

        # Use Terrain folder path to create USGS250k.csv file path
        USGS250kFilePath = self.TerrainFolderPath + "/LandUse/Data/USGS250k.csv"

        # Use Terrain folder path to create LandUseDir folder path
        LandUseDir = self.TerrainFolderPath

        # TheMainOption = int(input("Input Terrain Database Option (1 to 8): "))
        # TheMainOption = 1

        if self.TheMainOption == 1:
            self.TheOption = 12      # sub 2100
        if self.TheMainOption == 2:
            self.TheOption = 5       # sub 1200
        if self.TheMainOption == 3:
            self.TheOption = 6       # sub -
        if self.TheMainOption == 4:
            self.TheOption = 8       # sub 1600
        if self.TheMainOption == 5:
            self.TheOption = 7       # sub 1500
        if self.TheMainOption == 6:
            self.TheOption = 4       # sub 1400
        if self.TheMainOption == 7:
            self.TheOption = 10      # sub 1700
        if self.TheMainOption == 8:
            self.TheOption = 11      # sub 1700

        if self.TheOption == 12:
            print( "USGS NATIONAL ELEVATION DATABASE FOR THE US (10 METER NED)")
        if self.TheOption == 5:
            print( "USGS NATIONAL ELEVATION DATABASE FOR THE US (30 METER NED)")
        if self.TheOption == 6:
            print( "USGS PUERTO RICO AND THE US VIRGIN ISLANDS (30 METER DEM)")
        if self.TheOption == 8:
            print( "SHUTTLE TERRAIN DATA FOR THE US (30 METER SRTM)")
        if self.TheOption == 7:
            print( "SHUTTLE TERRAIN DATA FOR THE WORLD (90 METER SRTM)")
        if self.TheOption == 4:
            print( "USGS GTOPO30 TERRAIN DATABASE FOR THE WORLD (1 KM GRID)")
        if self.TheOption == 10:
            print( "CANADA CDED 1: 50,000 SCALE TERRAIN DATA FILES (10 - 20 METER)")
        if self.TheOption == 11:
            print( "CANADA CDED 1:250,000 SCALE TERRAIN DATA FILES (30 - 90 METER)")

        print()


        # slef.LandUse = "Y"

        # if this condition is met, do 50, else move on to 60
        # if self.TheOption == 5 or self.TheOption == 8 or self.TheOption == 12:
        #     # do 50
        #     while(True):
        #         print("Want to add land use & land cover (LULC) data to path profile data (Y or N)?")
        #         print("(only applicable for continental United States)")
        #         LandUse = input("Enter Y or y for Yes, N or n for No or nothing to terminate program")
        #         print()
        #         if LandUse == "y":
        #             LandUse = "Y"
        #         if LandUse == "n":
        #             LandUse = "N"
        #         if LandUse == "":
        #             sys.exit()      # GOTO 9999
        #         if LandUse == "Y" or LandUse == "N":
        #             break       # GOTO 60
        #         # Loop back to 50 (GOTO 50)
        #
        # # Label 60
        # print()

        # RetainIndex = "Y"

        # RetainIndex = input("If your input file has an index, do you want to retain it (Y/N)?")
        # if RetainIndex == "y":
        #     RetainIndex == "Y"
        # print()

        print("Reading <Criteria.csv> initialization file.")
        print()

        # 9000 Initialization subroutine, inserted here instead of calling the function
        CriteriaFilePath = self.ExampleS2AFolderPath + "/Criteria.csv"
        criteria_df = pd.read_csv(CriteriaFilePath, header=None)

        TheDataFile = criteria_df.iloc[0,0]
        TowerHt = criteria_df.iloc[1,0]
        MilesKm = criteria_df.iloc[2,0]
        self.FeetMeters = criteria_df.iloc[3,0]
        BuildingHt = criteria_df.iloc[4,0]
        TreeHt = criteria_df.iloc[5,0]
        OpFreq1 = criteria_df.iloc[7,1]
        MaxDist2 = criteria_df.iloc[8,0]
        OpFreq2 = criteria_df.iloc[8,1]
        MaxDist3 = criteria_df.iloc[9,0]
        OpFreq3 = criteria_df.iloc[9,1]
        MaxDist4 = criteria_df.iloc[10,0]
        OpFreq4 = criteria_df.iloc[10,1]
        FirstFresnelFraction = criteria_df.iloc[11,0]
        SecondFresnelFraction = criteria_df.iloc[12,0]
        SecondKFactor = criteria_df.iloc[13,0]
        DLaneTest = criteria_df.iloc[14,0]
        AddlClearance = criteria_df.iloc[15,0]
        ITURkFactor = criteria_df.iloc[16,0]
        ALUkFactor = criteria_df.iloc[17,0]

        if self.FeetMeters == "f":   # defined in 9000?
            self.FeetMeters = "F"
        if self.FeetMeters == "m":
            self.FeetMeters = "M"
        if self.FeetMeters == "":
            sys.exit() # GOTO 9999
        if self.FeetMeters != "F" and self.FeetMeters != "M":
            print("Fourth line of <Criteria.ini> not understood.")
            print("Line should be F or M.")
            print("Program Terminated.")
            sys.exit()

        TowerData = 0
        if TowerHt == "Y" or TowerHt == "y":     # defined in 9000?
            TowerData = 1
        print()

        # Add path index to input file
        TheDataFilePath = self.ExampleS2AFolderPath + "/" + TheDataFile + ".csv" # TheDataFile comes from 9000
        print("Input File: " + TheDataFilePath)
        data_df = pd.read_csv(TheDataFilePath)      # data_df == #10 in the basic module

        TempFilePath = self.ExampleS2AFolderPath + "/TempFile/TempFile.csv"
        temp1_df = open(TempFilePath, "w")          # temp1_df == #11 in the basic module

        # line 113

        headers = list(data_df.columns)

        HEADER1 = headers[0]

        if HEADER1 != "Index":      # if HEADER1 == "Index" then skip 150 and go to 200
            if HEADER1 != "Site1":
                print("File does not match required file format.")
                print("Left most header word is not <Index> or <Site1>.")
                sys.exit()
            else:   # if HEADER1 == "Site1" then execute the code under label 150
                # Label 150

                if TowerData == 0:
                    HEADER2 = headers[1]
                    HEADER3 = headers[2]
                    HEADER4 = headers[3]
                    HEADER5 = headers[4]
                    HEADER6 = headers[5]
                    temp1_df.write("Index" + "," + HEADER1 + "," + HEADER2 + "," + HEADER3 + "," + HEADER4 + "," + HEADER5 + "," + HEADER6)

                if TowerData == 0:
                    HEADER2 = headers[1]
                    HEADER3 = headers[2]
                    HEADER4 = headers[3]
                    HEADER5 = headers[4]
                    HEADER6 = headers[5]
                    HEADER7 = headers[6]
                    HEADER8 = headers[7]
                    temp1_df.write("Index" + "," + HEADER1 + "," + HEADER2 + "," + HEADER3 + "," + HEADER4 + \
                        "," + HEADER5 + "," + HEADER6 + "," + HEADER7 + "," + HEADER8)

                COUNTER = 0
                for index, row in data_df.iterrows():
                    COUNTER += 1
                    if TowerData == 0:
                        PathIndex = COUNTER
                        Site1 = row[0]
                        self.Latitude1 = row[1]
                        self.Longitude1 = row[2]
                        Site2 = row[3]
                        self.Latitude2 = row[4]
                        self.Longitude2 = row[5]

                        temp1_df.write(str(PathIndex) + "," + str(Site1) + "," + str(self.Latitude1) + "," + str(self.Longitude1) + "," + str(Site2) + "," + str(self.Latitude2) + "," + str(self.Longitude2))

                    if TowerData == 1:
                        PathIndex = COUNTER
                        Site1 = row[0]
                        self.Latitude1 = row[1]
                        self.Longitude1 = row[2]
                        Site2 = row[3]
                        self.Latitude2 = row[4]
                        self.Longitude2 = row[5]
                        TwrHt1 = row[6]
                        TwrHt2 = row[7]

                        temp1_df.write(str(PathIndex) + "," + str(Site1) + "," + str(self.Latitude1) + "," + str(self.Longitude1) + "," + str(Site2) + "," + str(self.Latitude2) + "," + str(self.Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2))

                # END LOOP SCOPE

                temp1_df.close()

                #################### LINE 181 ####################

                data_df = open(TheDataFilePath, "w")            # data_df == #10 in the basic module
                temp1_df = pd.read_csv(TempFilePath, header=None)            # temp1_df == #11 in the basic module

                ACOUNTER = 0
                for index, row in temp1_df.iterrows():
                    ACOUNTER += 1

                    if TowerData == 0:
                        PathIndex = row[0]
                        Site1 = row[1]
                        self.Latitude1 = row[2]
                        self.Longitude1 = row[3]
                        Site2 = row[4]
                        self.Latitude2 = row[5]
                        self.Longitude2 = row[6]

                        data_df.write(str(PathIndex) + "," + str(Site1) + "," + str(self.Latitude1) + "," + str(self.Longitude1) + "," + str(Site2) + "," + str(self.Latitude2) + "," + str(self.Longitude2) + "\n")

                    if TowerData == 1:
                        PathIndex = row[0]
                        Site1 = row[1]
                        self.Latitude1 = row[2]
                        self.Longitude1 = row[3]
                        Site2 = row[4]
                        self.Latitude2 = row[5]
                        self.Longitude2 = row[6]
                        TwrHt1 = row[7]
                        TwrHt2 = row[8]

                        data_df.write(str(PathIndex) + "," + str(Site1) + "," + str(self.Latitude1) + "," + str(self.Longitude1) + "," + str(Site2) + "," + str(self.Latitude2) + "," + str(self.Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2) + "\n")

                    data_df.close()

        # label 200
        data_df = pd.read_csv(TheDataFilePath)      # data_df == #10 in the basic module

        headers = list(data_df.columns)

        if TowerData == 0:
            HEADER1 = headers[0]
            HEADER2 = headers[1]
            HEADER3 = headers[2]
            HEADER4 = headers[3]
            HEADER5 = headers[4]
            HEADER6 = headers[5]
            HEADER7 = headers[6]

        if TowerData == 1:
            HEADER1 = headers[0]
            HEADER2 = headers[1]
            HEADER3 = headers[2]
            HEADER4 = headers[3]
            HEADER5 = headers[4]
            HEADER6 = headers[5]
            HEADER7 = headers[6]
            #HEADER8 = headers[7]
            #HEADER9 = headers[8]

        OldNumTerrainFiles = 0
        OldNumLandUseFiles = 0
        NumTerrainFiles = 0
        NumLandUseFiles = 0
        COUNTER = 0

        # Build the Global Mapper Script
        GMScriptFilePath = self.ExampleS2AFolderPath + "/GMscript.gms"
        gm_script = open(GMScriptFilePath, "w")        # gm_script == # 11 in the basic module

        gm_script.write("GLOBAL_MAPPER_SCRIPT VERSION=1.00")
        gm_script.write("UNLOAD_ALL")

        InputFile = self.TerrainFolderPath + "/Misc/GEO_NAD83.prj"

        if self.TheOption == 4 or self.TheOption == 7 or self.TheOption == 8:
            InputFile = self.TerrainFolderPath +  "/Misc/GEO_WGS84.prj"

        gm_script.write("LOAD_PROJECTION FILENAME=" + chr(34) + InputFile + chr(34))

        ProjectionFile = InputFile

        print()

        for index, row in data_df.iterrows():
            COUNTER += 1

            if TowerData == 0:
                PathIndex = row[0]
                Site1 = row[1]
                self.Latitude1 = row[2]
                self.Longitude1 = row[3]
                Site2 = row[4]
                self.Latitude2 = row[5]
                self.Longitude2 = row[6]

            if TowerData == 1:
                PathIndex = row[0]
                Site1 = row[1]
                self.Latitude1 = row[2]
                self.Longitude1 = row[3]
                Site2 = row[4]
                self.Latitude2 = row[5]
                self.Longitude2 = row[6]
                TwrHt1 = row[7]
                TwrHt2 = row[8]

            # Line 246
            Zmiles, Zkm = self.distance_between_a_and_b(self.Latitude1, self.Latitude2, self.Longitude1, self.Longitude2)

            LAT1 = self.Latitude1
            LONG1 = self.Longitude1
            Lat2 = self.Latitude2
            Long2 = self.Longitude2

            print("Processing: " + Site1 + "," + str(LAT1) + "," + str(LONG1) + "," + Site2 + "," + str(Lat2) + "," + str(Long2))

            self.LandUseFlag = 0
            self.NewGlobalFile[0] = ""
            self.NewGlobalFile[1] = ""

        	#GOSUB 1000
            self.findMaps(self.Latitude1, self.Latitude2, self.Longitude1, self.Longitude2, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)


            if COUNTER == 1:
                for i in range(1, self.MaxGlobal):
                    if self.GlobalTerrain[i] != "":
                        DataFile = self.TerrainFolderPath + str(self.GlobalTerrain[i])
                        gm_script.write("IMPORT TYPE=AUTO FILENAME=" + chr(34) + DataFile + chr(34))

                OldNumTerrainFiles = NumTerrainFiles

            if COUNTER > 1 and NumTerrainFiles > OldNumTerrainFiles:
                for T in range(OldNumTerrainFiles + 1, self.MaxGlobal):
                    if self.GlobalTerrain[T] != "":
                        DataFile = self.TerrainFolderPath + self.GlobalTerrain[T]
                        gm_script.write("IMPORT TYPE=AUTO FILENAME=" + chr(34) + DataFile + chr(34))
                OldNumTerrainFiles = NumTerrainFiles


            if self.LandUse == "Y":

                self.LandUseFlag = 1
                self.NewGlobalFile[1] = ""
                self.NewGlobalFile[2] = ""

                #GOSUB 1000
                self.findMaps(self.Latitude1, self.Latitude2, self.Longitude1, self.Longitude2, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles) # added later, verify signature

                if COUNTER == 1:
                    for T in range(1, self.MaxGlobal):
                        if self.GlobalLandUse[T] != "":
                            DataFile = LandUseDir + str(self.GlobalLandUse[T])
                            gm_script.write("IMPORT TYPE=LULC FILENAME=" + chr(34) + DataFile + chr(34))
                    OldNumLandUseFiles = NumLandUseFiles

                if COUNTER > 1 and NumLandUseFiles > OldNumLandUseFiles:
                    for T in range(OldNumLandUseFiles + 1, self.MaxGlobal):
                        if self.GlobalLandUse[T] != "":
                            DataFile = LandUseDir + self.GlobalLandUse[T]
                            gm_script.write("IMPORT TYPE=LULC FILENAME=" + chr(34) + DataFile + chr(34))
                    OldNumLandUseFiles = NumLandUseFiles

            if self.RetainIndex == "Y":        #THEN GOTO 300
                #300
                ProfileNumber = str(PathIndex)
                if PathIndex < 100000:
                    ProfileNumber = "0" + ProfileNumber
                if PathIndex < 10000:
                    ProfileNumber = "0" + ProfileNumber
                if PathIndex < 1000:
                    ProfileNumber = "0" + ProfileNumber
                if PathIndex < 100:
                    ProfileNumber = "0" + ProfileNumber
                if PathIndex < 10:
                    ProfileNumber = "0" + ProfileNumber
            else:
                ProfileNumber = str(COUNTER)
                if COUNTER > 999999:
                    print("Number paths exceeds 999,999.")
                    print("Program terminated.")
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

            # 350
            DataFile = "GENERATE_PATH_PROFILE FILENAME=" + chr(34) + self.ExampleS2AFolderPath + "/TempFile/" + "P" + ProfileNumber + ".csv" + chr(34)
            if self.FeetMeters == "F":
                DataFile = DataFile + " ELEV_UNITS=FEET"
            if self.FeetMeters == "M":
                DataFile = DataFile + " ELEV_UNITS=METERS"

            if self.TheOption == 10 or self.TheOption == 12:
                Samples = (1000 * Zkm) / 10
            if self.TheOption == 5 or self.TheOption == 6 or self.TheOption == 8 or self.TheOption == 11:
                Samples = (1000 * Zkm) / 30
            if self.TheOption == 4 or self.TheOption == 7:
                Samples = (1000 * Zkm) / 90

            Samples = 1 + int(Samples + .5)   # Point Count
            if Samples < 22:
                Samples = 22
            DataFile = DataFile + " POINT_COUNT=" + str(Samples)
            if self.LandUse == "Y":
                DataFile = DataFile + " ADD_LAND_USE_CODES=YES"

            DataFile = DataFile + " START_POS=" + str(self.Longitude1) + "," + str(self.Latitude1) + " END_POS=" + str(self.Longitude2) + "," + str(self.Latitude2)
            gm_script.write(DataFile)

        # Record number of profiles line 356
        # this part is commented out in the original code
        #ProfilesFilePath = ExampleS2AFolderPath + "/Profiles.csv"
        #profiles_df = open(ProfilesFilePath, "w")

        # Print maps
        MapsFilePath = self.ExampleS2AFolderPath + "/Maps.csv"
        maps_df = open(MapsFilePath, "w")   # maps_df == #12 in the basic module

        maps_df.write(ProjectionFile + "\n")

        #print(self.GlobalTerrain[T])
        for T in range(self.MaxGlobal):
            if self.GlobalTerrain[T] != "":
                DataFile = self.TerrainFolderPath + str(self.GlobalTerrain[T])
                maps_df.write(DataFile + "\n")

        print()
        print("Program Completed")
        print()


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

# test class
test = ScriptA()

ExampleStep2FolderPath = ex.openFolderNameDialog("Find ExampleStep2A Folder")
test.setFolderPath(ExampleStep2FolderPath)
TerrainPath = ex.openFolderNameDialog("Find Terrain Folder")
test.setTerrainDataPath(TerrainPath)

print()
print("TERRAIN DATABASE OPTIONS:")
print("   1   USGS NATIONAL ELEVATION DATABASE FOR THE US (10 METER NED)")
print("              [includes Hawaii]")
print("   2   USGS NATIONAL ELEVATION DATABASE FOR THE US (30 METER NED)")
print("              [includes Hawaii (30 meter) and Alasaka (60 meter)]")
print("   3   USGS PUERTO RICO AND THE US VIRGIN ISLANDS (30 METER DEM)")
print("   4   SHUTTLE TERRAIN DATA FOR THE US (30 METER SRTM)")
print("   5   SHUTTLE TERRAIN DATA FOR THE WORLD (90 METER SRTM)")
print("   6   USGS GTOPO30 TERRAIN DATABASE FOR THE WORLD (1 KM GRID)")
print("   7   CANADA CDED 1: 50,000 SCALE TERRAIN DATA FILES (10 - 20 METER)")
print("   8   CANADA CDED 1:250,000 SCALE TERRAIN DATA FILES (30 - 90 METER)")
print()
        
terrOption = input("Enter the Terrain Option (1-8): ")
test.setTerrainOption(terrOption)
LULCOption = input("Enter the Land Use Land Clutter (y or n): ")
test.setLULC(LULCOption)
retainOption = input("Enter the Retain Index (y or n): ")
test.setRetainIndex(retainOption)

test.execute()

input("Hit return to exit program")