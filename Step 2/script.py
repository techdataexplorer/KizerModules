import math
import numpy
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

# FIND TOPOGRAPHIC MAPS FOR END POINTS AND MIDPOINTS
# USE MAP CROSSING METHOD TO FIND TOPOGRAPHIC MAP FOR MIDPOINT
# Find Maps
#def Lable1000(Latitude1, Longitude1, TheOption):
def findMaps(LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles):
	
    Latitude = LATITUDEA
    Longitude = LONGITUDEA # WEST = NEGATIVE IN GLOBAL MAPPER
    FirstFlag = 1
    LatInc, LongInc = None, None
    Lat2 = LATITUDEB
    Long2 = LONGITUDEB

    # GOSUB 1050 AddGlobalFile
    AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)

    if TheOption == 4:
        Gtopo30[0][0] = T1
        Gtopo30[0][1] = T2
    else:
        if LandUseFlag == 0:
            LatInc = 1
            LongInc = 1
            if TheOption == 10:     # CANADA CDED 1: 50,000
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
            if TheOption == 11:         # CANADA CDED 1: 250,000
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
        else:  # LandUseFlag = 1
            LatInc = 1
            LongInc = 2
        #END if

        if Latitude2 < Latitude1:
            LatInc = -LatInc

        if Longitude2 < Longitude1:
            LongInc = -LongInc

        for ACase in range(1, 3):
            if ACase == 1:#  CALCULATE LATITUDE CROSSING
                Lat2 = Latitude1
                Long2 = int(abs(Longitude1) / abs(LongInc)) * abs(LongInc) * numpy.sign(Longitude1)
                if LongInc > 0 and Long2 < Longitude1 or LongInc < 0 and Long2 > Longitude1:Long2 = Long2 + LongInc
            else:       #  CALCULATE LONGITUDE CROSSING
                Lat2 = int(abs(Latitude1) / abs(LatInc)) * abs(LatInc) * numpy.sign(Latitude1)
                if LatInc > 0 and Lat2 < Latitude1 or LatInc < 0 and Lat2 > Latitude1:Lat2 = Lat2 + LatInc
                Long2 = Longitude1
            #END if
            EndFlag = 0

            while(EndFlag != 1): #DO
                if ACase == 1:
                    if LongInc > 0 and Long2 >= Longitude2 or LongInc < 0 and Long2 <= Longitude2:
                        EndFlag = 1
                    else:
                        Lat2 = (((Latitude2 - Latitude1) / (Longitude2 - Longitude1)) * (Long2 - Longitude1)) + Latitude1
                        Latitude = Lat2
                        Longitude = Long2 + abs(LongInc / 2)
                        #GOSUB 1050 # AddGlobalFile
                        AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                        Longitude = Long2 - abs(LongInc / 2)
                        #GOSUB 1050 # AddGlobalFile
                        AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                        Long2 = Long2 + LongInc
                    #END if
                else:
                    if LatInc > 0 and Lat2 >= Latitude2 or LatInc < 0 and Lat2 <= Latitude2:
                        EndFlag = 1
                    else:
                        Long2 = (((Longitude2 - Longitude1) / (Latitude2 - Latitude1)) * (Lat2 - Latitude1)) + Longitude1
                        Latitude = Lat2 + abs(LatInc / 2)
                        Longitude = Long2
                        #GOSUB 1050 # AddGlobalFile
                        AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                        Latitude = Lat2 - abs(LatInc / 2)
                        #GOSUB 1050 # AddGlobalFile
                        AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
                        Lat2 = Lat2 + LatInc
                    #END if
                #END if

    Latitude = LATITUDEB    # Latitude2
    Longitude = LONGITUDEB   # Longitude2      #  WEST = NEGATIVE IN GLOBAL MAPPER
    FirstFlag = 1
    #GOSUB 1050 AddGlobalFile
    AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)

    if TheOption == 4:
        Gtopo30[1][0] = T1
        Gtopo30[1][1] = T2
        if Gtopo30[0][0] != Gtopo30[1][0] and Gtopo30[0][1] != Gtopo30[1][1]:
            FirstFlag = 2
            #GOSUB 1050 # AddGlobalFile
            AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
            FirstFlag = 3
            #GOSUB 1050 # AddGlobalFile
            AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)
        #END if
    #END if


