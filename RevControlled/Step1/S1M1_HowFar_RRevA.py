# "How Far You Can Go" calculations

import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

def rainRate():
    # *************************************** Line 725
    # Determine rain rate R

    # ***************************************
    # CRANE RAIN ATTENUATION MODEL

    # Determine rain rate R for given fade margin and path length
    L = PathLenKM
    if PathLenKM > 22.5:
        L = 22.5
    R = .001
    Rstep = 20

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
    return      # probably need to return some stuff

def outageTime():
    while True:
        if R <= 0 or R > 550:
            break
        curve_df = pd.read_csv(RRCurvesFolderPath + "/Curve" + str(Curve) + ".csv")
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

    return OutageSec # probably need to return more stuff here

    # *************************************** Line 854

# Set the number of significant digits to 1
def SigFig1(num):
    num = int((num * 10) + .5)
    num = num / 10
    return num 

## TODO -- make sig fig functions


# def GO8210(R, L, Rstep):
#     if R > 550:
#         # R exceeds 550.  This is not allowed.
#         OutageSec = 0
#         # GOTO 8999
#         return # add some flag here
#     if R <= 0:
#         sys.exit("R is zero or less.  This is not allowed.")

#     B = 2.3 / (R ** (.17))
# 	    #B = 2.3 * (R ** (-.17))
#     C = .026 - (.03 * math.log(R))
#     D = 3.8 - (.6 * math.log(R))
#     U = (math.log(B) / D) + C
#         #U = (math.log(B * (math.exp(C * D)))) / D   alternate formula
#     KRAlpha = K * (R ** Alpha)

#     if L <= D:
#         PathEff = ((math.exp(U * Alpha * L)) - 1) / (U * Alpha)

#     if L > D:
#         NM1 = ((math.exp(U * Alpha * D)) - 1) / (U * Alpha)
#         NM2 = (B ** Alpha) * ((math.exp(C * Alpha * L)) - (math.exp(C * Alpha * D))) / (C * Alpha)
#         PathEff = (NM1 + NM2)
#             #PathEff = ((math.exp(U * Alpha * D) - 1) / U + B ** Alpha / C * (-math.exp(C * Alpha * D) + math.exp(C * Alpha * L))) / Alpha  'alternate formula

#     Pt2Path = PathEff / PathLenKM
#     TrialMargin = K * (R ** Alpha) * PathEff

#     # *************************************** Line 763
#     if TrialMargin < FadeMargin:
#         if Rstep < .01:
#             return #GOTO 8230
#         R = R + Rstep
#         GO8210(R, L, Rstep) #GOTO 8210
#     else:    
#         R = R - Rstep
#         Rstep = Rstep / 2

#     # *************************************** Line 772










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
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS1 Folder")

# Create file paths using main folder path
OutputFilePath = ExampleS3FolderPath + "/Output.csv"
CitiesFilePath = ExampleS3FolderPath + "/Cities.csv"
RRCurvesFolderPath = ExampleS3FolderPath + "/RRCurves"
RadiosFilePath = ExampleS3FolderPath + "/Radios.csv"

CityNumber = input("Input the city number: ")
cities_df = pd.read_csv(CitiesFilePath)

headers = list(cities_df.columns)

# This section can be optimized with a database
for dex, row in cities_df.iterrows():
    if (str(row[0]) == str(CityNumber)):      # if Index matches CityNumber, read entire row into variables then break loop
        Index = int(row[0])
        Zone = str(row[1])
        Site = str(row[2])
        State = str(row[3])
        Latitude = float(row[4])
        Longitude = float(row[5])
        ClimateFactor = float(row[6])
        Roughness = float(row[7])
        Temp = float(row[8])
        break

if not (str(row[0]) == str(CityNumber)):
    print("The city number " + CityNumber + " could not be found.")
    sys.exit()
    # Code a safe exit here -- program should not continue

print("The city chosen is " + Site + "\n")
print("No wet radome loss is used in these calculations.\n")

print("Currently path roughness is " + str(Roughness) + " feet." + "\n")
answer = input("Do you want to use minimum roughness (20 feet)? (y or n) ")

if (answer.upper == "Y"):
    Roughness = "20"
    #Roughness# = 20?


radios_df = pd.read_csv(RadiosFilePath)
#HeaderRow = radios_df.iloc[-1]           # this file has two rows of header's
HeaderRow = list(radios_df.columns)

# Get first row of header values
ProjectName = HeaderRow[1]
AnswerUnits = HeaderRow[4]
AnswerModulation = HeaderRow[7]
MinimumFadeMargin = HeaderRow[10]

Units = "fm"         # feet miles

if (AnswerUnits.upper() == "M"):
    Units = "mk"     # meters kilometers

AM = "no"
if (AnswerModulation.upper() == "A"):
    AM = "yes"


output_df = open(OutputFilePath, "w+")

PrintFile = "Project:," + ProjectName

if (AM == "no"):
    PrintFile = PrintFile + ",,Fixed,Modulation"
