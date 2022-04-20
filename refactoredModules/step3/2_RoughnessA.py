from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd
import math
import sys

class RoughnessA(object):

    def __init__(self):
        self.FolderPath = ""
        self.NumberOfProfiles = float("inf")

    def setFolderPath(self, folderPath):
        self.FolderPath = str(folderPath)

    def setNumberOfProfiles(self, numOfProfiles):
        self.NumberOfProfiles = int(numOfProfiles)

    def execute(self):
        # Get local machine's path for Profiles folder
        self.FolderPath = self.FolderPath + "/Profiles"

        for counter in range(1, self.NumberOfProfiles+1):
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

            roughness_df = open(self.FolderPath  + TheRoughness, "w+")
            profile_df = pd.read_csv(self.FolderPath  + TheProfile, header=None)
            
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


test = RoughnessA()
ExampleS3FolderPath = ex.openFolderNameDialog("Find ExampleS3 Folder")
#test.setFolderPath("C:/Users/ecuth/Desktop/Spatial Datalyst/Kizer/Path Design 11 April 2021/Step 3 Path Availability/ExampleStep3")
test.setFolderPath(ExampleS3FolderPath)
#test.setNumberOfProfiles(6)
test.setNumberOfProfiles(numOfProfiles=input("Enter number of profiles: "))
test.execute()
input("Press Enter to exit")