# AddGlobalFile
#def Lable1050(LandUseFlag):
#    if LandUseFlag == 0:
#        if TheOption == 4:
#            if FirstFlag == 1:
#                GOSUB 1400  # FindGtopo30
#            if FirstFlag == 2:
#                NewGlobalFile(1) = "Gtopo30\" + Gtopo30$(1, 1) + Gtopo30$(2, 2) + ".tar.gz"
#            if FirstFlag == 3:
#                NewGlobalFile(1) = "Gtopo30\" + Gtopo30$(2, 1) + Gtopo30$(1, 2) + ".tar.gz"
#        elif TheOption == 5:
#            GOSUB 1200  # FindNed30m
#        elif TheOption == 6:
#            NewGlobalFile(1) = "USned30m\PuertoRicoVirginIslands30m\PRVI" + "\PR.bil"  # FindPRVI
#        elif TheOption == 7:
#            GOSUB 1500  # FindWorldSrtm
#        elif TheOption == 8:
#            GOSUB 1600  # FindUsSrtm
#        elif TheOption == 10 or TheOption == 11:
#            GOSUB 1700  # FindCanada
#        elif TheOption == 12:
#            GOSUB 2100  # FindNED10m
#
#        if NewGlobalFile(1) != "":
#            #FOR T = 1 TO MaxGlobal
#            for T in range(1, MaxGlobal):
#                if GlobalTerrain(T) == "":
#                    GOTO 1060
#                if GlobalTerrain(T) == NewGlobalFile(1):
#                    GOTO 1070
            
