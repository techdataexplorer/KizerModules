import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd
import math


################################################# PyQT GUI Class ###################################################
# Based on code from https://pythonspot.com/pyqt5-file-dialog/

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

    def openFolderNameDialog(self, folderPrompt):
        folderName = QFileDialog.getExistingDirectory(self, folderPrompt)
        if folderName:
            return folderName

################################################# PyQT GUI Class ###################################################

# Create PyQT Object
app = QApplication(sys.argv)
ex = App()

# Get local machine's path for Profiles folder
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS3 Folder")
FolderPath = ExampleS3FolderPath + "/Profiles"

NumberOfProfiles = 6

for counter in range(1, NumberOfProfiles+1):
    ProfileNumber = str(counter)

    if counter < 100000:
        ProfileNumber = "0" + ProfileNumber

    if counter < 10000:
        ProfileNumber = "0" + ProfileNumber

    if counter < 1000:
        ProfileNumber = "0" + ProfileNumber

    if counter < 100:
        ProfileNumber = "0" + ProfileNumber

    if counter < 10:
        ProfileNumber = "0" + ProfileNumber

    TheProfile = "/P" + ProfileNumber + ".CSV"
    TheRoughness = "/Roughness" + ProfileNumber + ".CSV"

    roughness_df = open(FolderPath  + TheRoughness, "w+")
    profile_df = pd.read_csv(FolderPath  + TheProfile, header=None)
    
    latitude = profile_df.iloc[:, 0].tolist()
    longitude = profile_df.iloc[:, 1].tolist()
    height = profile_df.iloc[:, 2].tolist()

    MaxLoopCounter = len(profile_df)
    LoopCounter = 0
    CumulativeSum = 0.0
    SqCumulativeSum = 0.0

    for h in height:
        LoopCounter += 1
        if 1 < LoopCounter < MaxLoopCounter:
            CumulativeSum += h
            SqCumulativeSum += (h*h)

    hlower = min(height[0], height[len(height)-1])

    Average = CumulativeSum / (MaxLoopCounter - 2)
    SqAverage = SqCumulativeSum / (MaxLoopCounter - 2)
    AverageSq = (Average * Average)
    Roughness = SqAverage - AverageSq
    Roughness = math.pow(Roughness, 0.5)
    # print(Roughness)

    if Roughness > 140:
        Roughness = 140
    if Roughness < 20:
        Roughness = 20

    print(str(Roughness) + "," + str(hlower))

    roughness_df.write(str(Roughness) + "," + str(hlower) + "\n")

print("Press Enter To Exit.")
input()

