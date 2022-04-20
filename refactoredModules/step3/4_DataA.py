import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import os
import pandas as pd
import math
import numpy as np

class Data(object):

    def __init__(self):
        self.ExampleS3FolderPath = ""
        self.RadioFolderPath = ""
        self.AntennaFolderPath = ""

    def setFolderPath(self, folderPath):
        self.ExampleS3FolderPath = folderPath

    def setRadioPath(self, radioPath):
        self.RadioFolderPath = radioPath

    def setAntennaPath(self, antennaPath):
        self.AntennaFolderPath = antennaPath

    def retrieveAntennaData(self, AntennaToMatch, Freq, FilePath): # 3000 'Retrieve the antenna data
        
        antenna_df = pd.read_csv(FilePath)

        MatchFlag = 0

        for index, row in antenna_df.iterrows():

            AntennaNumber = row[0]
            AnAntenna = row[2]
            FreqLo = row[5]
            FreqMid =row[6]
            FreqHi = row[7]
            GainLo = row[8]
            GainMid =row[9]
            GainHi = row[10]

            print("Looking at antenna " + str(AnAntenna))

            if AntennaToMatch == AntennaNumber:
                MatchFlag = 1

                # 'check frequency range
                FreqCheckFlag = 0
                if float(Freq) < float(FreqLo):
                    FreqCheckFlag = 1
                if float(Freq) > float(FreqHi):
                    FreqCheckFlag = 1
                
                if FreqCheckFlag == 1:
                    print("The matched antenna frequency range <" + str(FreqLo) + "> to <" + str(FreqHi) + "> is outside the proposed operating frequency <" + str(Freq) + "> MHz.")
                    print("The program is terminated.")
                    return False

                # 'determine antenna gain at the operating frequency
                Difference = abs(float(Freq) - float(FreqLo))
                ReferenceGain = float(GainLo)
                ReferenceFreq = float(FreqLo)

                AnotherDiff = abs(float(Freq) - float(FreqMid))
                if AnotherDiff < Difference:
                    Difference = AnotherDiff
                    ReferenceGain = float(GainMid)
                    ReferenceFreq = float(FreqMid)

                AnotherDiff = abs(float(Freq) - float(FreqHi))
                if AnotherDiff < Difference:
                    Difference = AnotherDiff
                    ReferenceGain = float(GainHi)
                    ReferenceFreq = float(FreqHi)

                # 'determine antenna gain at operating frequency

                AntennaGain = ReferenceGain + (20 * math.log(Freq / ReferenceFreq) / math.log(10))
                AntennaModel = AnAntenna

                return AntennaGain, AntennaModel

        if MatchFlag == 0:
            print("Antenna number <" + str(AntennaToMatch) + "> was not matched.")
            print("Program is terminated.")
            return False


    # 4000 'Retrieve waveguide or cable attenuation
    def retrieveWaveguideCableAttenuation(self, Freq, TransLine, FilePath, LineLength):
        WordLength = len(str(TransLine))

        waveguide_df = pd.read_csv(FilePath)
        MatchFlag = 0

        # 'read the line in the list of cables
        for index, row in waveguide_df.iterrows():
            Item = row.tolist()
            NamePiece = str(Item[1])[:WordLength] # changed from Item[2] due to zero based index in python list

            if TransLine == NamePiece:
                MatchFlag = 1
                Diff = 99999.
                RefAttn = 0.0

                for I in range(6, 99, 2): # changed from range(7,99,2) due to zero based index in python list
                    TestFreq = float(Item[I])
                    TestDiff = abs(Freq - TestFreq)

                    if TestDiff < Diff:
                        Diff = TestDiff
                        RefFreq = TestFreq
                        RefAttn = float(Item[I+1])

                        FreqMinus = float(Item[I - 2])
                        AttenMinus = float(Item[I - 1])
                        DiffMinus = abs(Freq - FreqMinus)

                        FreqPlus = float(Item[I + 2])
                        AttenPlus = float(Item[I + 3])
                        DiffPlus = abs(Freq - FreqPlus)

                OtherFreq = FreqPlus
                OtherAttn = AttenPlus
                if DiffMinus <= DiffPlus or math.isnan(DiffPlus): # added or to catch when there are no greater freq available (diffplus == nan)
                    OtherFreq = FreqMinus
                    OtherAttn = AttenMinus

                CA = OtherFreq - RefFreq
                CB = Freq - RefFreq
                CC = OtherAttn - RefAttn
                NewAttn = RefAttn + ((CC / CA) * CB)

                # 'Convert attenuation from meters to feet and calculate transmission line attenuation.

                LineAttn = NewAttn * (0.3048 / 100) * float(LineLength)

                if MatchFlag == 0:
                    print("Transmission Line <" + str(TransLine) + "> was not matched.")
                    print("Program is terminated.")
                    return False

                return LineAttn


    # 5000 'calculate free space loss and atmospheric attenuation
    def calculateFreeSpaceLossAtmosphericAttenuation(self, PathIndex, Freq, FilePath):
        path_params_df = pd.read_csv(FilePath)

        MatchFlag = 0
        
        for index, row in path_params_df.iterrows(): 
            PathNumber = row[0]
            PathDistance = row[1]
            TempF = row[4]
            dN1 = row[5]
            Sa = row[6]
            RelativeHumidity = row[8]
            HL = row[9]

            if PathNumber == PathIndex:
                MatchFlag = 1

                GFreq = Freq / 1000 # '= radio frequency in GHz
                Distance = float(PathDistance) # '= path distance in miles

                # 'calculate free space loss (FreeSpaceLoss#)

                FreeSpaceLoss = 96.58 + (20 * math.log(GFreq) / math.log(10)) + (20 * math.log(Distance) / math.log(10))

                # 'calculate atmospheric loss (PathAttnAir#)

                T = float(TempF) # '= annual temperature (deg F)
                TempC = (T - 32) * (5 / 9)  # 'degrees C
                Dtemp = (7.5 * TempC / (TempC + 273))
                # 'Es# = saturated vapor pressure (hectopascals [hPa] or millibars [mbar]) at air temperature TempC#
                Es = 6.11 * math.pow(10, Dtemp)

                Hr = float(RelativeHumidity) # '= relative humidity (per cent)
                # 'Rho# = water-vapor density (g/m3)
                Rho = 217 * Es * Hr / (100 * (273 + TempC))

                Pres = 1013  # 'mean pressure (hectopascals [hPa] or millibars [mbar])
                Rp = Pres / 1013
                Rt = 288 / (273 + TempC)

                # 'For dry air, the attenuation AttnDryAir# (dB/km) is given by the following equations:

                X11 = math.pow(Rp, 0.0717) * math.pow(Rt, -1.8132)
                X12 = math.pow(math.e, ((0.0156) * (1 - Rp)) + ((-1.6515) * (1 - Rt)))
                Xi1 = X11 * X12

                X21 = math.pow(Rp, 0.5146) * math.pow(Rt, -4.6368)
                X22 = math.pow(math.e, ((-0.1921 * (1 - Rp)) + ((-5.7416) * (1 - Rt))))
                Xi2 = X21 * X22

                X31 = math.pow(Rp, 0.3414) * math.pow(Rt, -6.5851)
                X32 = math.pow(math.e, ((0.213 * (1 - Rp)) + ((-8.5854) * (1 - Rt))))
                Xi3 = X31 * X32

                X41 = math.pow(Rp, 0.0112) * math.pow(Rt, 0.0092)
                X42 = math.pow(math.e, ((-0.1033 * (1 - Rp)) + ((-0.0009) * (1 - Rt))))
                Xi4 = X41 * X42

                X51 = math.pow(Rp, 0.2705) * math.pow(Rt, -2.7192)
                X52 = math.pow(math.e, ((-0.3016 * (1 - Rp)) + ((-4.1033) * (1 - Rt))))
                Xi5 = X51 * X52

                X61 = math.pow(Rp, 0.2445) * math.pow(Rt, -5.9191)
                X62 = math.pow(math.e, ((0.0422 * (1 - Rp)) + ((-8.0719) * (1 - Rt))))
                Xi6 = X61 * X62

                X71 = math.pow(Rp, -0.1833) * math.pow(Rt, 6.5589)
                X72 = math.pow(math.e, ((-0.2402 * (1 - Rp)) + ((6.131) * (1 - Rt))))
                Xi7 = X71 * X72

                G541 = math.pow(Rp, 1.8286) * math.pow(Rt, -1.9487)
                G542 = math.pow(math.e, ((0.4051 * (1 - Rp)) + ((-2.8509) * (1 - Rt))))
                Gamma54 = 2.192 * G541 * G542

                G581 = math.pow(Rp, 1.0045) * math.pow(Rt, 3.561)
                G582 = math.pow(math.e, ((0.1588 * (1 - Rp)) + ((1.2834) * (1 - Rt))))
                Gamma58 = 12.59 * G581 * G582

                G601 = math.pow(Rp, 0.9003) * math.pow(Rt, 4.1335)
                G602 = math.pow(math.e, ((0.0427 * (1 - Rp)) + ((1.6088) * (1 - Rt))))
                Gamma60 = 15 * G601 * G602

                G621 = math.pow(Rp, 0.9886) * math.pow(Rt, 3.4176)
                G622 = math.pow(math.e, ((0.1827 * (1 - Rp)) + ((1.3429) * (1 - Rt))))
                Gamma62 = 14.28 * G621 * G622

                G641 = math.pow(Rp, 1.432) * math.pow(Rt, 0.6258)
                G642 = math.pow(math.e, ((0.3177 * (1 - Rp)) + ((-0.5914) * (1 - Rt))))
                Gamma64 = 6.819 * G641 * G642

                G661 = math.pow(Rp, 2.0717) * math.pow(Rt, -4.1404)
                G662 = math.pow(math.e, ((0.491 * (1 - Rp)) + ((-4.8718) * (1 - Rt))))
                Gamma66 = 1.908 * G661 * G662

                Delta1 = math.pow(Rp, 3.211) * math.pow(Rt, -14.94)
                Delta2 = math.pow(math.e, ((1.583 * (1 - Rp)) + ((-16.37) * (1 - Rt))))
                Delta = -0.00306 * Delta1 * Delta2

                # 'For f <= 54 GHz:

                if GFreq <= 54:
                    Ada1 = (7.2 * math.pow(Rt, 2.8)) / (math.pow(GFreq, 2) + (0.34 * math.pow(Rp, 2) * math.pow(Rt, 1.6)))
                    Ada2 = (.62 * Xi3) / (math.pow((54 - GFreq), (1.16 * Xi1)) + (0.83 * Xi2))
                    AttnDryAir = ((math.pow(GFreq, 2) * math.pow(Rp, 2)) / 1000) * (Ada1 + Ada2)

                # 'For 54 GHz < f <= 60 GHz:
            
                if GFreq > 54 and GFreq <= 60:
                    Ada3 = (math.log(Gamma54)) * (GFreq - 58) * (GFreq - 60) / 24
                    Ada4 = (math.log(Gamma58)) * (GFreq - 54) * (GFreq - 60) / 8
                    Ada5 = (math.log(Gamma60)) * (GFreq - 54) * (GFreq - 58) / 12
                    AttnDryAir = math.pow(math.e, (Ada3 - Ada4 + Ada5))

                # 'For 60 GHz < f <= 62 GHz:

                if GFreq > 60 and GFreq <= 62:
                    AttnDryAir = Gamma60 + ((Gamma62 - Gamma60) * (GFreq - 60) / 2)

                # 'For 62 GHz < f <= 66 GHz:

                if GFreq > 62 and GFreq <= 66:
                    Ada6 = (math.log(Gamma62)) * (GFreq - 64) * (GFreq - 66) / 8
                    Ada7 = (math.log(Gamma64)) * (GFreq - 62) * (GFreq - 66) / 4
                    Ada8 = (math.log(Gamma66)) * (GFreq - 62) * (GFreq - 64) / 8
                    AttnDryAir = math.pow(math.e,(Ada6 - Ada7 + Ada8))

                # 'For 66 GHz < f <= 120 GHz:

                if GFreq > 66 and GFreq <= 120:
                    Ada9 = (3.02 * math.pow(Rt, 3.5) / 10000)
                    Ada10A = (0.283 * math.pow(Rt, 3.8))
                    Ada10B = math.pow((GFreq - 118.75), 2) + (2.91 * math.pow(Rp, 2) * math.pow(Rt, 1.6))
                    Ada10 = Ada10A / Ada10B
                    Ada11A = 0.502 * Xi6 * (1 - (0.0163 * Xi7 * (GFreq - 66)))
                    Ada11B = math.pow((GFreq - 66), (1.4346 * Xi4)) + (1.15 * Xi5)
                    Ada11 = Ada11A / Ada11B
                    AttnDryAir = ((math.pow(GFreq, 2) * math.pow(Rp, 2)) / 1000) * (Ada9 + Ada10 + Ada11)

                # 'For 120 GHz < f <= 350 GHz:

                if GFreq > 120 and GFreq <= 350:
                    Ada12A = (3.02 / 10000)
                    Ada12B = 1 + (1.9 * math.pow(GFreq, 1.5) / 100000)
                    Ada12 = Ada12A / Ada12B
                    Ada13A = 0.283 * math.pow(Rt, 0.3)
                    Ada13B = math.pow((GFreq - 118.75), 2) + (2.91 * math.pow(Rp, 2) * math.pow(Rt, 1.6))
                    Ada13 = Ada13A / Ada13B
                    Ada14 = math.pow(GFreq, 2) * math.pow(Rp, 2) * math.pow(Rt, 3.5) / 1000
                    AttnDryAir = Delta + (Ada14 * (Ada12 + Ada13))

                # 'For 350 GHz < f :

                if GFreq > 350:
                    AttnDryAir = 0.03

                # 'For water vapor, the attenuation AttnWetAir#  (dB/km) is given by the following:

                Eta1 = (0.955 * Rp * math.pow(Rt, 0.68)) + (0.006 * Rho)
                Eta2 = (0.735 * Rp * math.pow(Rt, 0.5)) + (0.0353 * math.pow(Rt, 4) * Rho)

                Gfreq22 = 1 + math.pow(((GFreq - 22) / (GFreq + 22)), 2)
                Gfreq557 = 1 + math.pow(((GFreq - 557) / (GFreq + 557)), 2)
                Gfreq752 = 1 + math.pow(((GFreq - 752) / (GFreq + 752)), 2)
                Gfreq1780 = 1 + math.pow(((GFreq - 1780) / (GFreq + 1780)), 2)

                Awe1A = 3.98 * Eta1 * (math.pow(math.e, (2.23 * (1 - Rt)))) * Gfreq22
                Awe1B = math.pow((GFreq - 22.235), 2) + (9.42 * math.pow(Eta1, 2))
                Awe1 = Awe1A / Awe1B

                Awe2A = 11.96 * Eta1 * math.pow(math.e, (0.7 * (1 - Rt)))
                Awe2B = math.pow((GFreq - 183.31), 2) + (11.14 * math.pow(Eta1, 2))
                Awe2 = Awe2A / Awe2B

                Awe3A = 0.081 * Eta1 * math.pow(math.e, (6.44 * (1 - Rt)))
                Awe3B = math.pow((GFreq - 321.226), 2) + (6.29 * math.pow(Eta1, 2))
                Awe3 = Awe3A / Awe3B

                Awe4A = 3.66 * Eta1 * math.pow(math.e, (1.6 * (1 - Rt)))
                Awe4B = math.pow((GFreq - 325.153), 2) + (9.22 * math.pow(Eta1, 2))
                Awe4 = Awe4A / Awe4B

                Awe5A = 25.37 * Eta1 * math.pow(math.e, (1.09 * (1 - Rt)))
                Awe5B = math.pow((GFreq - 380), 2)
                Awe5 = Awe5A / Awe5B

                Awe6A = 17.4 * Eta1 * math.pow(math.e, (1.46 * (1 - Rt)))
                Awe6B = math.pow((GFreq - 448), 2)
                Awe6 = Awe6A / Awe6B

                Awe7A = 844.6 * Eta1 * math.pow(math.e, (0.17 * (1 - Rt))) * Gfreq557
                Awe7B = math.pow((GFreq - 557), 2)
                Awe7 = Awe7A / Awe7B

                Awe8A = 290 * Eta1 * math.pow(math.e, (0.41 * (1 - Rt))) * Gfreq752
                Awe8B = math.pow((GFreq - 752), 2)
                Awe8 = Awe8A / Awe8B

                Awe9A = 83328 * Eta2 * math.pow(math.e, (0.99 * (1 - Rt))) * Gfreq1780
                Awe9B = math.pow((GFreq - 1780), 2)
                Awe9 = Awe9A / Awe9B

                Awe10A = Awe1 + Awe2 + Awe3 + Awe4 + Awe5
                Awe10 = Awe10A + Awe6 + Awe7 + Awe8 + Awe9

                AttnWetAir = Awe10 * math.pow(GFreq, 2) * math.pow(Rt, 2.5) * Rho / 10000

                AttnAir = AttnDryAir + AttnWetAir
                PathAttnAir = AttnAir * (Distance * 1.60934)

                return FreeSpaceLoss, PathAttnAir

        if MatchFlag == 0:
            print("Path number <" + str(PathNumber) + "> was not matched during FS Loss and Atmos Attn calculation.")
            print("Program is terminated.")
            return False


    # 6000 'calculate retative dispersion factor
    def retativeDispersionFactor(self, PathIndex, FilePath1, FilePath2):
        # 'find aveage latitude  -------------------------------

        average_paths_df = pd.read_csv(FilePath1)

        MatchFlag = 0
        for index, row in average_paths_df.iterrows():
            AnIndex = row[0]
            AverageLat = row[1]

            if AnIndex == PathIndex:
                MatchFlag = 1
                AverageLat = float(AverageLat)

        if MatchFlag == 0:
            print("Path number <" + str(PathIndex) + "> was not matched during relative dispersion factor calculation.")
            print("Program is terminated.")
            return False
        
        # 'find other path parameters  -------------------------------
        path_params_df = pd.read_csv(FilePath2)


        MatchFlag = 0
        for index, row in path_params_df.iterrows():
            Item1 = row[0]

            if Item1 == PathIndex:
                MatchFlag = 1
                dN1 = float(row[5])
                Sa = float(row[6])
                HL = float(row[9])

        if MatchFlag == 0:
            print("Path number <" + str(PathIndex) + "> was not matched during relative dispersion factor calculation.")
            print("Program is terminated.")
            return False

    # '---------------------------------------------------------------------

        Q = math.pow((abs(math.cos((math.pi / 180) * 2 * AverageLat))), 0.7)
        Q = 5.6 * math.log(1.1 + Q) / math.log(10)
        if AverageLat > 45:
            Q = 5.6 * math.log(1.1 - Q) / math.log(10)
        LogK = -4.4 - (0.0027 * dN1) - (0.46 * math.log(10 + (Sa * 0.3048)) / math.log(10))

        RelDispFactor = -(2.5 * LogK) + (0.0019 * HL) - Q - 10.61
        if RelDispFactor < 1.0:
            RelDispFactor = 1.0

        return RelDispFactor


    def execute(self):
        FilePath = self.ExampleS3FolderPath + "/Data/PathDataPass1.csv"
        path_data_pass_df_1 = pd.read_csv(FilePath)

        # Get local output file path from pyqt interface
        FilePath = self.ExampleS3FolderPath + "/Data/PathDataPass2.csv"
        path_data_pass_df_2 = open(FilePath, "w+")

        # Get local RadioFilesRev1.csv file path from pyqt interface 
        RadioFilePath = self.RadioFolderPath + "/RadioFilesRev1.csv"

        # Get local AntennaFilesRev1.csv file path from pyqt interface 
        AntennaFilePath = self.AntennaFolderPath + "/AntennaFilesRev1.csv"

        # Get local WaveguideRev1.csv file path from pyqt interface 
        WaveGuideFilePath = self.AntennaFolderPath + "/WaveguideRev1.csv"

        # Get local PathParameters.csv file path from pyqt interface 
        PathParametersFilePath = self.ExampleS3FolderPath + "/PathParameters.csv"

        # Get local AveragePaths.csv file path from pyqt interface 
        AveragePathFilePath = self.ExampleS3FolderPath + "/AveragePaths.csv"

        Item = [None] * 105     # 'find the basic radio, antenna and waveguide parameters

        path_data_pass_df_2.write("Index,Radio Company,Radio Model,Alt Radio Model,Freq (avg),Polarization,Channel BW,Data Rate,Modulation,Threshold,ACM Offset,DFM,TX Pwr,TX Coupling,RX Coupling,Left Antenna Model,Left Antenna Gain,Left SD Antenna,Left SD Antenna Gain,Left SD Spacing (ft),Right Antenna Model,Right Antenna Gain,Right SD Antenna,Right SD Antenna Gain,Right SD Spacing (ft),Left Waveguide,Left WG Length (ft),Left WG Attn,Right Waveguide,Right WG Length (ft),Right WG Attn,Free Space Loss,Atmospheric Atten,Misc Loss,Field Margin,Rel Dispersion,NotchWidth,NotchDepth,LeftAntHeight,RightAntHeight\n")

        headers = list(path_data_pass_df_1.columns)
        for index, row in path_data_pass_df_1.iterrows():
            PathIndex = int(row[0])
            Freq = row[1]
            Radio = row[2]
            TXPower = row[3]
            LeftAntenna = row[4]
            LeftSDAntenna = row[5]
            LeftWaveguide = row[6]
            LeftWGLengthft = row[7]
            RightAntenna = row[8]
            RightSDAntenna = row[9]
            RightWaveguide = row[10]
            RightWGLengthft = row[11]
            MiscLoss = row[12]
            FieldMargin = row[13]

            # 'find radio parameters
            radio_file_df = pd.read_csv(RadioFilePath)
            
            MatchFlag = 0

            for index, row in radio_file_df.iterrows():
                RadioNumber = row[0]
                FreqMin = row[6]
                FreqMax = row[8]
                ARadio = row[4]

                print("Looking at radio " + str(ARadio))

                if Radio == RadioNumber:
                    MatchFlag = 1

                    FreqMatchFlag = 0
                    if float(Freq) < float(FreqMin):
                        FreqMatchFlag = 1
                    if float(Freq) > float(FreqMax):
                        FreqMatchFlag = 1
                    if FreqMatchFlag == 1:
                        print("The matched radio frequency range <" + str(FreqMin) + "> to <" + str(FreqMax) + "> is outside the proposed operating frequency <" + str(Freq) + "> MHz.")
                        print("The program is terminated.")
                        exit(1)
                
                    Company = row[2]
                    RadioModel = row[3]
                    AltRadioModel = row[4]
                    FreqAvg = row[7]
                    ChannelBW = row[9]
                    DataRate = row[10]
                    Modulation = row[11]
                    Threshold = row[12]
                    ACMoffset = row[13]
                    DFM = row[14]
                    TXpwr = None
                    if TXPower == 1: # removed "" from each int
                        TXpwr = row[16]
                    if TXPower == 2:
                        TXpwr = row[17]
                    if TXPower == 3:
                        TXpwr = row[18]
                    if TXPower == 4:
                        TXpwr = row[19]
                    if TXPower == 5:
                        TXpwr = row[20]
                    TXcoupling = row[22]
                    RXcoupling = row[25]

            if MatchFlag == 0:
                print("Radio number <" + str(Radio) + "> was not matched.")
                print("Program is terminated.")
                exit(1)

            PrintFile = str(PathIndex) + "," + str(Company) + "," + str(RadioModel) + "," + str(AltRadioModel) + "," + str(FreqAvg) + ",V," + str(ChannelBW) + "," + str(DataRate) + "," + str(Modulation) + "," + str(Threshold) + "," + str(ACMoffset) + "," + str(DFM) + "," + str(TXpwr) + "," + str(TXcoupling) + "," + str(RXcoupling) + ","
            
            print(PrintFile)
            path_data_pass_df_2.write(PrintFile)

            AntennaToMatch = LeftAntenna
            temp = self.retrieveAntennaData(AntennaToMatch, Freq, AntennaFilePath) # 'find antenna parameters
            if temp:
                AntennaGain, AntennaModel = temp[0], temp[1]
                LeftAntennaGain = AntennaGain
                LeftAntennaModel = AntennaModel

            LeftDiversitySpacing = ""
            if LeftSDAntenna:
                AntennaToMatch = LeftSDAntenna
                temp = self.retrieveAntennaData(AntennaToMatch, Freq, AntennaFilePath)
                if temp:
                    AntennaGain, AntennaModel = temp[0], temp[1]
                    LeftSDAntennaGain = AntennaGain
                    LeftDiversitySpacing = "30"
                    if Freq > 8500:
                        LeftDiversitySpacing = "20"
                    LeftSDAntennaModel = AntennaModel

            AntennaToMatch = RightAntenna
            temp = self.retrieveAntennaData(AntennaToMatch, Freq, AntennaFilePath)
            if temp:
                AntennaGain, AntennaModel = temp[0], temp[1]
                RightAntennaGain = AntennaGain
                RightAntennaModel = AntennaModel

            RightDiversitySpacing = ""
            if not (math.isnan(RightSDAntenna)): # changed from "if RightSDAntenna:" because nan tests true
                AntennaToMatch = RightSDAntenna
                temp = self.retrieveAntennaData(AntennaToMatch, Freq, AntennaFilePath)
                if temp:
                    AntennaGain, AntennaModel = temp[0], temp[1]
                    RightSDAntennaGain = AntennaGain
                    RightDiversitySpacing = "30"
                    if Freq > 8500:
                        RightDiversitySpacing = "20"
                    RightSDAntennaModel = AntennaModel
                
                
                    PrintFile = str(LeftAntennaModel) + "," + str(LeftAntennaGain) + "," + str(LeftSDAntennaModel) + "," + str(LeftSDAntennaGain) + "," + str(LeftDiversitySpacing) + "," + str(RightAntennaModel) + "," + str(RightAntennaGain) + "," + str(RightSDAntennaModel) + "," + str(RightSDAntennaGain) + "," + str(RightDiversitySpacing) + ","
                    print(PrintFile)
                    path_data_pass_df_2.write(PrintFile)
                    
            else: # added to fix output bug 
                PrintFile = str(LeftAntennaModel) + "," + str(LeftAntennaGain) + "," + "" + "," + "" + "," + "" + "," + str(RightAntennaModel) + "," + str(RightAntennaGain) + "," + "" + "," + "" + "," + "" + "," 
                path_data_pass_df_2.write(PrintFile)


            # 'find waveguide or cable loss

            LeftLineAttn = ""
            RightLineAttn = ""

            TransLine = LeftWaveguide
            LineLength = LeftWGLengthft
            if TransLine:
                LineAttn = self.retrieveWaveguideCableAttenuation(Freq, TransLine, WaveGuideFilePath, LineLength)
                if LineAttn:
                    if TransLine:
                        LeftLineAttn = LineAttn

            TransLine = RightWaveguide
            LineLength = RightWGLengthft

            #if not (math.isnan(TransLine)):
            if not (TransLine != TransLine): # string test for nan
            #if TransLine:
                LineAttn = self.retrieveWaveguideCableAttenuation(Freq, TransLine, WaveGuideFilePath, LineLength)
                if LineAttn:
                #if TransLine: -- No reason to test for this again
                    RightLineAttn = LineAttn

                    PrintFile = str(LeftWaveguide) + "," + str(LeftWGLengthft) + "," + str(LeftLineAttn) + "," + str(RightWaveguide) + "," + str(RightWGLengthft) + "," + str(RightLineAttn) + ","
                    print(PrintFile)
                    path_data_pass_df_2.write(PrintFile)
            else:
                PrintFile = "" + "," + "" + "," + "" + "," + "" + "," + "" + "," + "" + ","
                path_data_pass_df_2.write(PrintFile)

            # 'find free space loss and atmospheric attenuation
            temp = self.calculateFreeSpaceLossAtmosphericAttenuation(PathIndex, Freq, PathParametersFilePath)
            if temp:
                FreeSpaceLoss, PathAttnAir = temp[0], temp[1]
                PrintFile = str(FreeSpaceLoss) + "," + str(PathAttnAir) + ","
                print(PrintFile)
                path_data_pass_df_2.write(PrintFile)

            # 'Add Misc Loss and Field Margin
            PrintFile = str(MiscLoss) + "," + str(FieldMargin) + ","
            print(PrintFile)
            path_data_pass_df_2.write(PrintFile)

            # 'calculate relative dispersion factor
            RelDispFactor = self.retativeDispersionFactor(PathIndex, AveragePathFilePath, PathParametersFilePath)
            if RelDispFactor:
                PrintFile = str(RelDispFactor) + ","
                print(PrintFile)
                path_data_pass_df_2.write(PrintFile)

            # 'calculate W (or M) curve width and depth
            WidthMHz = 0.8 * float(ChannelBW)

            DepthDB = -32.1 + (0.88 * float(DFM)) + (8.8 * math.log(WidthMHz) / math.log(10))

            PrintFile = str(WidthMHz) + "," + str(DepthDB) + ",0,0"
            print(PrintFile)
            path_data_pass_df_2.write(PrintFile)
            path_data_pass_df_2.write("\n")
            print("Calculations for path <" + str(PathIndex) + "> completed.")

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

test = Data()
#test.setFolderPath("C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Path Design 11 April 2021/Step 3 Path Availability/ExampleS3")
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS3 Folder")
test.setFolderPath(ExampleS3FolderPath)
#test.setRadioPath("C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Radios") 
ExampleRadioPath = ex.openFolderNameDialog("Find Radio Folder")
test.setRadioPath(ExampleRadioPath)
#test.setAntennaPath("C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Antennas")
ExampleAntennaPath = ex.openFolderNameDialog("Find Antenna Folder")
test.setAntennaPath(ExampleAntennaPath)
test.execute()
input("Press Enter to exit")