def AddGlobalFile(FirstFlag, Latitude, Longitude, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles):
    if LandUseFlag == 0:
        if TheOption == 4:
            if FirstFlag == 1:
                FindGtopo30(Latitude, Longitude) # returning T1, T2
            elif FirstFlag == 2:
                NewGlobalFile[0] = "Gtopo30\\" + str(Gtopo30[0][0]) + str(Gtopo30[1][1]) + ".tar.gz"
            elif FirstFlag == 3:
                NewGlobalFile[0] = "Gtopo30\\" + str(Gtopo30[1][0]) + str(Gtopo30[0][1]) + ".tar.gz"
        
        elif TheOption == 5:
            FindNed30m(Latitude, Longitude)

        elif TheOption == 6:
            NewGlobalFile[0] = "USned30m\\PuertoRicoVirginIslands30m\\PRVI" + "\\PR.bil"  # FindPRVI

        elif TheOption == 7:
            FindWorldSrtm(Latitude, Longitude)

        elif TheOption == 8:
            FindUsSrtm(Latitude, Longitude)

        elif TheOption == 10 or TheOption == 11:
            FindCanada(Latitude, Longitude)

        elif TheOption == 12:
            FindNED10m(Latitude, Longitude)
        
        if NewGlobalFile[0] != "":
            for T in range(MaxGlobal):
                if GlobalTerrain[T] == "":
                    GlobalTerrain[T] = NewGlobalFile[0]
                    NumTerrainFiles = T
                    break
                if GlobalTerrain[T] == NewGlobalFile[0]:
                    if NumTerrainFiles > (MaxGlobal - 1):
                        print("Number of terrain files meets or exceeds MaxGlobal limit")
                        print("Program terminated")
                        exit(0)
                    break

    else:  # LandUseFlag = 1
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
        UsgsIndex = df.iloc[:,1].tolist()
        
        # usgs lat is the first column and the usgs lon are the other columns
        df = pd.read_csv(USGS250kFilePath, header=None)

        UsgsLat = df.iloc[:,0].tolist()[1:]
        UsgsLong = df.iloc[0].tolist()[1:]
        
        temp_df = df.iloc[1:]
        temp_df = temp_df.drop(df.columns[0], axis=1)
        Usgs = temp_df.to_numpy()
    
        # 'READ USGS LULC INDEX FOR 250k SCALE MAPS
        data = [434,467,434,499,383,504,383,507,431,431,431,496,361,493,361,485,352,495,352,476,469,474,480,486,375,502,375,375,90,90,90,473,90,498,90,479,506,494,503,376,489,488,497,471,468,377,377,377,68,68,68,482,491,500,483,481,505,478,466,492,461,461,508,461,484,487,465,475,477,490,501,472,470,6,6,6,0,0,0,0,124,122,49,48,124,122,48,47,124,122,46,45,124,122,45,44,124,122,44,43,124,122,43,42,124,122,38,37,126,124,44,43,126,124,43,42,122,120,38,37,122,120,37,36,122,120,36,35,114,112,38,37,112,110,40,39,112,110,32,31,106,104,49,48,96,94,35,34,94,92,36,35,108,106,36,35,0,0,0,0]

        Lulc = [[ [0 for col in range(2)] for col in range(2)] for row in range(20)]
        LulcLong = [[0 for i in range(2)] for j in range(20)]
        LulcLat = [[0 for i in range(2)] for j in range(20)]

        j = 0
        for i in range(20):
            Lulc[i][0][0] = data[j]
            Lulc[i][0][1] = data[j + 1]
            Lulc[i][1][0] = data[j + 2]
            Lulc[i][1][1] = data[j + 3]
            j += 4

        j = 80
        for i in range(20):
            LulcLong[i][0] = data[j]
            LulcLong[i][1] = data[j + 1]
            LulcLat[i][0] = data[j + 2]
            LulcLat[i][1] = data[j + 3]
            j += 4

        #  FIND USGS LULC FILE
        NewGlobalFile[0] = ""
        NewGlobalFile[1] = ""
        Flag = 0
        if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
            Flag = 1
        if Flag == 0:
            return('Site is not in the continental United States')

        if Flag == 1:
            UsgsRow = 26
            UsgsColumn = 31
            I = 0 # SEARCH FOR LATITUDE
            T = int(((1 / (UsgsLat[1] - UsgsLat[0]) * (Latitude - UsgsLat[0]) + 1)))
            
            if (T < 1):
                T = 1
            
            if T > UsgsRow:
                T = UsgsRow

            while(I != 0 or T == 0 or T == UsgsRow + 1):
                if UsgsLat[T] >= Latitude and Latitude >= UsgsLat[T + 1]:
                    I = T
                else:
                    if Latitude > UsgsLat[T]:
                        T = T - 1
                    else:
                        T = T + 1

            J = 0 # SEARCH FOR LONGITUDE
            T = int(((1 / (UsgsLong[1] - UsgsLong[0]) * (abs(Longitude) - UsgsLong[0]) + 1)))
            
            if (T < 1):
                T = 1

            if T > (UsgsColumn - 1):
                T = UsgsColumn - 1
            
            while J != 0 or T == 0 or T == UsgsColumn:
                if UsgsLong[T] >= abs(Longitude) and abs(Longitude) >= UsgsLong[T + 1]:
                    J = T
                else:
                    if abs(Longitude) > UsgsLong[T]:
                        T = T - 1
                    else:
                        T = T + 1
            
            if I == 0 or J == 0:
                return
            T1 = Usgs[I, J]
        
        else:
            T1 = 0

        if T1 > 0: # 250k DATA
            T2 = T1
        if T1 < 0: # 100k DATA
            I = abs(T1)
            if Latitude >= (LulcLat[I][0] + LulcLat[I][1]) / 2:
                J = 1
            else:
                J = 2
        
            if abs(Longitude) >= (LulcLong[I][0] + LulcLong[I][1]) / 2:
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
                NewGlobalFile[0] = "LandUse\\" + UsgsIndex[T2] + "\\land_use1.gz"
                NewGlobalFile[1] = "LandUse\\" + UsgsIndex[T2] + "\\land_use2.gz"
            else:
                NewGlobalFile[0] = "LandUse\\" + UsgsIndex[T2] + "\\land_use.gz"
                NewGlobalFile[1] = ""

        # finishing AddGlobalFile scope
        for T1 in range(1, 3):
            if NewGlobalFile != "":
                for T in range(1, MaxGlobal):
                    if GlobalLandUse == "":
                        # do 1080
                        GlobalLandUse[T] = NewGlobalFile[T1]
                        NumLandUseFiles = T
                        break
                    if GlobalLandUse == NewGlobalFile[T1]:
                        # do 1090
                        if NumLandUseFiles > (MaxGlobal - 1):
                            print("Number of LULC files meets or exceeds MaxGlobal limit")
                            print("Program terminated")
                            sys.exit()
                        break

    
