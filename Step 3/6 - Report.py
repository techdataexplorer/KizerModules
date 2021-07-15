import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd

def generateReport(ExampleS3FilePath):

    # Create file paths using main folder path
    PathsFilePath = ExampleS3FolderPath + "/Paths.csv"
    Pass2FilePath = ExampleS3FolderPath + "/Data/PathDataPass2.csv"
    Pass3FilePath = ExampleS3FolderPath + "/Data/PathDataPass3.csv"
    ReportFilePath = ExampleS3FolderPath + "/Data/Report.txt"

    # Open dataframes for each file
    path_data_paths_df = pd.read_csv(PathsFilePath)     # open dataframe for file called "Paths"
    path_data_pass_2_df = pd.read_csv(Pass2FilePath)    # open dataframe for file called "PathDataPass2"
    path_data_pass_3_df = pd.read_csv(Pass3FilePath)    # open dataframe for file called "PathDataPass3"
    report = open(ReportFilePath, "w")                  # open text file for output called "Report"

    NUMBER_OF_PATHS = path_data_paths_df.shape[0]       # number of paths is equal to the number of rows in "Paths" file

    # This loop iterates through each row of files called Paths, PathDataPass2, and PathDataPass3
    # All 3 files have the same number of rows which == NUMBER_OF_PATHS
    for index in range(0, NUMBER_OF_PATHS):

        PathsRow = path_data_paths_df.iloc[index]       # entire row of "Paths.csv"

        # Split row into variables for legibility 
        PathIndex = PathsRow[0]
        Site1 = PathsRow[1]
        Latitude1 = PathsRow[2]
        Longitude1 = PathsRow[3]
        Site2 = PathsRow[4]
        Latitude2 = PathsRow[5]
        Longitude2 = PathsRow[6]

        Pass2Row = path_data_pass_2_df.iloc[index]      # entire row of "PathDataPass2"
        
        # Split row into variables for legibility 
        RadioCompany = Pass2Row[1]
        RadioModel = Pass2Row[2]
        AltRadioModel = Pass2Row[3]
        Freq = Pass2Row[4]
        Polarization = Pass2Row[5]
        ChannelBW = Pass2Row[6]
        DataRate = Pass2Row[7]
        
        Modulation = Pass2Row[8]
        Threshold = Pass2Row[9]
        ACMOffset = Pass2Row[10]
        DFM = Pass2Row[11]
        TXPwr = Pass2Row[12]
        TXCoupling = Pass2Row[13]
        RXCoupling = Pass2Row[14]

        LeftAntennaModel = Pass2Row[15]
        LeftAntennaGain = Pass2Row[16]
        LeftSDAntenna = Pass2Row[17]
        LeftSDAntennaGain = Pass2Row[18]
        LeftSDSpacing = Pass2Row[19]

        RightAntennaModel = Pass2Row[20]
        RightAntennaGain = Pass2Row[21]
        RightSDAntenna = Pass2Row[22]
        RightSDAntennaGain = Pass2Row[23]
        RightSDSpacing = Pass2Row[24]

        LeftWaveguide = Pass2Row[25]
        LeftWGLength = Pass2Row[26]
        LeftWGAttn = Pass2Row[27]
        RightWaveguide = Pass2Row[28]
        RightWGLength = Pass2Row[29]
        RightWGAttn = Pass2Row[30]

        FreeSpaceLoss = Pass2Row[31]
        AtmosphericAtten = Pass2Row[32]
        MiscLoss = Pass2Row[33]
        FieldMargin = Pass2Row[34]
        RelDispersion = Pass2Row[35]
        NotchWidth = Pass2Row[36]
        NotchDepth = Pass2Row[37]
        LeftAntHt = Pass2Row[38]
        RightAntHt = Pass2Row[39]

        Pass3Row = path_data_pass_3_df.iloc[index]      # entire row of "PathDataPass3"

        # Split row into variables for legibility 
        # Many of the following variables were already assinged from PathDataPass2
        # These can most likely be removed, however this is how the orginal algorithm does it
        PathIndex12 = Pass3Row[0]
        TXPwr = Pass3Row[1]                 # Double assignment 
        TXCoupling = Pass3Row[2]            # Double assignment 
        LeftAntennaGain = Pass3Row[3]       # Double assignment 
        LeftWGAttn = Pass3Row[4]            # Double assignment 
        FreeSpaceLoss = Pass3Row[5]         # Double assignment 
        AtmosphericAtten = Pass3Row[6]      # Double assignment 

        RightAntennaGain = Pass3Row[7]      # Double assignment 
        RightWGAttn = Pass3Row[8]           # Double assignment 
        Threshold = Pass3Row[9]             # Double assignment 
        RXCoupling = Pass3Row[10]           # Double assignment 
        MiscLoss = Pass3Row[11]             # Double assignment 
        FieldMargin = Pass3Row[12]          # Double assignment 

        FadeMargin = Pass3Row[13]
        Distance = Pass3Row[14]
        Gfreq = Pass3Row[15]
        VBTotalFFSecs = Pass3Row[16]
        VBTotalDFSecs = Pass3Row[17]
        VBTotalMultipathSecs = Pass3Row[18]
        CraneTotalRainSecs = Pass3Row[19]

        ITURTotalFFSecs = Pass3Row[20]
        ITURTotalDFSecs = Pass3Row[21]
        ITURTotalMultipathSecs = Pass3Row[22]
        ITURRainOutageSecs = Pass3Row[23]

        if Polarization == "V":
            Polarization = "Vertical Polarization"
        elif Polarization == "H":
            Polarization = "Vertical Polarization"

        LeftEIRP = TXPwr - TXCoupling + LeftAntennaGain - LeftWGAttn
        RightEIRP = TXPwr - TXCoupling + RightAntennaGain - RightWGAttn
        RSL = TXPwr - TXCoupling + LeftAntennaGain - LeftWGAttn - FreeSpaceLoss - AtmosphericAtten - \
            FieldMargin - MiscLoss + RightAntennaGain - RightWGAttn - RXCoupling

        # I think this section can be removed
        RainFlag = 0
        if ITURRainOutageSecs == "> 315,576":
            RainFlag = 1
        if ITURRainOutageSecs == "< 316":
            RainFlag = 1
        if ITURRainOutageSecs == "---":
            RainFlag = 1
        
        NAOutageSecs = VBTotalMultipathSecs + CraneTotalRainSecs
        ITUROutageSecs = ITURTotalMultipathSecs

        RainFlag = 0
        if ITURRainOutageSecs == "> 315,576": 
            RainFlag = 1
        if ITURRainOutageSecs == "< 316":
            RainFlag = 1
        if ITURRainOutageSecs == "---":
            RainFlag == 1
        if RainFlag == 0:
            ITUROutageSecs = ITUROutageSecs + float(ITURRainOutageSecs)

        Tsmonth = ((365.25 / 12) * 24 * 60 * 60)        # Seconds in a month
        Tsyear = (365.25 * 24 * 60 * 60)                # Seconds in a year

        NAavailability = 100 * (1 - (NAOutageSecs / Tsyear))

        ITURavailability = 100 * (1 - (ITUROutageSecs / Tsyear))

        #report.write( + "\n")
        # Create report
        report.write("Path: " + str(PathIndex) + "\n\n")
        report.write("Site 1: " + str(Site1) + "     ,     Site2: " + str(Site2) + "\n")
        report.write("Latitude 1: " + str(Latitude1) + "     ,     " + "Latitude 2: " + str(Latitude2) + "\n")
        report.write("Longitude 1: " + str(Longitude1) + "     ,     " + "Longitude 2: " + str(Longitude2) + "\n")
        report.write("Distance (miles): " + str(round(Distance, 1)) + "\n")

        report.write("Frequency (MHz): " + str(Freq) + "\n")
        report.write(str(Polarization) + "\n")
        report.write("Radio: " + str(RadioCompany) + "\n")
        report.write(str(RadioModel) + "\n")
        report.write(str(AltRadioModel.lstrip()) + "\n")
        
        report.write("Modulation (QAM): " + str(Modulation) + "\n")
        report.write("Bandwidth (MHz): " + str(ChannelBW) + "\n")
        report.write("Data Rate (Mb/s): " + str(DataRate) + "\n")
        report.write("TX Power (dBm): " + str(TXPwr) + "\n")
        report.write("RX Threshold (dBm): " + str(Threshold) + "\n")

        report.write("Antenna: " + str(LeftAntennaModel) + "," + str(RightAntennaModel) + "\n")
        report.write("Gain (dBi): " + str(LeftAntennaGain) + "," + str(RightAntennaGain) + "\n")

        if not (LeftSDAntenna != LeftSDAntenna or RightSDAntenna != RightSDAntenna):
            report.write("SD Antenna: " + str(LeftSDAntenna) + "," + str(RightSDAntenna) + "\n")
            report.write("SD Gain (dBi): " + str(LeftSDAntennaGain) + "," + str(RightSDAntennaGain) + "\n")
            report.write("Spacing (ft): " + str(LeftSDSpacing) + "," + str(RightSDSpacing) + "\n")

        if not (LeftWaveguide != LeftWaveguide or RightWaveguide != RightWaveguide):
            report.write("Waveguide: " + str(LeftWaveguide) + "," + str(RightWaveguide) + "\n")
            report.write("Length (ft): " + str(LeftWGLength) + "," + str(RightWGLength) + "\n")
            report.write("Attenuation (dB): " + str(LeftWGAttn) + "," + str(RightWGAttn) + "\n")

        report.write("TX Coupling Loss (dB): " + str(TXCoupling) + "\n")
        report.write("EIRP (dBm): " + str(LeftEIRP) + "," + str(RightEIRP) + "\n")
        report.write("RX Coupling Loss (dB): " + str(RXCoupling) + "\n")
        report.write("Field Margin (dB): " + str(FieldMargin) + "\n")
        report.write("Misc. Losses (dB): " + str(MiscLoss) + "\n")

        report.write("Free Space Loss (dB): " + str(round(FreeSpaceLoss)) + "\n")
        report.write("Atmospheric Absorption (dB): " + str(round(AtmosphericAtten, 1)) + "\n")
        report.write("Received Signal Level (dBm): " + str(round(RSL, 1)) + "\n")
        report.write("Flat Fade Margin (dB): " + str(round(FadeMargin, 1)) + "\n")
        report.write("Dispersive Fade Margin (dB): " + str(DFM) + "\n")

        report.write("Relative Dispersion Factor (multiplicative): " + str(round(RelDispersion)) + "\n\n")
        report.write("North American Methodology" + "\n")
        report.write("Annual two-way Flat Fading Multipath Outage Seconds: " + str(round(VBTotalFFSecs, 1)) + "\n")
        report.write("Annual two-way Dispersive Multipath Outage Seconds: " + str(round(VBTotalDFSecs, 1)) + "\n")
        report.write("Annual two-way Rain Outage Seconds: " + str(round(CraneTotalRainSecs)) + "\n")

        report.write("Annual (two-way) Availability (Vigants-Barnett & Crane): " + str(round(NAavailability, 5)) + " %" + "\n\n")
        report.write("ITU-R Methodology" + "\n")
        report.write("Annual two-way Flat Fading Multipath Outage Seconds: " + str(round(ITURTotalFFSecs, 1)) + "\n")
        report.write("Annual two-way Dispersive Multipath Outage Seconds: " + str(round(ITURTotalDFSecs, 1)) + "\n")

        if (ITURRainOutageSecs == "> 315,576" or ITURRainOutageSecs == "< 316" or ITURRainOutageSecs == "---"):
            report.write("Annual two-way Rain Outage Seconds: " + str(ITURRainOutageSecs) + "\n")
        else:
            report.write("Annual two-way Rain Outage Seconds: " + str(round(float(ITURRainOutageSecs), 1)) + "\n")

        report.write("Annual (two-way) Availability (ITU-R Rec P.530-17): " + str(round(ITURavailability, 5)) + " %" + "\n")
        report.write("-------------------------------------------------------------------------" + "\n")

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
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS3 Folder")

generateReport(ExampleS3FolderPath)

print("View the report in report.txt")
print("Press enter to exit.")
input()