if (AM == "yes"):
    PrintFile = PrintFile + ",,Adaptive,Modulation"
if (Units == "fm"):
    PrintFile = PrintFile + ",,feet & miles"
if (Units == "mk"):
    PrintFile = PrintFile + ",,m & km"

PrintFile = PrintFile + ",,Min Fade Margin:," + MinimumFadeMargin + " (dB)" + "\n\n"

output_df.write(PrintFile)

########## Line 104 ###########

PrintFile = "City #,Rain Zone,City,State"
PrintFile = PrintFile + ",Distance 99.9999%,Distance 99.9995%,Distance 99.999%"
PrintFile = PrintFile + ",Distance 99.995%,Distance 99.99%,Distance 99.95%"
PrintFile = PrintFile + ",Distance 99.9%,Distance 99.5%,Distance 99%"
PrintFile = PrintFile + ",Latitude,Longitude,Climate Factor,Roughness,Avg Temp"

PrintFile = PrintFile + ",Frequency (GHz),Polarization,Radio Model,Main Antenna"
PrintFile = PrintFile + ",RF Bandwidth (MHz),Modulation,Radio Capacity (MB/s),Transmit Power (dBm)"
PrintFile = PrintFile + ",Receiver Threshold (dBm),System Gain (dB),Link Budget (dB)" + "\n\n"

output_df.write(PrintFile)

Counter = 0
OldModel = ""
OldCounter = 0

#*************************************** Line 123

# I dont think this code will ever run
if (Counter > 0):
    output_df.write("------,------,------,------")
    Counter += 1