def FindNed30m(Latitude, Longitude):
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
        LandUse = "N"
    if Flag == 3:
        LandUse = "N"

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
        NewGlobalFile[0] = "USned30m\\" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "_1\\W001001.adf"

    if Flag == 2:
        NewGlobalFile[0] = "USned30m\\Alaska60m\\" + "dem" + LongitudeIndex + LatitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "\\W001001.adf"

    if Flag == 3:
        NewGlobalFile[0] = "USned30m\\Hawaii30m\\" + "dem" + LongitudeIndex + LatitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "\\W001001.adf"

def FindGtopo30(Latitude, Longitude):
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
    
    NewGlobalFile[0] = "Gtopo30\\" + str(T1) + str(T2) + ".tar.gz"
    NewGlobalFile[1] = ""

def FindWorldSrtm(Latitude, Longitude):
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
            Srtm[i][j] = data[k]
            k += 1

    for T in range(SrtmMax):
        if Srtm[T][0] <= Latitude and Latitude <= Srtm[T][1] and Srtm[T][2] <= Longitude and Longitude <= Srtm[T][3]:
            T3 = str(Srtm[T][0])
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
            NewGlobalFile[0] = "WorldSRTM\\" + T1 + "\\" + T2 + ".bil"
            NewGlobalFile[1] = ""
            return
    return

def FindUsSrtm(Latitude, Longitude):
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
        LandUse = "N"

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
            Srtm[i][j] = data[k]
            k += 1

    for T in range(SrtmMax):
        if Srtm[T][0] <= Latitude and Latitude <= Srtm[T][1] and Srtm[T][2] <= Longitude and Longitude <= Srtm[T][3]:
            T1 = "area0" + str(Srtm[T][0])
            
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
            NewGlobalFile[0] = "USSRTM\\" + T1 + "\\" + T2 + ".bil"
            NewGlobalFile[1] = ""
            return


def FindCanada(Latitude, Longitude):
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
    
    if TheOption == 10: # changed from option
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
        NewGlobalFile[0] = "Canada\\50kdem\\" + str(T1) + "\\" + str(T1) + str(T2) + str(T3) + ".zip"
    
    else:
        #1:250k data, option=11
        NewGlobalFile[0] = "Canada\\250kdem\\" + str(T1) + "\\" + str(T1) + str(T2) + ".zip"

    return

def FindNED10m(Latitude, Longitude):
    Flag = 0
    if 24 <= Latitude and Latitude <= 50 and -126 <= Longitude and Longitude <= -66:
        Flag = 1 # ' CONTINENTAL US
    if 18 <= Latitude and Latitude <= 23 and -161 <= Longitude and Longitude <= -154:
        Flag = 2 # ' HAWAII

    if Flag == 0:
        print("Site coordinates outside the limits of CONUS and Hawaii")
        return

    if Flag == 2:
        LandUse = "N"

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
        NewGlobalFile[0] = "USned10m\\" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "_13\\W001001.adf"

    if Flag == 2:
        NewGlobalFile[0] = "USned10m\\Hawaii\\" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "\\grd" + NS + LatitudeIndex + EW + LongitudeIndex
        NewGlobalFile[0] = NewGlobalFile[0] + "_13\\W001001.adf"

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

def distance_between_a_and_b(LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB):
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

def InitSubRoutine(ExampleS2AFolderPath):
    CriteriaFilePath = ExampleS2AFolderPath + "/Criteria.ini"
    criteria_df = pd.read_csv(CriteriaFilePath)

    TheDataFile = criteria_df.iloc[0,0]
    TowerHt = criteria_df.iloc[1,0]
    MilesKm = criteria_df.iloc[2,0]
    FeetMeters = criteria_df.iloc[3,0]
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

# Global Variables
NewGlobalFile = [""] * 201 # bug fix
GlobalTerrain = [""] * 201
GlobalLandUse = [None] * 201
UsgsIndex = [None] * 510
UsgsLat = [None] * 27
UsgsLong = [None] * 31
LulcLat = [[None]* 20 for i in range(2)] 
LulcLong = [[None]* 20 for i in range(2)] 
Usgs = [[None]* 26 for i in range(31)] 
Srtm = [[None]* 5 for i in range(15)]
Gtopo30 = [[None]* 2 for i in range(2)] 
LandUseFlag = 0
LandUse = "N"
FeetMeters = "F"
Samples = 50
MaxGlobal = 101
T1, T2 = None, None

