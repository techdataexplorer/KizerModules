#5/18/21 Updated file paths to pull data from my machine

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd
import math
from pathlib import Path


class Performance(object):

    def __init__(self):
        self.ExampleS3FolderPath = ""

    def setFolderPath(self, folderPath):
        self.ExampleS3FolderPath = folderPath

    # 6500   'subroutine
    def subroutine6500(self, Gfreq, RainProb, A01):
        C0 = 0.12
        if Gfreq >= 10:
            C0 = 0.12 + (0.4 * math.pow((math.log(Gfreq / 10) / math.log(10)), 0.8))
            #see Pathloss notes regarding formula for Gfreq >= 10
            #math.log(N) = natural log of N
            #math.log(N)/math.log(10) = LOG10(N)=log base 10 of N
        C1 = math.pow(0.07,C0) * math.pow(0.12, (1 - C0))
        C2 = (0.855 * C0) + (0.546 * (1 - C0))
        C3 = (0.139 * C0) + (0.043 * (1 - C0))
        Ap = (A01 * C1) / math.pow(RainProb, (C2 + (C3 * math.log(RainProb) / math.log(10))))
        #Ap = path rain attenuation not exceeded RainProb % of time
        return Ap

    def distance_between_a_and_b(self, MilesKm, LATITUDEA, LATITUDEB, LONGITUDEA, LONGITUDEB):
        # 'CALCULATE DISTANCE BETWEEN SITE A and SITE B
        # 'INPUT: LATITUDEA#, LATITUDEB#, LONGITUDEA#, LONGITUDEB#
        # 'OUTPUT: Z# (DISTANCE IN MILES)

        # 'HIGH ACCURACY FORMULA
        Z = math.pow((math.sin((math.pi * (LATITUDEA - LATITUDEB) / 180) / 2)), 2)
        Z = Z + math.cos(math.pi * LATITUDEA / 180) * math.cos(math.pi * LATITUDEB / 180) * math.pow((math.sin((math.pi * (LONGITUDEA - LONGITUDEB) / 180) / 2)), 2)
        Z = math.pow(Z, 0.5)
        X = Z

        ZSHORT = 2 * (180 / math.pi) * math.asin(Z)

        if MilesKm == "M":
            return 69.06 * ZSHORT #DISTANCE IN MILES
        # elif MilesKm == "K": 
        return 111.1 * ZSHORT #DISTANCE IN KILOMETERS

    # 3000 'calculate multipath outage seconds
    # 'results are one way based upon data in feet or mile units
    # '***************************************
    # 'Vigants-Barnett Multipath Model
    def calculateMultipathOutage(self, TempF, ClimateFactor, PathRoughness, Freq, Distance, FadeMargin, DFM, RelDispersion, AntennaGain, SDGain, DivSpacing):
        T = float(TempF)  # 'annual temperature (deg F)

        C = float(ClimateFactor) # 'climate factor

        W = float(PathRoughness) # 'terrain roughness (ft)
        if W < 20:
            W = 20
        if W > 140:
            W = 140

        F = float(Freq) / 1000 # 'frequency (GHz)
        D= float(Distance) # 'path distance (miles)
        FFM = float(FadeMargin) # 'flat fade margin (dB)
        DFM = float(DFM) # 'dispersive fade margin (dB)
        RDF = float(RelDispersion) # 'multiplicative dispersive fading factor
        R = C * math.pow((50 / W), 1.3) * (F / 4) * math.pow(D, 3) / 100000

        # 'R# = Pzero in ITU-R notation
        Pff = R / math.pow(10, (FFM / 10)) # 'probability of non-diversity flat fading outage during heavy fading
        Pdf = R * RDF / math.pow(10, (DFM / 10)) # 'probability of non-diversity dispersive fading outage during heavy fading
        Isdff = 1.0
        Isddf = 1.0

        if SDGain != 0:
            # '------------------------------------------
            # 'Space Diversity results

            P1 = float(AntennaGain) # 'main antenna gain (dBi)

            P2 = float(SDGain) # 'diversity antenna gain (dBi)

            S = float(DivSpacing) # 'diversity antenna spacing (ft)

            P = P2 - P1

            Isdff = (7 / 100000) * math.pow(S, 2) * F * math.pow(10, (P / 10)) * math.pow(10, (FFM / 10)) / D

            if Isdff > 200:
                Isdff = 200

            Isddf = 0.09 * F * math.pow(10, (DFM / 10)) / D

            if Isddf > 200:
                Isddf = 200

        Pff = Pff / Isdff # 'probability of flat fading outage during heavy fading
        Pdf = Pdf / Isddf # 'probability of dispersive fading outage during heavy fading
        Ts = 8000000 * (T / 50) # 'seconds in the annual heavy fading season
        Tsmonth = ((365.25 / 12.0) * 24.0 * 60.0 * 60.0) # 'seconds in a month
        Tsyear = (365.25 * 24.0 * 60.0 * 60.0) # 'seconds in a year

        # 'Worst month (ITU-R) fading
        SecFFmonth = Tsmonth * Pff
        SecDFmonth = Tsmonth * Pdf
        TotalSecMonth = SecFFmonth + SecDFmonth

        # 'Annual (North American) fading
        SecFFyear = Ts * Pff
        SecDFyear = Ts * Pdf
        TotalSecYear = SecFFyear + SecDFyear

        return SecFFyear, SecDFyear, TotalSecYear

    # 5000 'calculate multipath outage seconds using the ITU-R method
    # 'gather basic data
    def calculateMultipathOutageITUR(self, Site1Latitude, Site2Latitude, Distance, dN1, Sa, HL, Gfreq, FadeMargin, LeftAntHt, RightAntHt, AntennaGain, SDGain, DivSpacing, NotchWidth, NotchDepth):
        AvgLat = (float(Site1Latitude) + float(Site2Latitude)) / 2.0
        DistanceKM = 1.609 * float(Distance)
        dN1 = float(dN1)
        if dN1 < -860.0:
            dN1 = -860.
        if dN1 > -150.0:
            dN1 = -150.
        Sa = 0.3048 * float(Sa)
        if Sa < 1.0:
            Sa = 1.
        if Sa > 850.0:
            Sa = 850.
        HL = 0.3048 * float(HL)
        if HL < 17.0:
            HL = 17.
        if HL > 2300.0:
            HL = 2300.
        Gfreq = float(Gfreq)
        FlatFadeMargin = float(FadeMargin)

        Hr = 0.3048 * float(LeftAntHt)  #antenn height at one end of the path (meters)
        He = 0.3048 * float(RightAntHt)  #antenna height at the other end of the path (meters)
        Ep = abs(Hr - He)/DistanceKM  #path inclination (milliradians)
        if Ep > 37.0:
            Ep = 37.0

        #Monthly to Annual propagation outage factor
        if AvgLat <= 45.0:
            DeltaG = 10.5 - (2.6 * math.log(DistanceKM) / math.log(10.0)) + (1.7 * math.log(1.0 + Ep) / math.log(10.0))
            DeltaG = DeltaG - (5.6 * math.log((1.1 + math.pow((abs(math.cos((3.1415926 / 180.0) * 2.0 * AvgLat))),0.7))) / math.log(10.0))

        if AvgLat > 45.0:
            DeltaG = 10.5 - (2.6 * math.log(DistanceKM) / math.log(10.0)) + (1.7 * math.log(1.0 + Ep) / math.log(10.0))
            DeltaG = DeltaG - (5.6 * math.log((1.1 - math.pow((abs(math.cos((3.1415926 / 180.0) * 2.0 * AvgLat))),0.7))) / math.log(10.0))

        if DeltaG > 10.8:
            DeltaG = 10.8

        CMY = 1.0 / math.pow(10.0, (DeltaG / 10.0))

        Tsmonth = ((365.25 / 12.0) * 24.0 * 60.0 * 60.0) #seconds in a month
        Tsyear = (365.25 * 24.0 * 60.0 * 60.0) #seconds in a year

        #Non-diversity Flat fading outage seconds
        Kay = math.pow((10.0 + Sa), 0.46) * math.pow(10.0, 4.4) * math.pow(10.0, (0.0027 * dN1))
        Kay = 1.0 / Kay

        Pzero = math.pow((1.0 + Ep), 1.03) * math.pow(10.0, (0.00076 * HL))
        Pzero = (0.01 * Kay * math.pow(DistanceKM,3.4) * math.pow(Gfreq,0.8)) / Pzero

        Pffm = Pzero / math.pow(10.0,(FlatFadeMargin / 10.0)) #probability of worst month non-diversity flat fading

        #Worst month (ITU-R) flat fading
        SecFFmonth = Tsmonth * Pffm

        #Annual (North American) flat fading
        SecFFyear = Tsyear * Pffm * CMY

        #Non-diversity Dispersive fading outage seconds
        Mu = math.pow(2.7182818,(0.2 * math.pow(Pzero,0.75)))
        Mu = 1.0 - (1.0 / Mu)

        Wa = (float(NotchWidth))/1000.0  #GHz
        Ba = float(NotchDepth)  #dB

        TauR = 6.3
        TauM = 0.7 * math.pow((DistanceKM / 50.0),1.3)

        Pdfm = 4.3 * Mu * Wa * TauM * TauM / (TauR * math.pow(10.0,(Ba / 20.0))) #probability of worst month non-diversity dispersive fading

        #Worst month (ITU-R) dispersive fading
        SecDFmonth = Tsmonth * Pdfm

        #Annual (North American) dispersive fading
        SecDFyear = Tsyear * Pdfm * CMY

        #Combined flat and dispersive fading
        #Worst month (ITU-R) fading
        TotalSecMonth = SecFFmonth + SecDFmonth

        #Annual (North American) fading
        TotalSecYear = SecFFyear + SecDFyear

        if SDGain != 0:
            #------------------------------------------
            #Space Diversity results
            #Flat Fading Improvement
            SpacingM = 0.3048 * float(DivSpacing) #antenna spacing in meters
            if SpacingM < 3.0:
                SpacingM = 3.0
            if SpacingM > 23:
                SpacingM = 23.

            K2ns = 0.0004 * math.pow(SpacingM,0.87) * math.pow(DistanceKM,0.48) / (math.pow(Gfreq,0.12) * math.pow(Pzero,0.04) * Mu)
            K2ns = 1.0 / math.pow(2.7182818,K2ns)

            GainDiff = abs(float(AntennaGain) - float(SDGain))

            Ins = (100 * Mu / Pzero) * (1.0 - (K2ns * (1.0 - (Pzero / (100 * Mu * math.pow(10.0,(FlatFadeMargin / 10))))))) * math.pow(10.0,(FlatFadeMargin / 10)) / math.pow(10.0,(GainDiff / 10.0))

            Pdffm = Pffm / Ins #probability of worst month space diversity flat fading

            #Worst month (ITU-R) flat fading
            SecFFmonth = Tsmonth * Pdffm

            #Annual (North American) flat fading
            SecFFyear = Tsyear * Pdffm * CMY

            #Dispersive Fading Improvement
            if K2ns <= 0.26:
                Rw = 1.0 - (0.9746 * math.pow((1.0 - K2ns),2.170))
            # if K2ns > 0.26:
            else:
                Rw = 1.0 - (0.6921 * math.pow((1.0 - K2ns),1.034))

            K2s = 1.0 - (0.195 * math.pow((1.0 - Rw),(0.109 - (0.13 * math.log(1.0 - Rw) / math.log(10.0)))))
            if Rw <= 0.5:
                K2s = 0.8238
            if Rw > 0.9628:
                K2s = 1.0 - (0.3957 * math.pow((1.0 - Rw), 0.5136))

            Pddfm = Pdfm * Pdfm / (Mu * (1.0 - K2s)) #probability of worst month space diversity dispersive fading

            #Worst month (ITU-R) dispersive fading
            SecDFmonth = Tsmonth * Pddfm

            #Annual (North American) dispersive fading
            SecDFyear = Tsyear * Pddfm * CMY

            #Total diversity dispersive fading outage seconds
            Pd = math.pow((math.pow(Pdffm,0.75) + math.pow(Pddfm,0.75)),(4.0 / 3.0))

            #Diversity worst month (ITU-R) fading
            TotalSecMonth = Tsmonth * Pd

            #Diversity annual (North American) fading
            TotalSecYear = Tsyear * Pd * CMY

        return SecFFyear, SecDFyear, TotalSecYear


    def execute(self):
        # open main folder

        FilePath = Path(str(self.ExampleS3FolderPath) + "/Data/PathDataPass2.csv")
        path_data_pass_df_2 = pd.read_csv(FilePath)

        FilePath = Path(str(self.ExampleS3FolderPath) + "/Data/PathDataPass3.csv")
        path_data_pass_df_3 = open(FilePath, "w+") 

        PrintFile = "PathIndex,TXPwr,TXCoupling,LeftAntennaGain,LeftWGAttn,FreeSpaceLoss,AtmosphericAtten,RightAntennaGain,RightWGAttn,Threshold,RXCoupling,MiscLoss,FieldMargin,FadeMargin,Distance,Frequency,NAFlatFadeSecs,NADispFadeSecs,NATotalMultipathSecs,CraneRainSeconds,ITU-RFlatFadeSecs,ITU-RDispFadeSecs,ITU-RTotalMultipathSecs,ITU-RRainSeconds\n"

        path_data_pass_df_3.write(PrintFile)

        PathParametersFilePath = Path(str(self.ExampleS3FolderPath) + "/Data/PathParameters.csv")

        PathsFilePath = Path(str(self.ExampleS3FolderPath) + "/Paths.csv")

        RRCurvesFolderPath = Path(str(self.ExampleS3FolderPath) + "/Data/RRCurves")

        RainCityIndexFilePath = (str(Path(RRCurvesFolderPath)) + "/Rain City Index.csv")

        for index, row in path_data_pass_df_2.iterrows():
            # 'input the primary path data --------------------------------------
            PathIndex = int(row['Index'])
            RadioCompany = row['Radio Company']
            RadioModel = row['Radio Model']
            AltRadioModel = row['Alt Radio Model']
            Freq = row['Freq (avg)']
            Polarization = row['Polarization']
            ChannelBW = row['Channel BW']
            DataRate = row['Data Rate']
            Modulation = row['Modulation']
            Threshold = row['Threshold']
            ACMOffset = row['ACM Offset']
            DFM = row['DFM']
            TXPwr = row['TX Pwr']
            TXCoupling = row['TX Coupling']
            RXCoupling = row['RX Coupling']
            LeftAntennaModel = row['Left Antenna Model']
            LeftAntennaGain = row['Left Antenna Gain']
            LeftSDAntenna = row['Left SD Antenna'],
            LeftSDAntennaGain = row['Left SD Antenna Gain']
            if math.isnan(LeftSDAntennaGain):
                LeftSDAntennaGain = 0
            LeftSDSpacing = row['Left SD Spacing (ft)']
            if math.isnan(LeftSDSpacing):
                LeftSDSpacing = 0
            RightAntennaModel = row['Right Antenna Model']
            RightAntennaGain = row['Right Antenna Gain']
            RightSDAntenna = row['Right SD Antenna']
            RightSDAntennaGain = row['Right SD Antenna Gain']
            if math.isnan(RightSDAntennaGain):
                RightSDAntennaGain = 0
            RightSDSpacing = row['Right SD Spacing (ft)']
            if math.isnan(RightSDSpacing):
                RightSDSpacing = 0
            LeftWaveguide = row['Left Waveguide']
            LeftWGLength = row['Left WG Length (ft)']
            LeftWGAttn = row['Left WG Attn']
            if math.isnan(LeftWGAttn):
                LeftWGAttn = 0
            RightWaveguide = row['Right Waveguide']
            RightWGLength = row['Right WG Length (ft)']
            RightWGAttn = row['Right WG Attn']
            if math.isnan(RightWGAttn):
                RightWGAttn = 0
            FreeSpaceLoss = row['Free Space Loss']
            AtmosphericAtten = row['Atmospheric Atten']
            MiscLoss = row['Misc Loss']
            FieldMargin = row['Field Margin']
            RelDispersion = row['Rel Dispersion']
            NotchWidth = row['NotchWidth']
            NotchDepth = row['NotchDepth']
            LeftAntHt = row['LeftAntHeight']
            RightAntHt = row['RightAntHeight']

            Gfreq = float(Freq) / 1000

            # 'find additional path parameters
            path_params_df = pd.read_csv(PathParametersFilePath)

            row = path_params_df.loc[path_params_df['Index'] == (PathIndex)]

            if not row.empty:
                Distance = row['Path Distance (miles)']
                PathRoughness = row['Path Roughness (ft)']
                ClimateFactor = row['Climate Factor']
                TempF = row['Temp (F)']
                dN1 = row['dN1']
                Sa = row['Sa (ft)']
                R01 =row['Rain Rate']
                RelHumidity = row['Relative Humidity']
                HL = row['Lower Height (ft)']

            else:
                print("Path number <" + str(PathIndex) + "> was not matched during additional path parameter gathering.")
                print("Program is terminated.")
                exit(1)

            # '----------------------------------
            # ' Get primary path data
            print("line 431")
            paths_df = pd.read_csv(PathsFilePath)

            row = paths_df.loc[paths_df['Index'] == (PathIndex)]

            if not row.empty:
                Site1 = row['Site1']
                Site1Latitude = row['Latitude1']
                Site1Longitude = row['Longitude1']
                Site2 = row['Site2']
                Site2Latitude = row['Latitude2']
                Site2Longitude = row['Longitude2']
            else:
                print("Path number <" + str(PathIndex) + "> was not matched during additional path parameter gathering.")
                print("Program is terminated.")
                exit(1)

            FadeMargin = float(TXPwr) - float(TXCoupling) + float(LeftAntennaGain) - float(LeftWGAttn) - \
                        float(FreeSpaceLoss) - float(AtmosphericAtten) + float(RightAntennaGain) - \
                        float(RightWGAttn) - float(Threshold) - float(RXCoupling) - float(MiscLoss) - float(FieldMargin)

            # 'estimate North American multipath outages --------------------------------------
            AntennaGain = LeftAntennaGain
            SDGain = LeftSDAntennaGain
            DivSpacing = LeftSDSpacing
            SecFFyear, SecDFyear, TotalSecYear = self.calculateMultipathOutage(TempF, ClimateFactor, PathRoughness, Freq, Distance, FadeMargin, DFM, RelDispersion, AntennaGain, SDGain, DivSpacing) # 'calculate multipath outage using Vigants-Barnett method

            RightLeftFFSecs = SecFFyear
            RightLeftDFSecs = SecDFyear
            RightLeftTotalSecs = TotalSecYear

            AntennaGain = RightAntennaGain
            SDGain = RightSDAntennaGain
            DivSpacing = RightSDSpacing
            SecFFyear, SecDFyear, TotalSecYear = self.calculateMultipathOutage(TempF, ClimateFactor, PathRoughness, Freq, Distance, FadeMargin, DFM, RelDispersion, AntennaGain, SDGain, DivSpacing) # 'calculate multipath outage using Vigants-Barnett method

            LeftRightFFSecs = SecFFyear
            LeftRightDFSecs = SecDFyear
            LeftRightTotalSecs = TotalSecYear

            VBTotalFFSecs = RightLeftFFSecs + LeftRightFFSecs
            VBTotalDFSecs = RightLeftDFSecs + LeftRightDFSecs
            # print("RightLeftTotalSecs", RightLeftTotalSecs)
            # print("LeftRightTotalSecs", LeftRightTotalSecs)

            VBTotalMultipathSecs = RightLeftTotalSecs + LeftRightTotalSecs

            # 'estimate North American rain outages --------------------------------------
            # 'calculate rain outage seconds using the Crane method
            # '***************************************
            # 'Determine the appropriate rain curve city
            # '***************************************
            LATITUDEA = (float(Site1Latitude) + float(Site2Latitude)) / 2
            LONGITUDEA = (float(Site1Longitude) + float(Site2Longitude)) / 2

            OldDistance = 5000
            OldIndex = "0"
            OldCity = ""
            OldState = ""
            OldCountry = ""

            rain_city_index_df = pd.read_csv(RainCityIndexFilePath)

            for index, row in rain_city_index_df.iterrows():
                NewIndex = row['Index']
                NewCity = row['Site']
                NewState = row['State / Province']
                NewCountry = row['Country']
                LatitudeB = row['Latitude']
                LongitudeB = row['Longitude']
                Zmiles = self.distance_between_a_and_b("m", LATITUDEA, LatitudeB, LONGITUDEA, LongitudeB)

                if Zmiles < OldDistance:
                    OldDistance = Zmiles
                    OldIndex = NewIndex
                    OldCity = NewCity
                    OldState = NewState
                    OldCountry = NewCountry

            Curve = OldIndex

            # '***************************************
            # 'Crane Model
            # '***************************************
            # 'results are two way based upon data in feet or mile units

            Gfreq = float(Gfreq) # 'frequency, GHz
            Pol = Polarization # 'polarization, V or H
            if Pol == "v":
                Pol = "V"
            if Pol == "h":
                Pol = "H"
            if Pol != "V" and Pol != "H":
                print("Polarization <" + Pol + "> was not in expected format>")
                print("Program is terminated.")
                exit(1)

            PathLenMiles = float(Distance) # 'path length in miles
            FadeMargin = float(FadeMargin) # 'fade margin in dB

            PathLenKM = 1.60934 * PathLenMiles # 'path length in kilometers

            # 'Note that in this program math.log(X) = natural logarithm of X ( ln(X) )
            # 'math.log base 10 (X) = math.log(X) / math.log(10)
            # 'Calculate rain fading time
            # 'Determine K and Alpha factors
            # '***************************************
            # ' GET ITU-R K & ALPHA AS A FUNCTION OF FREQUENCY & POLARIZATION
            # 'Calculate K and Alpha factors
            # '----------------------
            kHa1 = -5.3398
            kHa2 = -0.35351
            kHa3 = -0.23789
            kHa4 = -0.94158
            kVa1 = -3.80595
            kVa2 = -3.44965
            kVa3 = -0.39902
            kVa4 = 0.50167
            aHa1 = -0.14318
            aHa2 = 0.29591
            aHa3 = 0.32177
            aHa4 = -5.3761
            aHa5 = 16.1721
            aVa1 = -0.07771
            aVa2 = 0.56727
            aVa3 = -0.20238
            aVa4 = -48.2991
            aVa5 = 48.5833
            # '---------------------
            kHb1 = -0.10008
            kHb2 = 1.2697
            kHb3 = 0.86036
            kHb4 = 0.64552
            kVb1 = 0.56934
            kVb2 = -0.22911
            kVb3 = 0.73042
            kVb4 = 1.07319
            aHb1 = 1.82442
            aHb2 = 0.77564
            aHb3 = 0.63773
            aHb4 = -0.9623
            aHb5 = -3.2998
            aVb1 = 2.3384
            aVb2 = 0.95545
            aVb3 = 1.1452
            aVb4 = 0.791669
            aVb5 = 0.791459
            # '---------------------
            kHc1 = 1.13098
            kHc2 = 0.454
            kHc3 = 0.15354
            kHc4 = 0.16817
            kVc1 = 0.81061
            kVc2 = 0.51059
            kVc3 = 0.11899
            kVc4 = 0.27195
            aHc1 = -0.55187
            aHc2 = 0.19822
            aHc3 = 0.13164
            aHc4 = 1.47828
            aHc5 = 3.4399
            aVc1 = -0.76284
            aVc2 = 0.54039
            aVc3 = 0.26809
            aVc4 = 0.116226
            aVc5 = 0.116479
            # '---------------------
            kHmk = -0.18961
            kVmk = -0.16398
            aHma = 0.67849
            aVma = -0.053739
            # '---------------------
            kHck = 0.71147
            kVck = 0.63297
            aHca = -1.95537
            aVca = 0.83433
            # '----------------------

            # 'kH
            k1 = ((math.log(Gfreq) / math.log(10)) - kHb1) / kHc1
            k1 = -k1 * k1
            k1 = kHa1 * math.exp(k1)
            k2 = ((math.log(Gfreq) / math.log(10)) - kHb2) / kHc2
            k2 = -k2 * k2
            k2 = kHa2 * math.exp(k2)
            k3 = ((math.log(Gfreq) / math.log(10)) - kHb3) / kHc3
            k3 = -k3 * k3
            k3 = kHa3 * math.exp(k3)
            k4 = ((math.log(Gfreq) / math.log(10)) - kHb4) / kHc4
            k4 = -k4 * k4
            k4 = kHa4 * math.exp(k4)

            log10k = k1 + k2 + k3 + k4 + (kHmk * math.log(Gfreq) / math.log(10)) + kHck
            kH = math.pow(10, log10k)

            #  'kV
            k1 = ((math.log(Gfreq) / math.log(10)) - kVb1) / kVc1
            k1 = -k1 * k1
            k1 = kVa1 * math.exp(k1)
            k2 = ((math.log(Gfreq) / math.log(10)) - kVb2) / kVc2
            k2 = -k2 * k2
            k2 = kVa2 * math.exp(k2)
            k3 = ((math.log(Gfreq) / math.log(10)) - kVb3) / kVc3
            k3 = -k3 * k3
            k3 = kVa3 * math.exp(k3)
            k4 = ((math.log(Gfreq) / math.log(10)) - kVb4) / kVc4
            k4 = -k4 * k4
            k4 = kVa4 * math.exp(k4)

            log10k = k1 + k2 + k3 + k4 + (kVmk * math.log(Gfreq) / math.log(10)) + kVck
            kV = math.pow(10, log10k)

            #  'aH
            a1 = ((math.log(Gfreq) / math.log(10)) - aHb1) / aHc1
            a1 = -a1 * a1
            a1 = aHa1 * math.exp(a1)
            a2 = ((math.log(Gfreq) / math.log(10)) - aHb2) / aHc2
            a2 = -a2 * a2
            a2 = aHa2 * math.exp(a2)
            a3 = ((math.log(Gfreq) / math.log(10)) - aHb3) / aHc3
            a3 = -a3 * a3
            a3 = aHa3 * math.exp(a3)
            a4 = ((math.log(Gfreq) / math.log(10)) - aHb4) / aHc4
            a4 = -a4 * a4
            a4 = aHa4 * math.exp(a4)
            a5 = ((math.log(Gfreq) / math.log(10)) - aHb5) / aHc5
            a5 = -a5 * a5
            a5 = aHa5 * math.exp(a5)
            aH = a1 + a2 + a3 + a4 + a5 + (aHma * math.log(Gfreq) / math.log(10)) + aHca

            #  'aV
            a1 = ((math.log(Gfreq) / math.log(10)) - aVb1) / aVc1
            a1 = -a1 * a1
            a1 = aVa1 * math.exp(a1)
            a2 = ((math.log(Gfreq) / math.log(10)) - aVb2) / aVc2
            a2 = -a2 * a2
            a2 = aVa2 * math.exp(a2)
            a3 = ((math.log(Gfreq) / math.log(10)) - aVb3) / aVc3
            a3 = -a3 * a3
            a3 = aVa3 * math.exp(a3)
            a4 = ((math.log(Gfreq) / math.log(10)) - aVb4) / aVc4
            a4 = -a4 * a4
            a4 = aVa4 * math.exp(a4)
            a5 = ((math.log(Gfreq) / math.log(10)) - aVb5) / aVc5
            a5 = -a5 * a5
            a5 = aVa5 * math.exp(a5)
            aV = a1 + a2 + a3 + a4 + a5 + (aVma * math.log(Gfreq) / math.log(10)) + aVca

            if Pol == "V":
                K = kV
                Alpha = aV
            if Pol == "H":
                K = kH
                Alpha = aH

            # '***************************************
            # 'Determine rain rate R
            # '***************************************
            # ' CRANE RAIN ATTENUATION MODEL
            # 'Determine rain rate R for given fade margin and path length
            L = PathLenKM
            if PathLenKM > 22.5:
                L = 22.5
            R = 0.001
            Rstep = 20

            # TODO
            while True:
                if R > 550:
                    # 'R exceeds 550.  This is not allowed.
                    OutageSec = 0
                    print("Rain rate exceeds 550.")
                    break
                if R <= 0:
                    print("R is zero or less.  This is not allowed.")
                    OutageSec = 0
                    print("Rain rate too low.")
                    break

                B = 2.3 / math.pow(R, (0.17))
                # B = 2.3 * (R,(-.17))
                C = 0.026 - (0.03 * math.log(R))
                D = 3.8 - (0.6 * math.log(R))
                U = (math.log(B) / D) + C
                # U = (math.log(B * (math.exp(C * D)))) / D   #alternate formula
                KRAlpha = K * math.pow(R, Alpha)
                if L <= D:
                    PathEff = ((math.exp(U * Alpha * L)) - 1) / (U * Alpha)
                else:
                    NM1 = ((math.exp(U * Alpha * D)) - 1) / (U * Alpha)
                    NM2 = math.pow(B, Alpha) * ((math.exp(C * Alpha * L)) - (math.exp(C * Alpha * D))) / (C * Alpha)
                    PathEff = (NM1 + NM2)
                    # PathEff = ((math.exp(U * Alpha * D) - 1) / U + B,Alpha / C * (-math.exp(C * Alpha * D) + math.exp(C * Alpha * L))) / Alpha  #alternate formula

                Pt2Path = PathEff / PathLenKM
                TrialMargin = K * math.pow(R, Alpha) * PathEff

                if TrialMargin < FadeMargin:
                    if Rstep < 0.01:
                        break
                else:
                    R = R - Rstep
                    Rstep = Rstep / 2
                    if Rstep < 0.01:
                        break

                R = R + Rstep

            # if R <= 0:
            #     print("R is zero or less.  This is not allowed.")
            #     OutageSec = 0
            #     print("Rain rate too low.")
            #     break
            #
            # B = 2.3 / math.pow(R, (0.17))
            # #B = 2.3 * (R,(-.17))
            # C = 0.026 - (0.03 * math.log(R))
            # D = 3.8 - (0.6 * math.log(R))
            # U = (math.log(B) / D) + C
            # #U = (math.log(B * (math.exp(C * D)))) / D   #alternate formula
            # KRAlpha = K * math.pow(R, Alpha)
            # if L <= D:
            #     PathEff = ((math.exp(U * Alpha * L)) - 1) / (U * Alpha)
            # if L > D:
            #     NM1 = ((math.exp(U * Alpha * D)) - 1) / (U * Alpha)
            #     NM2 = math.pow(B, Alpha) * ((math.exp(C * Alpha * L)) - (math.exp(C * Alpha * D))) / (C * Alpha)
            #     PathEff = (NM1 + NM2)
            #     #PathEff = ((math.exp(U * Alpha * D) - 1) / U + B,Alpha / C * (-math.exp(C * Alpha * D) + math.exp(C * Alpha * L))) / Alpha  #alternate formula
            #
            # Pt2Path = PathEff / PathLenKM
            # TrialMargin = K * math.pow(R, Alpha) * PathEff
            # if TrialMargin < FadeMargin:
            #     if Rstep < 0.01:
            #         pass
            #
            # R = R - Rstep
            # Rstep = Rstep / 2
            #
            # R = R + Rstep
            # # print("R:", R)
            # if R > 550:
            #     # 'R exceeds 550.  This is not allowed.
            #     OutageSec = 0
            #     print("Rain rate exceeds 550.")
            #     break

            # '***************************************

            # 'Determine the outage time associated with R

            # '***************************************
            while True:
                if R <= 0 or R > 550:
                    break
                curve_df = pd.read_csv(Path(str(RRCurvesFolderPath) + "/Curve" + str(Curve) + ".csv"))
                curve_df = curve_df.iloc[7:]
                curve_df = curve_df.reset_index(drop=True)
                curve_df.columns = curve_df.iloc[0]
                curve_df = curve_df.iloc[1:]
                curve_df.columns = ['Rain Time', 'Unavailability', 'Rain Rate']

                MinutesOld = 0
                PerCentOld = 0
                RateOld = 0

                for index, row in curve_df.iterrows():
                    # 'Kizer City Data
                    Minutes = float(row['Rain Time'])
                    PerCent = float(row['Unavailability'])
                    Rate = float(row['Rain Rate'])

                    # TODO
                    # MinutesOld = Minutes
                    # PerCentOld = PerCent
                    # RateOld = Rate
                    if R >= float(row['Rain Rate']):
                        break
                    else:
                        MinutesOld = Minutes
                        PerCentOld = PerCent
                        RateOld = Rate
                # 'Interpolate the rain rate

                X1var = RateOld
                X2var = Rate
                Y1var = PerCentOld
                Y2var = PerCent
                Xvar = R
                MinutesInYear = 365.25 * 24 * 60

                while True:
                    if abs(X1var - X2var) < 0.000001:
                        Yvar = Y1var
                        break

                    if abs(Y1var - Y2var) < 0.000001:
                        Yvar = Y1var
                        break

                    if Y1var <= 0:
                        Yvar = Y1var
                        break
                    LogYvar = (math.log(Y1var) / math.log(10)) + \
                            (((math.log(Y2var / Y1var) / math.log(10)) / (X2var - X1var)) * (Xvar - X1var))
                    Yvar = math.pow(10, LogYvar)
                    break

                # '***************************************
                # 'Linear Interpolation, X & Log Y

                # LogYvar = (math.log(Y1var) / math.log(10)) + \
                #           (((math.log(Y2var / Y1var) / math.log(10)) / (X2var - X1var)) * (Xvar - X1var))
                # Yvar = math.pow(10, LogYvar)

                # '***************************************
                MinutesInYear = 365.25 * 24 * 60
                OutagePerCent = Yvar

                if PathLenKM > 22.5:
                    OutagePerCent = OutagePerCent * PathLenKM / 22.5
                Availability = 100 - OutagePerCent
                OutageMin = OutagePerCent * MinutesInYear / 100
                OutageSec = 60 * OutageMin

                if OutageSec < 3.5:
                    OutageSec = 0
                break

            CraneTotalRainSecs = OutageSec

            #  'estimate ITU-R multipath outages --------------------------------------

            AntennaGain = LeftAntennaGain
            SDGain = LeftSDAntennaGain
            DivSpacing = LeftSDSpacing
            SecFFyear, SecDFyear, TotalSecYear = self.calculateMultipathOutageITUR(Site1Latitude, Site2Latitude, Distance, dN1, Sa, HL, Gfreq, FadeMargin, LeftAntHt, RightAntHt,AntennaGain, SDGain, DivSpacing, NotchWidth, NotchDepth)
            RightLeftFFSecs = SecFFyear
            RightLeftDFSecs = SecDFyear
            RightLeftTotalSecs = TotalSecYear

            AntennaGain = RightAntennaGain
            SDGain = RightSDAntennaGain
            DivSpacing = RightSDSpacing
            SecFFyear, SecDFyear, TotalSecYear = self.calculateMultipathOutageITUR(Site1Latitude, Site2Latitude, Distance, dN1, Sa, HL, Gfreq, FadeMargin, LeftAntHt, RightAntHt, AntennaGain, SDGain, DivSpacing, NotchWidth, NotchDepth)
            LeftRightFFSecs = SecFFyear
            LeftRightDFSecs = SecDFyear
            LeftRightTotalSecs = TotalSecYear

            ITURTotalFFSecs = RightLeftFFSecs + LeftRightFFSecs
            ITURTotalDFSecs = RightLeftDFSecs + LeftRightDFSecs
            ITURTotalMultipathSecs = RightLeftTotalSecs + LeftRightTotalSecs

            # 6000 'calculate rain outage seconds using the ITU-R method
            RainFadeMargin = FadeMargin   #dB

            #Calculate K and Alpha as accomplished in Crane algorithm

            COUNT = 0
            M = RainFadeMargin
            RainDistance = 1.60934 * float(Distance)   #path distance in kilometers
            RainNote = ""
            ITURRainOutageSecs = "---"

            R01 = float(R01)  #from interpolation of ITU-R data
            PointAttn = K * math.pow(R01, Alpha)  #point (single location) rain attenuation

            R0 = (0.477 * math.pow(RainDistance, 0.633)) * math.pow(R01, (0.073 * Alpha)) * math.pow(Gfreq, 0.123)
            R0 = R0 - (10.579 * (1 - (1 / math.exp(0.024 * RainDistance))))
            R = 1 / R0  #point to path conversion factor
            if R > 2.5:
                R = 2.5

            A01 = PointAttn * RainDistance * R   #path rain attenuation not exceeded 0.01% of time

            while True:
                RainProb = 0.001
                Ap = self.subroutine6500(Gfreq, RainProb, A01)
                if Ap < M:
                    RainNote = "ITU-R rain path unavailability less than 0.001%."
                    ITURRainOutageSecs = "< 316"
                    break

                RainProb = 1
                Ap = self.subroutine6500(Gfreq, RainProb, A01)
                if Ap > M:
                    RainNote = "ITU-R rain path unavailability greater than 1%."
                    ITURRainOutageSecs = "> 315,576"
                    break

                RainProb = 0.001
                Delta = 0.0001
                OldSign = 1

                while True:
                    ITURRainOutageSecsNum = 0
                    COUNT = COUNT + 1
                    RainProb = RainProb + Delta
                    if RainProb < 0.001:
                        RainNote = "ITU-R rain rate convergence failed."
                        print(RainNote)
                        break

                    Ap = self.subroutine6500(Gfreq, RainProb, A01)
                    RainAvail = 100 - RainProb  #path availability due to rain
                    #print USING " Fade Margin = 0., Rain Attn =., Fade Prob =., Avail =."; COUNT; M; Ap; RainProb; RainAvail
                    Diff = M - Ap
                    if Diff < 0:
                        Sign = 1
                    else:
                        Sign = -1
                    if OldSign + Sign == 0:
                        Delta = -Delta / 10
                    else:
                        Delta = 1.5 * Delta
                    OldSign = Sign
                    if abs(Diff) < 0.01:
                        break

                if RainProb < 0.001:
                    break
                Tsyear = (365.25 * 24.0 * 60.0 * 60.0)
                ITURRainOutageSecs = (RainProb/100.0) * Tsyear
                ITURRainOutageSecsNum = ITURRainOutageSecs
                break

            if ITURRainOutageSecsNum == 0:
                ITURRainOutageSecsNum = ITURRainOutageSecs
            print(str(COUNT) + " Fade Margin = " + str(M) + ", Rain Attn =" + str(Ap) + ", Fade Prob = " + str(
                RainProb) + ", Outage Secs =" + str(ITURRainOutageSecsNum))
            if RainNote != "":
                print(RainNote)
            print(str(PathIndex) + "," + Distance.to_string(index=False) + "," + "freq" +str(Gfreq) + "," + str(FadeMargin) + "," + str(VBTotalMultipathSecs) + "," + str(CraneTotalRainSecs) + "," + str(ITURRainOutageSecs))
            Distance = Distance.to_string(index=False)
            # ' --------------------------------------
            PrintFile = str(PathIndex) + "," + str(TXPwr) + "," + str(TXCoupling) + "," + str(LeftAntennaGain) + "," + str(LeftWGAttn) + "," + str(FreeSpaceLoss) + "," + str(AtmosphericAtten) + ","
            PrintFile = PrintFile + str(RightAntennaGain) + "," + str(RightWGAttn) + "," + str(Threshold) + "," + str(RXCoupling) + "," + str(MiscLoss) + "," + str(FieldMargin) + ","
            PrintFile = PrintFile + str(FadeMargin) + "," + str(Distance) + "," + str(Gfreq) + "," + str(VBTotalFFSecs) + "," + str(VBTotalDFSecs) + "," + str(VBTotalMultipathSecs) + "," + str(CraneTotalRainSecs) + "," + str(ITURTotalFFSecs) + "," + str(ITURTotalDFSecs) + "," + str(ITURTotalMultipathSecs) + "," + str(ITURRainOutageSecs) + "\n"
            path_data_pass_df_3.write(PrintFile)

            print("Calculations for path <" + str(PathIndex) + "> completed.\n")

        print("Program completed")


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

test = Performance()
ExampleS3FolderPath = Path(ex.openFolderNameDialog("Find ExampleStep3 Folder"))
##"C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Step 3 Path Availability/ExampleStep3"
test.setFolderPath(ExampleS3FolderPath)
test.execute()
input("Press Enter to exit")