HeaderRow = list(radios_df.columns)     # ignore second row of headers, not sure if this works yet
NUMBER_OF_RADIOS = radios_df.shape[0] 
print(NUMBER_OF_RADIOS)
for index in range(1, NUMBER_OF_RADIOS):
#for index, row in radios_df.iterrows():
    row = radios_df.iloc[index]  

    Model = str(row[0])
    Frequency = float(row[1])
    Antenna = str(row[2])
    Gain = float(row[3])
    SDAntenna = row[4]

    SDGain = row[5]
    DivSpacing = row[6]
    Bandwidth = float(row[7])
    Modulation = float(row[8])
    Capacity = float(row[9])

    DFM = float(row[10])
    RDF = float(row[11])
    AMshift = float(row[12])
    MiscLoss = float(row[13])
    Power = float(row[14])

    Threshold = row[15]
    OperFreq = Frequency

    
    #Gain# = VAL(Gain)
    #Power# = VAL(Power)
    #Threshold# = VAL(Threshold)
    #MiscLoss# = VAL(MiscLoss)
    #AMshift# = VAL(AMshift)
    SystemGain = float(Power) - float(Threshold) - float(MiscLoss)
    LinkBudget = float(SystemGain) + float(Gain) + float(Gain)

    SpaceDiversity = "N"
    if (SDAntenna == SDAntenna and math.isnan(SDGain) == False):        # if SDAntenna and SDGain are defined (not nan)
        SpaceDiversity = "Y"

    # *************************************** Line 176

    for JJ in range(1, 3):
        if (JJ == 1):
            Polarization = "V"
        if (JJ == 2):
            Polarization = "H"

        # calculate how far you can go

        Seconds99 = 315576        #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.99)
        Seconds995 = 157788       #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.995)
        Seconds999 = 31558        #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.999)
        Seconds9995 = 15779       #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.9995)
        Seconds9999 = 3156        #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.9999)
        Seconds99995 = 1578       #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.99995)
        Seconds99999 = 316        #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.99999)
        Seconds999995 = 158       #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.999995)
        Seconds999999 = 32        #365.25 days/yr * 24 hrs/day * 60 mins/hr * 60 secs/min * (1 - 0.999999)

        DifSecs99 = 999999
        DifSecs995 = 999999
        DifSecs999 = 999999
        DifSecs9995 = 999999
        DifSecs9999 = 999999
        DifSecs99995 = 999999
        DifSecs99999 = 999999
        DifSecs999995 = 999999
        DifSecs999999 = 999999

        Distance99 = 0
        Distance995 = 0
        Distance999 = 0
        Distance9995 = 0
        Distance9999 = 0
        Distance99995 = 0
        Distance99999 = 0
        Distance999995 = 0
        Distance999999 = 0

        OldDifSecs999 = 999999999

        for J in range(1, 2001):
            Distance = J / 10       # Miles

            FreeSpaceLoss = 96.58 + (20 * math.log(float(OperFreq)) / math.log(10)) + (20 * math.log(float(Distance)) / math.log(10))

            # calculate atmospheric loss

            # *************************************** Line 229

            Freq = OperFreq                 #GHz
            T = Temp                        #annual temperature (deg F)
            TempC = (T - 32) * (5 / 9)      #degrees C
            Rho = 7.5                       #water-vapor density (g/m3)
            Pres = 1013                     #mean pressure (hectopascals [hPa] or millibars [mbar])
            Rp = Pres / 1013
            Rt = 288 / (273 + TempC)

            # For dry air, the attenuation AttnDryAir# (dB/km) is given by the following equations

            X11 = (Rp ** (.0717)) * (Rt ** (-1.8132))
            X12 = math.exp(((.0156) * (1 - Rp)) + ((-1.6515) * (1 - Rt)))
            Xi1 = X11 * X12

            X21 = (Rp ** (.5146)) * (Rt ** (-4.6368))
            X22 = math.exp(((-.1921) * (1 - Rp)) + ((-5.7416) * (1 - Rt)))
            Xi2 = X21 * X22

            X31 = (Rp ** (.3414)) * (Rt ** (-6.5851))
            X32 = math.exp(((.213) * (1 - Rp)) + ((-8.5854) * (1 - Rt)))
            Xi3 = X31 * X32

            X41 = (Rp ** (-.0112)) * (Rt ** (.0092))
            X42 = math.exp(((-.1033) * (1 - Rp)) + ((-.0009) * (1 - Rt)))
            Xi4 = X41 * X42

            X51 = (Rp ** (.2705)) * (Rt ** (-2.7192))
            X52 = math.exp(((-.3016) * (1 - Rp)) + ((-4.1033) * (1 - Rt)))
            Xi5 = X51 * X52

            X61 = (Rp ** (.2445)) * (Rt ** (-5.9191))
            X62 = math.exp(((.0422) * (1 - Rp)) + ((-8.0719) * (1 - Rt)))
            Xi6 = X61 * X62

            X71 = (Rp ** (-.1833)) * (Rt ** (6.5589))
            X72 = math.exp(((-.2402) * (1 - Rp)) + ((6.131) * (1 - Rt)))
            Xi7 = X71 * X72

            G541 = (Rp ** (1.8286)) * (Rt ** (-1.9487))
            G542 = math.exp(((.4051) * (1 - Rp)) + ((-2.8509) * (1 - Rt)))
            Gamma54 = 2.192 * G541 * G542

            G581 = (Rp ** (1.0045)) * (Rt ** (3.561))
            G582 = math.exp(((.1588) * (1 - Rp)) + ((1.2834) * (1 - Rt)))
            Gamma58 = 12.59 * G581 * G582

            G601 = (Rp ** (.9003)) * (Rt ** (4.1335))
            G602 = math.exp(((.0427) * (1 - Rp)) + ((1.6088) * (1 - Rt)))
            Gamma60 = 15 * G601 * G602

            G621 = (Rp ** (.9886)) * (Rt ** (3.4176))
            G622 = math.exp(((.1827) * (1 - Rp)) + ((1.3429) * (1 - Rt)))
            Gamma62 = 14.28 * G621 * G622

            G641 = (Rp ** (1.432)) * (Rt ** (.6258))
            G642 = math.exp(((.3177) * (1 - Rp)) + ((-.5914) * (1 - Rt)))
            Gamma64 = 6.819 * G641 * G642

            G661 = (Rp ** (2.0717)) * (Rt ** (-4.1404))
            G662 = math.exp(((.491) * (1 - Rp)) + ((-4.8718) * (1 - Rt)))
            Gamma66 = 1.908 * G661 * G662

            Delta1 = (Rp ** (3.211)) * (Rt ** (-14.94))
            Delta2 = math.exp(((1.583) * (1 - Rp)) + ((-16.37) * (1 - Rt)))
            Delta = -.00306 * Delta1 * Delta2

            if (float(Freq) <= 54):
                Ada1 = (7.2 * (Rt ** 2.8)) / ((float(Freq) ** 2) + (.34 * (Rp ** 2) * (Rt ** 1.6)))
                Ada2 = (.62 * Xi3) / (((54 - float(Freq)) ** (1.16 * Xi1)) + (.83 * Xi2))
                AttnDryAir = (((float(Freq) ** 2) * (Rp ** 2)) / 1000) * (Ada1 + Ada2)

            if (float(Freq) > 54 and float(Freq) <= 60):
                    Ada3 = (math.log(Gamma54)) * (float(Freq) - 58) * (float(Freq) - 60) / 24
                    Ada4 = (math.log(Gamma58)) * (float(Freq) - 54) * (float(Freq) - 60) / 8
                    Ada5 = (math.log(Gamma60)) * (float(Freq) - 54) * (float(Freq) - 58) / 12
                    AttnDryAir = math.exp(Ada3 - Ada4 + Ada5)
                    
            if (float(Freq) > 60 and float(Freq) <= 62):
                AttnDryAir = Gamma60 + ((Gamma62 - Gamma60) * (float(Freq) - 60) / 2)

            if (float(Freq) > 62 and float(Freq) <= 66):
                Ada6 = (math.log(Gamma62)) * (float(Freq) - 64) * (float(Freq) - 66) / 8
                Ada7 = (math.log(Gamma64)) * (float(Freq) - 62) * (float(Freq) - 66) / 4
                Ada8 = (math.log(Gamma66)) * (float(Freq) - 62) * (float(Freq) - 64) / 8
                AttnDryAir = math.exp(Ada6 - Ada7 + Ada8)

            if (float(Freq) > 66 and float(Freq) <= 120):
                Ada9 = (3.02 * (Rt ** 3.5) / 10000)
                Ada10A = (.283 * (Rt ** 3.8))
                Ada10B = ((float(Freq) - 118.75) ** 2) + (2.91 * (Rp ** 2) * (Rt ** 1.6))
                Ada10 = Ada10A / Ada10B
                Ada11A = .502 * Xi6 * (1 - (.0163 * Xi7 * (float(Freq) - 66)))
                Ada11B = ((float(Freq) - 66) ** (1.4346 * Xi4)) + (1.15 * Xi5)
                Ada11 = Ada11A / Ada11B
                AttnDryAir = (((float(Freq) ** 2) * (Rp ** 2)) / 1000) * (Ada9 + Ada10 + Ada11)

            if (float(Freq) > 120 and float(Freq) <= 350):
                Ada12A = (3.02 / 10000)
                Ada12B = 1 + (1.9 * (float(Freq) ** 1.5) / 100000)
                Ada12 = Ada12A / Ada12B
                Ada13A = .283 * (Rt ** .3)
                Ada13B = ((float(Freq) - 118.75) ** 2) + (2.91 * (Rp ** 2) * (Rt ** 1.6))
                Ada13 = Ada13A / Ada13B
                Ada14 = (float(Freq) ** 2) * (Rp ** 2) * (Rt ** 3.5) / 1000
                AttnDryAir = Delta + (Ada14 * (Ada12 + Ada13))

            if (float(Freq) > 350):
                AttnDryAir = .03
            
            # For water vapor, the attenuation AttnWetAir#  (dB/km) is given by the following:

            Eta1 = (.955 * Rp * (Rt ** .68)) + (.006 * Rho)
            Eta2 = (.735 * Rp * (Rt ** .5)) + (.0353 * (Rt ** 4) * Rho)

            Gfreq22 = 1 + (((float(Freq) - 22) / (float(Freq) + 22)) ** 2)
            Gfreq557 = 1 + (((float(Freq) - 557) / (float(Freq) + 557)) ** 2)
            Gfreq752 = 1 + (((float(Freq) - 752) / (float(Freq) + 752)) ** 2)
            Gfreq1780 = 1 + (((float(Freq) - 1780) / (float(Freq) + 1780)) ** 2)

            Awe1A = 3.98 * Eta1 * (math.exp(2.23 * (1 - Rt))) * Gfreq22
            Awe1B = ((float(Freq) - 22.235) ** 2) + (9.42 * (Eta1 ** 2))
            Awe1 = Awe1A / Awe1B

            Awe2A = 11.96 * Eta1 * (math.exp(.7 * (1 - Rt)))
            Awe2B = ((float(Freq) - 183.31) ** 2) + (11.14 * (Eta1 ** 2))
            Awe2 = Awe2A / Awe2B

            Awe3A = .081 * Eta1 * (math.exp(6.44 * (1 - Rt)))
            Awe3B = ((float(Freq) - 321.226) ** 2) + (6.29 * (Eta1 ** 2))
            Awe3 = Awe3A / Awe3B

            Awe4A = 3.66 * Eta1 * (math.exp(1.6 * (1 - Rt)))
            Awe4B = ((float(Freq) - 325.153) ** 2) + (9.22 * (Eta1 ** 2))
            Awe4 = Awe4A / Awe4B

            Awe5A = 25.37 * Eta1 * (math.exp(1.09 * (1 - Rt)))
            Awe5B = ((float(Freq) - 380) ** 2)
            Awe5 = Awe5A / Awe5B

            Awe6A = 17.4 * Eta1 * (math.exp(1.46 * (1 - Rt)))
            Awe6B = ((float(Freq) - 448) ** 2)
            Awe6 = Awe6A / Awe6B

            Awe7A = 844.6 * Eta1 * (math.exp(.17 * (1 - Rt))) * Gfreq557
            Awe7B = ((float(Freq) - 557) ** 2)
            Awe7 = Awe7A / Awe7B

            Awe8A = 290 * Eta1 * (math.exp(.41 * (1 - Rt))) * Gfreq752
            Awe8B = ((float(Freq) - 752) ** 2)
            Awe8 = Awe8A / Awe8B

            Awe9A = 83328 * Eta2 * (math.exp(.99 * (1 - Rt))) * Gfreq1780
            Awe9B = ((float(Freq) - 1780) ** 2)
            Awe9 = Awe9A / Awe9B

            Awe10A = Awe1 + Awe2 + Awe3 + Awe4 + Awe5
            Awe10 = Awe10A + Awe6 + Awe7 + Awe8 + Awe9

            AttnWetAir = Awe10 * (float(Freq) ** 2) * (Rt ** 2.5) * Rho / 10000

            AttnAir = AttnDryAir + AttnWetAir
            PathAttnAir = AttnAir * (Distance * 1.60934)

            # *************************************** Line 433

            FreeSpaceLoss = FreeSpaceLoss + PathAttnAir

            #FreeSpaceLoss = int((10 * FreeSpaceLoss) + .5)
            #FreeSpaceLoss = FreeSpaceLoss / 10
            FreeSpaceLoss = round(FreeSpaceLoss, 1)

            FadeMargin = float(LinkBudget) - float(FreeSpaceLoss)

            if (AM == "yes"):
                FadeMargin = float(FadeMargin) - float(AMshift)

            #FadeMargin = int((10 * float(FadeMargin)) + .5)
            #FadeMargin = float(FadeMargin) / 10
            FadeMargin = round(FadeMargin, 1)

            # calculate multipath outage seconds

            # *************************************** Line 447

            # Vigants Model

            T = float(Temp) #annual temperature (deg F)

            C = float(ClimateFactor) #climate factor

            W = float(Roughness) #terrain roughness (ft)

            if W < 20:
                W = 20
            if W > 140:
                W = 140

            F = float(OperFreq) #frequency (GHz)

            D = float(Distance)    #path distance (miles)

            FFM = float(FadeMargin) #flat fade margin (dB)

            DFM = float(DFM) #dispersive fade margin (dB)

            RDF = float(RDF) #multiplicative dispersive fading factor

            R = C * ((W / 50) ** -1.3) * (F / 4) * (D ** 3) / 100000

            Ts = 8000000 * (T / 50)

            Secsff = Ts * R / (10 ** (FFM / 10))

            Secsdf = Ts * R * RDF / (10 ** (DFM / 10))

            SecsTotal = Secsff + Secsdf

            SecsTotal2Way = 2 * SecsTotal

            if SpaceDiversity == "Y":
                # Space Diversity results"

                P1 = Gain  # main antenna gain (dB)

                P2 = SDGain  # diversity antenna gain (dB)

                S = DivSpacing  # diversity antenna spacing (ft)convert meters to feet

                if Units == "mk":
                    S = S * 3.28084

                P = P2 - P1

                Isdff = (7 / 100000) * (S ** 2) * F * (10 ** (P / 10)) * (10 ** (FFM / 10)) / D

                if Isdff > 200:
                    Isdff = 200

                Isddf = .09 * F * (10 ** (DFM / 10)) / D

                if Isddf > 200:
                    Isddf = 200

                Secsff = Secsff / Isdff

                Secsdf = Secsdf / Isddf

                SecsTotal = Secsff + Secsdf

                SecsTotal2Way = 2 * SecsTotal
            
            # *************************************** Line 516

            MultiOutage = SecsTotal2Way
            #MultiOutage = int((10 * MultiOutage) + .5)
            #MultiOutage = (MultiOutage / 10)
            MultiOutage = round(MultiOutage, 1)


            # calculate rain outage

            # ***************************************
            Curve = Index

            Freq = OperFreq                         # frequency, GHz
            Pol = Polarization                     # polarization, V or H
            PathLenMiles = Distance                 # path length in miles

            PathLenKM = 1.60934 * PathLenMiles      # path length in kilometers

            # Note that in this program math.log(X) = natural logarithm of X ( ln(X) )
            # math.log base 10 (X) = math.log(X) / math.log(10)

            # Calculate rain fading time

            # Determine K and Alpha factors

            # *************************************** Line 544
            # GET ITU-R K & ALPHA AS A FUNCTION OF FREQUENCY & POLARIZATION

            # Calculate K and Alpha factors

            # ----------------------
            kHa1 = -5.3398
            kHa2 = -.35351
            kHa3 = -.23789
            kHa4 = -.94158

            kVa1 = -3.80595
            kVa2 = -3.44965
            kVa3 = -.39902
            kVa4 = .50167

            aHa1 = -.14318
            aHa2 = .29591
            aHa3 = .32177
            aHa4 = -5.3761
            aHa5 = 16.1721

            aVa1 = -.07771
            aVa2 = .56727
            aVa3 = -.20238
            aVa4 = -48.2991
            aVa5 = 48.5833
            # ----------------------
            kHb1 = -.10008
            kHb2 = 1.2697
            kHb3 = .86036
            kHb4 = .64552

            kVb1 = .56934
            kVb2 = -.22911
            kVb3 = .73042
            kVb4 = 1.07319

            aHb1 = 1.82442
            aHb2 = .77564
            aHb3 = .63773
            aHb4 = -.9623
            aHb5 = -3.2998

            aVb1 = 2.3384
            aVb2 = .95545
            aVb3 = 1.1452
            aVb4 = .791669
            aVb5 = .791459
            # ----------------------
            kHc1 = 1.13098
            kHc2 = .454
            kHc3 = .15354
            kHc4 = .16817

            kVc1 = .81061
            kVc2 = .51059
            kVc3 = .11899
            kVc4 = .27195

            aHc1 = -.55187
            aHc2 = .19822
            aHc3 = .13164
            aHc4 = 1.47828
            aHc5 = 3.4399

            aVc1 = -.76284
            aVc2 = .54039
            aVc3 = .26809
            aVc4 = .116226
            aVc5 = .116479
            # ----------------------
            kHmk = -.18961
            kVmk = -.16398
            aHma = .67849
            aVma = -.053739
            # ----------------------
            kHck = .71147
            kVck = .63297
            aHca = -1.95537
            aVca = .83433
            # ---------------------- Line 625

            # kH

            k1 = ((math.log(Freq) / math.log(10)) - kHb1) / kHc1
            k1 = -k1 * k1
            k1 = kHa1 * math.exp(k1)

            k2 = ((math.log(Freq) / math.log(10)) - kHb2) / kHc2
            k2 = -k2 * k2
            k2 = kHa2 * math.exp(k2)

            k3 = ((math.log(Freq) / math.log(10)) - kHb3) / kHc3
            k3 = -k3 * k3
            k3 = kHa3 * math.exp(k3)

            k4 = ((math.log(Freq) / math.log(10)) - kHb4) / kHc4
            k4 = -k4 * k4
            k4 = kHa4 * math.exp(k4)

            log10k = k1 + k2 + k3 + k4 + (kHmk * math.log(Freq) / math.log(10)) + kHck
            kH = 10 ** log10k

            #kV

            k1 = ((math.log(Freq) / math.log(10)) - kVb1) / kVc1
            k1 = -k1 * k1
            k1 = kVa1 * math.exp(k1)

            k2 = ((math.log(Freq) / math.log(10)) - kVb2) / kVc2
            k2 = -k2 * k2
            k2 = kVa2 * math.exp(k2)

            k3 = ((math.log(Freq) / math.log(10)) - kVb3) / kVc3
            k3 = -k3 * k3
            k3 = kVa3 * math.exp(k3)

            k4 = ((math.log(Freq) / math.log(10)) - kVb4) / kVc4
            k4 = -k4 * k4
            k4 = kVa4 * math.exp(k4)

            log10k = k1 + k2 + k3 + k4 + (kVmk * math.log(Freq) / math.log(10)) + kVck
            kV = 10 ** log10k

            #aH

            a1 = ((math.log(Freq) / math.log(10)) - aHb1) / aHc1
            a1 = -a1 * a1
            a1 = aHa1 * math.exp(a1)

            a2 = ((math.log(Freq) / math.log(10)) - aHb2) / aHc2
            a2 = -a2 * a2
            a2 = aHa2 * math.exp(a2)

            a3 = ((math.log(Freq) / math.log(10)) - aHb3) / aHc3
            a3 = -a3 * a3
            a3 = aHa3 * math.exp(a3)

            a4 = ((math.log(Freq) / math.log(10)) - aHb4) / aHc4
            a4 = -a4 * a4
            a4 = aHa4 * math.exp(a4)

            a5 = ((math.log(Freq) / math.log(10)) - aHb5) / aHc5
            a5 = -a5 * a5
            a5 = aHa5 * math.exp(a5)

            aH = a1 + a2 + a3 + a4 + a5 + (aHma * math.log(Freq) / math.log(10)) + aHca

            #aV

            a1 = ((math.log(Freq) / math.log(10)) - aVb1) / aVc1
            a1 = -a1 * a1
            a1 = aVa1 * math.exp(a1)

            a2 = ((math.log(Freq) / math.log(10)) - aVb2) / aVc2
            a2 = -a2 * a2
            a2 = aVa2 * math.exp(a2)

            a3 = ((math.log(Freq) / math.log(10)) - aVb3) / aVc3
            a3 = -a3 * a3
            a3 = aVa3 * math.exp(a3)

            a4 = ((math.log(Freq) / math.log(10)) - aVb4) / aVc4
            a4 = -a4 * a4
            a4 = aVa4 * math.exp(a4)

            a5 = ((math.log(Freq) / math.log(10)) - aVb5) / aVc5
            a5 = -a5 * a5
            a5 = aVa5 * math.exp(a5)

            aV = a1 + a2 + a3 + a4 + a5 + (aVma * math.log(Freq) / math.log(10)) + aVca

            if Pol == "v":
                Pol = "V"
            if Pol == "h":
                Pol = "H"

            if Pol == "V":
                K = kV
            if Pol == "V":
                Alpha = aV
            if Pol == "H":
                K = kH
            if Pol == "H":
                Alpha = aH

            # # *************************************** Line 725
            # # Determine rain rate R

            # # ***************************************
            # # CRANE RAIN ATTENUATION MODEL

            # # Determine rain rate R for given fade margin and path length
            # L = PathLenKM
            # if PathLenKM > 22.5:
            #     L = 22.5
            # R = .001
            # Rstep = 20

            #rainRate()      # add return statements
            #####################################################################
            L = PathLenKM
            if PathLenKM > 22.5:
                L = 22.5
            R = 0.001
            Rstep = 20

            
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
            #####################################################################


            #RainOutage = outageTime()    # add more return statements (probably)
            #####################################################################
            while True:
                if R <= 0 or R > 550:
                    break
                curve_df = pd.read_csv(RRCurvesFolderPath + "/Curve" + str(Curve) + ".csv")
                curve_df = curve_df.iloc[7:]
                curve_df = curve_df.reset_index(drop=True)
                curve_df.columns = curve_df.iloc[0]
                curve_df = curve_df.iloc[1:]
                curve_df.columns = ['Rain Time', 'Unavailability', 'Rain Rate']

                MinutesOld = 0
                PerCentOld = 0
                RateOld = 0

                for i, row in curve_df.iterrows():
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

                #LogYvar = (math.log(Y1var) / math.log(10)) + (((math.log(Y2var / Y1var) / math.log(10)) / (X2var - X1var)) * (Xvar - X1var))
                #Yvar = math.pow(10, LogYvar)

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

            #####################################################################


            # ***************************************

            # Set the number of significant digits (# of decimals actually)

            # ***************************************

            FadeMargin = round(FadeMargin, 1)
            K = round(K, 6)
            Alpha = round(Alpha, 6)
            R = round(R, 1)
            TrialMargin = round(TrialMargin, 1)
            KRAlpha = round(KRAlpha, 3)
            PathEff = round(PathEff, 3)
            Pt2Path = round(Pt2Path, 3)
            if 'OutageMin' in globals():
                OutageMin = round(OutageMin, 1)
            OutageSec = round(OutageSec, 1)
            if 'OutagePerCent' in globals():
                OutagePerCent = round(OutagePerCent, 6)
            if 'Availability' in globals():
                Availability = round(Availability, 6)
            








            #####################################################################

            RainOutage = OutageSec

            #RainOutage = int((10 * RainOutage) + .5)
            #RainOutage = (RainOutage / 10)
            RainOutage = round(RainOutage, 1)

            # *************************************** Line 954

            TotalOutageSecs = MultiOutage + RainOutage

            if SpaceDiversity != "Y":
                print(Model + " Antenna= " + Antenna)
            if SpaceDiversity == "Y":
                print(Model + " Main Antenna= " + Antenna + " & SD Antenna= " + SDAntenna)

            Bandwidth = str(Bandwidth)

            if len(Bandwidth) == 1:
                Bandwidth = "   " + Bandwidth
            if len(Bandwidth) == 2:
                Bandwidth = "  " + Bandwidth
            if len(Bandwidth) == 3:
                Bandwidth = " " + Bandwidth

            Modulation = str(Modulation)

            if len(Modulation) == 1:
                Modulation = "    " + Modulation
            if len(Modulation) == 2:
                Modulation = "   " + Modulation
            if len(Modulation) == 3:
                Modulation = "  " + Modulation
            if len(Modulation) == 4:
                Modulation = " " + Modulation

            Capacity = str(Capacity)

            if len(Capacity) == 1:
                Capacity = "   " + Capacity
            if len(Capacity) == 2:
                Capacity = "  " + Capacity
            if len(Capacity) == 3:
                Capacity = " " + Capacity
            
            print(str(Site) + " Freq= " + str(Frequency) + " ChBW= " + str(Bandwidth) + " QAM= " + str(Modulation) + " Capacity= " + str(Capacity) + " TxOut= " + str(Power))

            Distance = str(Distance)

            if len(Distance) == 1:
                Distance = "   " + Distance
            if len(Distance) == 2:
                Distance = "  " + Distance
            if len(Distance) == 3:
                Distance = " " + Distance

            FadeMargin = str(FadeMargin)

            if len(FadeMargin) == 1:
                FadeMargin = " " + FadeMargin
                
            MultiOutage = str(MultiOutage)
            
            if len(MultiOutage) == 1:
                MultiOutage = "     " + MultiOutage
            if len(MultiOutage) == 2:
                MultiOutage = "    " + MultiOutage
            if len(MultiOutage) == 3:
                MultiOutage = "   " + MultiOutage
            if len(MultiOutage) == 4:
                MultiOutage = "  " + MultiOutage
            if len(MultiOutage) == 5:
                MultiOutage = " " + MultiOutage

            RainOutage = str(RainOutage)

            if len(RainOutage) == 1:
                RainOutage = "     " + RainOutage
            if len(RainOutage) == 2:
                RainOutage = "    " + RainOutage
            if len(RainOutage) == 3:
                RainOutage = "   " + RainOutage
            if len(RainOutage) == 4:
                RainOutage = "  " + RainOutage
            if len(RainOutage) == 5:
                RainOutage = " " + RainOutage

            TotalOutageSecs = str(TotalOutageSecs)

            if len(TotalOutageSecs) == 1:
                TotalOutageSecs = "     " + TotalOutageSecs
            if len(TotalOutageSecs) == 2:
                TotalOutageSecs = "    " + TotalOutageSecs
            if len(TotalOutageSecs) == 3:
                TotalOutageSecs = "   " + TotalOutageSecs
            if len(TotalOutageSecs) == 4:
                TotalOutageSecs = "  " + TotalOutageSecs
            if len(TotalOutageSecs) == 5:
                TotalOutageSecs = " " + TotalOutageSecs

            PrintFile = "City=" + str(Index) + " Freq=" + str(OperFreq) + " Dist=" + str(Distance) + " FM=" + str(FadeMargin) + " Multi=" + str(MultiOutage) + " Rain=" + str(RainOutage) + " Total=" + str(TotalOutageSecs)

            print(PrintFile)

           
            # update data

            # *************************************** Line 1052

            CheckDistance = Distance

            if Units == "mk":
                TheNumber = 1.60934 * CheckDistance

            TotalOutageSecs = float(TotalOutageSecs)

            DifCheck = abs(TotalOutageSecs - Seconds99)
            if DifCheck < DifSecs99:
                DifSecs99 = DifCheck
                Distance99 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds995)
            if DifCheck < DifSecs995:
                DifSecs995 = DifCheck
                Distance995 = CheckDistance
            
            
            DifCheck = abs(TotalOutageSecs - Seconds999)
            if DifCheck < DifSecs999:
                DifSecs999 = DifCheck
                Distance999 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds9995)
            if DifCheck < DifSecs9995:
                DifSecs9995 = DifCheck
                Distance9995 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds9999)
            if DifCheck < DifSecs9999:
                DifSecs9999 = DifCheck
                Distance9999 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds99995)
            if DifCheck < DifSecs99995:
                DifSecs99995 = DifCheck
                Distance99995 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds99999)
            if DifCheck < DifSecs99999:
                DifSecs99999 = DifCheck
                Distance99999 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds999995)
            if DifCheck < DifSecs999995:
                DifSecs999995 = DifCheck
                Distance999995 = CheckDistance

            DifCheck = abs(TotalOutageSecs - Seconds999999)
            if DifCheck < DifSecs999999:
                DifSecs999999 = DifCheck
                Distance999999 = CheckDistance

            # *************************************** Line 1121

            
            if FadeMargin < MinimumFadeMargin:
                if TotalOutageSecs > 320000:
                    break
                Distance99 = "-"
                if TotalOutageSecs > 160000:
                    break
                Distance995 = "-"
                if TotalOutageSecs > 32000:
                    break
                Distance999 = "-"
                if TotalOutageSecs > 16000:
                    break
                Distance9995 = "-"
                if TotalOutageSecs > 3200:
                    break
                Distance9999 = "-"
                if TotalOutageSecs > 1600:
                    break
                Distance99995 = "-"
                if TotalOutageSecs > 320:
                    break
                Distance99999 = "-"
                if TotalOutageSecs > 160:
                    break
                Distance999995 = "-"
                if TotalOutageSecs > 33:
                    break
                Distance999999 = "-"
            
            if TotalOutageSecs > 320000:
                break
            
            print("#############################J loop: " + str(J))
        print("################################JJ loop: " + str(JJ)) 
        #NEXT J& #################################### end loop scope??
       
        # *************************************** Line 1150

        if Model != OldModel and OldCounter == Counter:
            print()  #1, ""  # print blank line to file?
        OldModel = Model
        OldCounter = Counter

        PrintFile = str(Index) + "," + str(Zone) + "," + str(Site) + "," + str(State)
        print(PrintFile)
        # PrintFile = PrintFile + "," + Distance + "," + FreeSpaceLoss + "," + FadeMargin
        PrintFile = PrintFile + "," + str(Distance999999) + "," + str(Distance999995) + "," + str(Distance99999)
        PrintFile = PrintFile + "," + str(Distance99995) + "," + str(Distance9999) + "," + str(Distance9995)
        PrintFile = PrintFile + "," + str(Distance999) + "," + str(Distance995) + "," + str(Distance99)
        PrintFile = PrintFile + "," + str(Latitude) + "," + str(Longitude) + "," + str(ClimateFactor) + "," + str(Roughness) + "," + str(Temp)
        PrintFile = PrintFile + "," + str(Frequency) + "," + str(Polarization) + "," + str(Model) + "," + str(Antenna) + "," + str(Bandwidth)
        PrintFile = PrintFile + "," + str(Modulation) + "," + str(Capacity) + "," + str(Power) + "," + str(Threshold)
        PrintFile = PrintFile + "," + str(SystemGain) + "," + str(LinkBudget)
        PrintFile = PrintFile + '\n'

        output_df.write(PrintFile)
        
        # PRINT #1, PrintFile$ #### write to file here

        
        #if Counter == LineToStop: ## not defined??
            # break # exit JJ loop?
            
    # NEXT JJ&  ' Polarization # end loop scope?
    # LOOP  'Radios
# CLOSE #3

#PRINT #1, ",,Program,completed,normally." # print to file

print("")
print("Program terminated")