# Create PyQT Object
app = QApplication(sys.argv)
ex = App()

# Get ExampleS2A folder path from user's machine
ExampleS2AFolderPath = ex.openFolderNameDialog("Find ExampleS2A Folder")

# Get Terrain folder path from user's machine
TerrainFolderPath = ex.openFolderNameDialog("Find Terrain Folder")

# Use Terrain folder path to create USGSindx.csv file path
USGSindxFilePath = TerrainFolderPath + "/LandUse/Data/USGSindx.csv"

# Use Terrain folder path to create USGS250k.csv file path
USGS250kFilePath = TerrainFolderPath + "/LandUse/Data/USGS250k.csv"

# Use Terrain folder path to create LandUseDir folder path
LandUseDir = TerrainFolderPath

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

TheMainOption = int(input("Input Terrain Database Option (1 to 8): "))

TheOption = 0

if TheMainOption == 1:
    TheOption = 12      # sub 2100
if TheMainOption == 2:
    TheOption = 5       # sub 1200
if TheMainOption == 3:
    TheOption = 6       # sub -
if TheMainOption == 4:
    TheOption = 8       # sub 1600
if TheMainOption == 5:
    TheOption = 7       # sub 1500
if TheMainOption == 6:
    TheOption = 4       # sub 1400
if TheMainOption == 7:
    TheOption = 10      # sub 1700
if TheMainOption == 8:
    TheOption = 11      # sub 1700

if TheOption == 12:
    print( "USGS NATIONAL ELEVATION DATABASE FOR THE US (10 METER NED)")
if TheOption == 5:
    print( "USGS NATIONAL ELEVATION DATABASE FOR THE US (30 METER NED)")
if TheOption == 6:
    print( "USGS PUERTO RICO AND THE US VIRGIN ISLANDS (30 METER DEM)")
if TheOption == 8:
    print( "SHUTTLE TERRAIN DATA FOR THE US (30 METER SRTM)")
if TheOption == 7:
    print( "SHUTTLE TERRAIN DATA FOR THE WORLD (90 METER SRTM)")
if TheOption == 4:
    print( "USGS GTOPO30 TERRAIN DATABASE FOR THE WORLD (1 KM GRID)")
if TheOption == 10:
    print( "CANADA CDED 1: 50,000 SCALE TERRAIN DATA FILES (10 - 20 METER)")
if TheOption == 11:
    print( "CANADA CDED 1:250,000 SCALE TERRAIN DATA FILES (30 - 90 METER)")

print()

if TheOption == 0:
    sys.exit()

LandUse = "N"

# if this condition is met, do 50, else move on to 60
if TheOption == 5 or TheOption == 8 or TheOption == 12:
    # do 50
    while(True):
        print("Want to add land use & land cover (LULC) data to path profile data (Y or N)?")
        print("(only applicable for continental United States)")
        LandUse = input("Enter Y or y for Yes, N or n for No or nothing to terminate program")
        print()
        if LandUse == "y":
            LandUse = "Y"
        if LandUse == "n":
            LandUse = "N"
        if LandUse == "":
            sys.exit()      # GOTO 9999
        if LandUse == "Y" or LandUse == "N":
            break       # GOTO 60
        # Loop back to 50 (GOTO 50)
    
# Label 60
print()
RetainIndex = input("If your input file has an index, do you want to retain it (Y/N)?")
if RetainIndex == "y":
    RetainIndex == "Y"
print()

print("Reading <Criteria.ini> initialization file.")
print()

# 9000 Initialization subroutine, inserted here instead of calling the function
CriteriaFilePath = ExampleS2AFolderPath + "/Criteria.csv"
criteria_df = pd.read_csv(CriteriaFilePath, header=None)

TheDataFile = criteria_df.iloc[0,0]
TowerHt = criteria_df.iloc[1,0]
MilesKm = criteria_df.iloc[2,0]
FeetMeters = criteria_df.iloc[3,0]
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

if FeetMeters == "f":   # defined in 9000?
    FeetMeters = "F"
if FeetMeters == "m":
    FeetMeters = "M"
if FeetMeters == "":
    sys.exit() # GOTO 9999
if FeetMeters != "F" and FeetMeters != "M":
    print("Fourth line of <Criteria.ini> not understood.")
    print("Line should be F or M.")
    print("Program Terminated.")
    sys.exit()

TowerData = 0
if TowerHt == "Y" or TowerHt == "y":     # defined in 9000?
    TowerData = 1
print()

# Add path index to input file
TheDataFilePath = ExampleS2AFolderPath + "/" + TheDataFile + ".csv" # TheDataFile comes from 9000
print("Input File: " + TheDataFilePath)
data_df = pd.read_csv(TheDataFilePath)      # data_df == #10 in the basic module

TempFilePath = ExampleS2AFolderPath + "/TempFile/TempFile.csv"
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
                Latitude1 = row[1] 
                Longitude1 = row[2] 
                Site2 = row[3]
                Latitude2 = row[4]
                Longitude2 = row[5]

                temp1_df.write(str(PathIndex) + "," + str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + "," + str(Longitude2))
                
            if TowerData == 1:
                PathIndex = COUNTER
                Site1 = row[0]
                Latitude1 = row[1] 
                Longitude1 = row[2] 
                Site2 = row[3]
                Latitude2 = row[4]
                Longitude2 = row[5]
                TwrHt1 = row[6]
                TwrHt2 = row[7]

                temp1_df.write(str(PathIndex) + "," + str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2))
            
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
                Latitude1 = row[2] 
                Longitude1 = row[3] 
                Site2 = row[4]
                Latitude2 = row[5]
                Longitude2 = row[6]

                data_df.write(str(PathIndex) + "," + str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + "," + str(Longitude2) + "\n")

            if TowerData == 1:
                PathIndex = row[0]
                Site1 = row[1]
                Latitude1 = row[2] 
                Longitude1 = row[3] 
                Site2 = row[4]
                Latitude2 = row[5]
                Longitude2 = row[6]
                TwrHt1 = row[7]
                TwrHt2 = row[8]

                data_df.write(str(PathIndex) + "," + str(Site1) + "," + str(Latitude1) + "," + str(Longitude1) + "," + str(Site2) + "," + str(Latitude2) + "," + str(Longitude2) + "," + str(TwrHt1) + "," + str(TwrHt2) + "\n")

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
    HEADER8 = headers[7]
    HEADER9 = headers[8]

OldNumTerrainFiles = 0
OldNumLandUseFiles = 0
NumTerrainFiles = 0
NumLandUseFiles = 0
COUNTER = 0

# Build the Global Mapper Script
GMScriptFilePath = ExampleS2AFolderPath + "/GMscript.gms"
gm_script = open(GMScriptFilePath, "w")        # gm_script == # 11 in the basic module

gm_script.write("GLOBAL_MAPPER_SCRIPT VERSION=1.00")
gm_script.write("UNLOAD_ALL")

InputFile = TerrainFolderPath + "/Misc/GEO_NAD83.prj"

if TheOption == 4 or TheOption == 7 or TheOption == 8:
    InputFile = TerrainFolderPath +  "/Misc/GEO_WGS84.prj"

gm_script.write("LOAD_PROJECTION FILENAME=" + chr(34) + InputFile + chr(34))

ProjectionFile = InputFile

print()

for index, row in data_df.iterrows():
    COUNTER += 1 

    if TowerData == 0:
        PathIndex = row[0]
        Site1 = row[1]
        Latitude1 = row[2] 
        Longitude1 = row[3] 
        Site2 = row[4]
        Latitude2 = row[5]
        Longitude2 = row[6]

    if TowerData == 1:
        PathIndex = row[0]
        Site1 = row[1]
        Latitude1 = row[2] 
        Longitude1 = row[3] 
        Site2 = row[4]
        Latitude2 = row[5]
        Longitude2 = row[6]
        TwrHt1 = row[7]
        TwrHt2 = row[8]

    # Line 246
    Zmiles, Zkm = distance_between_a_and_b(Latitude1, Latitude2, Longitude1, Longitude2)

    LAT1 = Latitude1
    LONG1 = Longitude1
    Lat2 = Latitude2
    Long2 = Longitude2

    print("Processing: " + Site1 + "," + str(LAT1) + "," + str(LONG1) + "," + Site2 + "," + str(Lat2) + "," + str(Long2))

    LandUseFlag = 0
    NewGlobalFile[0] = ""
    NewGlobalFile[1] = ""

	#GOSUB 1000
    findMaps(Latitude1, Latitude2, Longitude1, Longitude2, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles)


    if COUNTER == 1:
        for i in range(1, MaxGlobal):       
            if GlobalTerrain[i] != "":
                DataFile = TerrainFolderPath + str(GlobalTerrain[i])   
                gm_script.write("IMPORT TYPE=AUTO FILENAME=" + chr(34) + DataFile + chr(34))

        OldNumTerrainFiles = NumTerrainFiles

    if COUNTER > 1 and NumTerrainFiles > OldNumTerrainFiles:
        for T in range(OldNumTerrainFiles + 1, MaxGlobal):
            if GlobalTerrain[T] != "":
                DataFile = TerrainFolderPath + GlobalTerrain[T]
                gm_script.write("IMPORT TYPE=AUTO FILENAME=" + chr(34) + DataFile + chr(34))
        OldNumTerrainFiles = NumTerrainFiles


    if LandUse == "Y":

        LandUseFlag = 1
        NewGlobalFile[1] = ""
        NewGlobalFile[2] = ""

        #GOSUB 1000
        findMaps(Latitude1, Latitude2, Longitude1, Longitude2, USGSindxFilePath, USGS250kFilePath, NumTerrainFiles) # added later, verify signature

        if COUNTER == 1:
            for T in range(1, MaxGlobal):
                if GlobalLandUse[T] != "":
                    DataFile = LandUseDir + str(GlobalLandUse[T])
                    gm_script.write("IMPORT TYPE=LULC FILENAME=" + chr(34) + DataFile + chr(34))
            OldNumLandUseFiles = NumLandUseFiles

        if COUNTER > 1 and NumLandUseFiles > OldNumLandUseFiles:
            for T in range(OldNumLandUseFiles + 1, MaxGlobal):
                if GlobalLandUse[T] != "":
                    DataFile = LandUseDir + GlobalLandUse[T]
                    gm_script.write("IMPORT TYPE=LULC FILENAME=" + chr(34) + DataFile + chr(34))
            OldNumLandUseFiles = NumLandUseFiles

    if RetainIndex == "Y":        #THEN GOTO 300
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
    DataFile = "GENERATE_PATH_PROFILE FILENAME=" + chr(34) + ExampleS2AFolderPath + "/TempFile/" + "P" + ProfileNumber + ".csv" + chr(34)
    if FeetMeters == "F":
        DataFile = DataFile + " ELEV_UNITS=FEET"
    if FeetMeters == "M":
        DataFile = DataFile + " ELEV_UNITS=METERS"

    if TheOption == 10 or TheOption == 12:
        Samples = (1000 * Zkm) / 10
    if TheOption == 5 or TheOption == 6 or TheOption == 8 or TheOption == 11:
        Samples = (1000 * Zkm) / 30
    if TheOption == 4 or TheOption == 7:
        Samples = (1000 * Zkm) / 90

    Samples = 1 + int(Samples + .5)   # Point Count
    if Samples < 22:
        Samples = 22
    DataFile = DataFile + " POINT_COUNT=" + str(Samples)
    if LandUse == "Y":
        DataFile = DataFile + " ADD_LAND_USE_CODES=YES"
    
    DataFile = DataFile + " START_POS=" + str(Longitude1) + "," + str(Latitude1) + " END_POS=" + str(Longitude2) + "," + str(Latitude2)
    gm_script.write(DataFile)

# Record number of profiles line 356
# this part is commented out in the original code
#ProfilesFilePath = ExampleS2AFolderPath + "/Profiles.csv"
#profiles_df = open(ProfilesFilePath, "w") 

# Print maps
MapsFilePath = ExampleS2AFolderPath + "/Maps.csv"
maps_df = open(MapsFilePath, "w")   # maps_df == #12 in the basic module

maps_df.write(ProjectionFile + "\n")

print(GlobalTerrain[T])
for T in range(MaxGlobal):
    if GlobalTerrain[T] != "": 
        DataFile = TerrainFolderPath + str(GlobalTerrain[T])
        maps_df.write(DataFile + "\n")

print()
print("Program Completed")
print()
input("Press <Enter> key to clear this window")