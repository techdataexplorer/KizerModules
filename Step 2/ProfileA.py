import os
import sys
from profileAUI import Ui_ProfileA_Window, QGoogleMap
import PyQt5
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import pandas as pd
import time


# reads the input file and appends certain lines when the internal variable counter reaches set values.
# TODO investigate the origins and meanings of set values

class Worker(QObject):
    
    def __init__(self, FolderPath):
        super().__init__()
        self.FolderPath = FolderPath
    
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self):
        print("Reading <Criteria.ini> initialization file.\n")


        Criteria = (self.FolderPath + "\Criteria.ini")

        #Initialization subroutine
        Answers = self.initializeSubroutine(Criteria)  # 9000

        FeetMeters = Answers[3]

        if (FeetMeters == "f"):
            FeetMeters = "F"
        elif (FeetMeters == "m"):
            FeetMeters = "M"
        if (FeetMeters == "F" or FeetMeters == "M"):
            pass
        else:
            print("Fourth line of <Criteria.ini> not understood.")
            print("Line should be F or M.")
            print(" Program; Terminated.")
            endProgram()  # 9999

        Status = (FolderPath + "\TempFile\Status.CSV")
        #move file into s2a
        #open file, read file, close file

        StatusDF = pd.read_csv(Status, header=None)
        counter = 0
        for index, row in StatusDF.iterrows():

            Question = row[0]
            YNAnswer = row[1]
            if (counter == 0):
                SysOpt = YNAnswer
            elif(counter == 1):
                SysFail = YNAnswer
            elif(counter == 2):
                SysPass = YNAnswer

            counter += 1


        if(SysOpt == "Y"):
            print("\nCreating Optimized path profiles\n")

            InFolder = FolderPath + "\Optimize"
            OutFolder = FolderPath + "\ProfOpt"
            InputFolder = InFolder + "\PATHINFO.CSV"
            self.createProfile(InputFolder, OutFolder, InFolder, FeetMeters)
            
            self.progress.emit(2)

        if(SysFail == "Y"):
            print("\nCreating Failed path profiles\n")

            InFolder = FolderPath + "\Failed"
            OutFolder = FolderPath + "\ProfFail"
            InputFolder = InFolder + "\PATHINFO.CSV"

            self.createProfile(InputFolder, OutFolder, InFolder, FeetMeters)

            self.progress.emit(3)

        if(SysPass == "Y"):
            print("\nCreating Passed path profiles\n")

            InFolder = FolderPath + "\Passed"
            OutFolder = FolderPath + "\ProfPass"
            InputFolder = InFolder + "\PATHINFO.CSV"
            self.createProfile(InputFolder, OutFolder, InFolder, FeetMeters)
            
            self.progress.emit(4)
            
        self.finished.emit()


    def initializeSubroutine(self, Criteria):  # 9000

        inpFile = open(Criteria, "r")

        Answers = []
        counter = 0

        for line in inpFile:
            currentline = line.split(",")
            if (counter == 6 or counter == 22):
                counter += 1
                continue

            if (counter == 7):
                Answers.append(currentline[1])
                counter += 1
                continue

            Answers.append(currentline[0])

            if(counter >= 8 and counter <= 13):
                Answers.append(currentline[1])
                counter += 1

            counter += 1

        inpFile.close()
        Answers.append(1000)  # MaxDist1

        return Answers

    def createProfile(self, InputFolder, OutFolder, InFolder, FeetMeters):  # 900
        CleanUpScript = (OutFolder + "\CleanUp.CMD")
        CleanUpScriptFile = open(CleanUpScript, "w")

        PrintScript = (OutFolder + "\Plot.CMD")
        PrintScriptOutput = open(PrintScript, "w")
        PrintScriptOutput.write("@echo off\n")
        PrintScriptOutput.write("CD " + OutFolder + "\n")

        input_df = pd.read_csv(InputFolder)
        for index, row in input_df.iterrows():

            PathIndex = int(row[0])
            Site1 = str(row[1])
            Lat1 = float(row[2])
            Long1 = float(row[3])
            Site2 = str(row[4])
            Lat2 = float(row[5])
            Long2 = float(row[6])
            TowerHeight1 = float(row[7])
            TowerHeight2 = float(row[8])
            AntennaHeight1 = float(row[9])
            AntennaHeight2 = float(row[10])
            PathDistance = float(row[11])
            OpFrequency = float(row[12])

            print(str(PathIndex) + "   " + Site1 + "   " + Site2)
            PathNumber = int(PathIndex)
            ProfileNumber = PathNumber

            #not sure what this is for
            if(ProfileNumber < 10):
                ProfileNumber = "00000" + str(ProfileNumber)
            elif(ProfileNumber < 100):
                ProfileNumber = "0000" + str(ProfileNumber)
            elif(ProfileNumber < 1000):
                ProfileNumber = "000" + str(ProfileNumber)
            elif(ProfileNumber < 10000):
                ProfileNumber = "00" + str(ProfileNumber)
            elif(ProfileNumber < 100000):
                ProfileNumber = "0" + str(ProfileNumber)

            PrintScriptOutput.write(
                OutFolder + "\Plotter\\" + "pgnuplot.exe SC" + str(ProfileNumber) + ".gp\n")

            Flag2 = self.createScripts(InFolder, OutFolder, ProfileNumber, CleanUpScriptFile, TowerHeight1,
                                TowerHeight2, AntennaHeight1, AntennaHeight2, PathDistance, Site1, Site2, FeetMeters)  # Create scripts

            self.createDataFiles(InFolder, OutFolder, ProfileNumber,
                            CleanUpScriptFile, Flag2, AntennaHeight1)  # Create data files

        return

    def createScripts(self, InFolder, OutFolder, ProfileNumber, CleanUpScriptFile, TowerHeight1, TowerHeight2, AntennaHeight1, AntennaHeight2, PathDistance, Site1, Site2, FeetMeters):  # 1000
        MainScript = OutFolder + "\SC" + str(ProfileNumber) + ".gp"
        CleanUpScriptFile.write("DEL " + MainScript + "\n")

        MainScriptFile = open(MainScript, "w")
        InFolderFile = (InFolder + "\EV" + str(ProfileNumber) + ".CSV")

        input_df = pd.read_csv(InFolderFile)  # 66

        for index1, row1 in input_df.iterrows():

            AAAA = float(row1[0])
            AAAB = float(row1[1])
            AAAC = float(row1[2])
            AAAD = float(row1[3])
            AAAE = float(row1[4])
            AAAF = float(row1[5])
            AAAG = float(row1[6])
            break

        del input_df
        Flag2 = 0
        if (abs(AAAD) > 1):
            Flag2 = 1  # The second criterions are being evaluated
        MainScriptFile.write("set grid\n")

        #Set Y range
        Max = 0
        Min = 999999
        TheCounter = 0

        input_df = pd.read_csv(InFolderFile)  # 31

        for index2, row2 in input_df.iterrows():
            TheCounter += 1

            Dist1 = float(row2[0])
            T0 = float(row2[1])
            T1 = float(row2[2])
            T2 = float(row2[3])
            P0 = float(row2[4])
            P1 = float(row2[5])
            P2 = float(row2[6])

            Test = float(T0) + float(TowerHeight1) - float(AntennaHeight1)
            if(TheCounter == 1 and Test > Max):
                Max = Test

            Test = float(T0) + float(TowerHeight2) - float(AntennaHeight2)
            EndOfFile = (index2 == input_df.index[-1])
            if(EndOfFile and Test > Max):
                Max = Test

            if (float(T0) > Max):
                Max = float(T0)
            if (float(T1) > Max):
                Max = float(T1)
            if (float(P0) > Max):
                Max = float(P0)
            if (float(P1) > Max):
                Max = float(P1)
            if (float(T0) < Min):
                Min = float(T0)
            if (float(T1) < Min):
                Min = float(T1)
            if (float(P0) < Min):
                Min = float(P0)
            if (float(P1) < Min):
                Min = float(P1)
            #this might be wrong
            if(Flag2 == 1):
                if(float(T2) > Max):
                    Max = float(T2)
                if(float(P2) > Max):
                    Max = float(P2)
                if(float(T2) < Min):
                    Max = float(T2)
                if(float(P2) < Min):
                    Max = float(P2)
        del input_df

        InFolderFile2 = (InFolder + "\PR" + str(ProfileNumber) + ".CSV")

        input_df = pd.read_csv(InFolderFile2)  # 31

        for index3, row3 in input_df.iterrows():

            Dist1 = float(row3[0])
            T0 = float(row3[1])
            T1 = float(row3[2])
            T2 = str(row3[3])
            P0 = str(row3[4])

            if(float(T0) > Max):
                Max = float(T0)
            if(float(T0) < Min):
                Min = float(T0)

        del input_df
        Max = int((Max / 10) + 1)
        Min = int(Min / 10)
        Max = 10 * Max
        Min = 10 * Min

        Max = str(Max)
        Min = str(Min)

        MainScriptFile.write("set yrange[" + Min + " to " + Max + "]\n")

        #Set X range
        Increment = float(PathDistance) / 50
        LeftPoint = Increment
        RightPoint = float(PathDistance) + Increment
        LeftPoint = int((LeftPoint * 10000) + .5)
        LeftPoint = LeftPoint / 10000
        RightPoint = int((RightPoint * 10000) + .5)
        RightPoint = RightPoint / 10000
        MainScriptFile.write(
            "set xrange [-{} to {}]\n".format(LeftPoint, RightPoint))

        MainScriptFile.write("set encoding iso_8859_1\n")
        MainScriptFile.write("set term png\n")
        MainScriptFile.write("set nokey\n")
        MainScriptFile.write("set title 'Path Profile {}'\n".format(ProfileNumber))

        LenS1 = len(Site1)
        LenS2 = len(Site2)
        TheSite1 = Site1
        TheSite2 = Site2
        if(LenS1 > 20):
            TheSite1 = Site1[1-20: 1]
        if(LenS2 > 20):
            TheSite2 = Site2[1-20: 1]
        if(LenS1 > 20):
            LenS1 = 20
        if(LenS2 > 20):
            LenS2 = 20

        PathDistance = int((float(PathDistance) * 100) + .5)
        PathDistance = PathDistance / 100
        DistLabel = "Path Distance = " + str(PathDistance)
        if(FeetMeters == "F"):
            DistLabel = DistLabel + " miles"
        if(FeetMeters == "M"):
            DistLabel = DistLabel + " km"
        LenDist = len(DistLabel)
        Delta = 80 - LenS1 - LenS2 - LenDist
        Delta = Delta / 2
        Delta = int(Delta)
        Adder = ""
        if(Delta > 0):
            for i in range(Delta):
                Adder = Adder + " "
        BottomLabel = TheSite1 + Adder + DistLabel + Adder + TheSite2
        MainScriptFile.write("set xlabel '" + BottomLabel + "'\n")
        if(FeetMeters == "F"):
            LeftLabel = "Elevation (AMSL, feet)"
        if(FeetMeters == "M"):
            LeftLabel = "Elevation (AMSL, meters)"
        MainScriptFile.write("set ylabel '" + LeftLabel + "'\n")
        MainScriptFile.write("set output 'PR" + ProfileNumber + ".png'\n")

        #Place arrows ---------------------
        EVFileName = (InFolder + "\EV" + ProfileNumber + ".CSV")  # 31
        PRFileName = (InFolder + "\PR" + ProfileNumber + ".CSV")  # 32
        LocationCounter = 0

        ev_df = pd.read_csv(EVFileName)  # 31
        pr_df = pd.read_csv(PRFileName)  # 32

        ev_length = ev_df.shape[0]
        for index3 in range(0, ev_length):
            LocationCounter = LocationCounter + 1

            evRow = ev_df.iloc[index3]  # 31
            Dist1 = float(evRow[0])
            T0 = float(evRow[1])
            T1 = float(evRow[2])
            T2 = float(evRow[3])
            P0 = float(evRow[4])
            P1 = float(evRow[5])
            P2 = float(evRow[6])

            prRow = pr_df.iloc[index3]  # 32
            Dist2 = float(prRow[0])
            Elev = float(prRow[1])
            ObHt = float(prRow[2])
            ObCode = str(prRow[3])
            ObType = str(prRow[4])

            if(abs(Elev) < .1):
                Elev = 0
            Elev = str(Elev)

            if(LocationCounter == 1):
                Elev2 = float(Elev) + float(TowerHeight1)
                Elev2 = str(Elev2)

                MainScriptFile.write("set arrow nohead from " + str(Dist2) +
                                    "," + str(Elev) + " to " + str(Dist2) + "," + Elev2 + "\n")
                continue

            if(ObCode == "B"):
                Delta1 = float(T1) - float(T0)
                Delta2 = float(T2) - float(T0)
                Ht0Down = float(Elev)
                Ht0Up = Ht0Down + float(ObHt)
                Ht1Down = Ht0Down + Delta1
                Ht1Up = Ht1Down + float(ObHt)
                Ht2Down = Ht0Down + Delta2
                Ht2Up = Ht2Down + float(ObHt)

                if(abs(Ht0Down) < .1):
                    Ht0Down = 0
                if(abs(Ht0Up) < .1):
                    Ht0Up = 0
                if(abs(Ht1Down) < .1):
                    Ht1Down = 0
                if(abs(Ht1Up) < .1):
                    Ht1Up = 0
                if(abs(Ht2Down) < .1):
                    Ht2Down = 0
                if(abs(Ht2Up) < .1):
                    Ht2Up = 0

                Ht0Down = str(Ht0Down)
                Ht0Up = str(Ht0Up)
                Ht1Down = str(Ht1Down)
                Ht1Up = str(Ht1Up)
                Ht2Down = str(Ht2Down)
                Ht2Up = str(Ht2Up)

                MainScriptFile.write("set arrow nohead from " + str(Dist2) +
                                    "," + Ht0Down + " to " + str(Dist2) + "," + Ht0Up + "\n")
                MainScriptFile.write("set arrow nohead from " + str(Dist2) +
                                    "," + Ht1Down + " to " + str(Dist2) + "," + Ht1Up + "\n")

                if(Flag2 == 1):
                    MainScriptFile.write("set arrow nohead from " + str(Dist2) +
                                        "," + Ht2Down + " to " + str(Dist2) + "," + Ht2Up + "\n")

            if(ObCode == "T"):
                Delta1 = float(T1) - float(T0)
                Delta2 = float(T2) - float(T0)

                Ht0Down = float(Elev)
                Ht0Up = Ht0Down + float(ObHt)
                Ht1Down = Ht0Down + Delta1
                Ht1Up = Ht1Down + float(ObHt)
                Ht2Down = Ht0Down + Delta2
                Ht2Up = Ht2Down + float(ObHt)

                if(abs(Ht0Down) < .1):
                    Ht0Down = 0
                if(abs(Ht0Up) < .1):
                    Ht0Up = 0
                if(abs(Ht1Down) < .1):
                    Ht1Down = 0
                if(abs(Ht1Up) < .1):
                    Ht1Up = 0
                if(abs(Ht2Down) < .1):
                    Ht2Down = 0
                if(abs(Ht2Up) < .1):
                    Ht2Up = 0

                Ht0Down = str(Ht0Down)
                Ht0Up = str(Ht0Up)
                Ht1Down = str(Ht1Down)
                Ht1Up = str(Ht1Up)
                Ht2Down = str(Ht2Down)
                Ht2Up = str(Ht2Up)

                MainScriptFile.write("set arrow head from " + str(Dist2) +
                                    "," + Ht0Down + " to " + str(Dist2) + "," + Ht0Up + "\n")
                MainScriptFile.write("set arrow head from " + str(Dist2) +
                                    "," + Ht1Down + " to " + str(Dist2) + "," + Ht1Up + "\n")

                if(Flag2 == 1):
                    MainScriptFile.write("set arrow head from " + str(Dist2) +
                                        "," + Ht2Down + " to " + str(Dist2) + "," + Ht2Up + "\n")

        del ev_df
        del pr_df
        Elev2 = float(Elev) + float(TowerHeight2)
        Elev2 = str(Elev2)
        MainScriptFile.write("set arrow nohead from " + str(Dist2) +
                            "," + Elev + " to " + str(Dist2) + "," + Elev2 + "\n")

        #----------------------------------------

        PrintLine = "plot "
        PrintLine = (PrintLine + "'T0" + ProfileNumber + ".gp' with lines,")
        PrintLine = (PrintLine + "'T1" + ProfileNumber + ".gp' with lines,")
        if(Flag2 == 1):
            PrintLine = (PrintLine + "'T2" + ProfileNumber + ".gp' with lines,")
        PrintLine = (PrintLine + "'P0" + ProfileNumber + ".gp' with lines,")
        PrintLine = (PrintLine + "'P1" + ProfileNumber + ".gp' with lines")
        if(Flag2 == 1):
            PrintLine = PrintLine + ",'P2" + ProfileNumber + ".gp' with lines"
        MainScriptFile.write(PrintLine)

        MainScriptFile.close()

        #Update the cleanup script
        TPScript = (OutFolder + "\T0" + ProfileNumber + ".gp")
        CleanUpScriptFile.write("DEL " + TPScript + "\n")
        TPScript = (OutFolder + "\T1" + ProfileNumber + ".gp")
        CleanUpScriptFile.write("DEL " + TPScript + "\n")
        TPScript = (OutFolder + "\T2" + ProfileNumber + ".gp")
        if(Flag2 == 1):
            CleanUpScriptFile.write("DEL " + TPScript + "\n")
        TPScript = (OutFolder + "\P0" + ProfileNumber + ".gp")
        CleanUpScriptFile.write("DEL " + TPScript + "\n")
        TPScript = (OutFolder + "\P1" + ProfileNumber + ".gp")
        CleanUpScriptFile.write("DEL " + TPScript + "\n")
        TPScript = (OutFolder + "\P2" + ProfileNumber + ".gp")
        if(Flag2 == 1):
            CleanUpScriptFile.write("DEL " + TPScript + "\n")

        return Flag2

    def createDataFiles(self, InFolder, OutFolder, ProfileNumber, CleanUpScriptFile, Flag2, AntennaHeight1):  # 2000

        Tdata0 = OutFolder + "\T0" + ProfileNumber + ".gp"
        Tdata1 = OutFolder + "\T1" + ProfileNumber + ".gp"
        Tdata2 = OutFolder + "\T2" + ProfileNumber + ".gp"
        Pdata0 = OutFolder + "\P0" + ProfileNumber + ".gp"
        Pdata1 = OutFolder + "\P1" + ProfileNumber + ".gp"
        Pdata2 = OutFolder + "\P2" + ProfileNumber + ".gp"

        Tdata0File = open(Tdata0, "w")  # 21
        Tdata1File = open(Tdata1, "w")  # 22
        if(Flag2 == 1):
            Tdata2File = open(Tdata2, "w")  # 23
        Pdata0File = open(Pdata0, "w")  # 24
        Pdata1File = open(Pdata1, "w")  # 25
        if(Flag2 == 1):
            Pdata2File = open(Pdata2, "w")  # 26

        CleanUpScriptFile.write("DEL " + Tdata0 + "\n")
        CleanUpScriptFile.write("DEL " + Tdata1 + "\n")
        if(Flag2 == 1):
            CleanUpScriptFile.write("DEL " + Tdata2 + "\n")
        CleanUpScriptFile.write("DEL " + Pdata0 + "\n")
        CleanUpScriptFile.write("DEL " + Pdata1 + "\n")
        if(Flag2 == 1):
            CleanUpScriptFile.write("DEL " + Pdata2 + "\n")

        EVFileName = (InFolder + "\EV" + ProfileNumber + ".CSV")  # 31
        PRFileName = (InFolder + "\PR" + ProfileNumber + ".CSV")  # 32
        LocationCounter = 0

        ev_df = pd.read_csv(EVFileName)  # 31
        pr_df = pd.read_csv(PRFileName)  # 32

        ev_length = ev_df.shape[0]
        for index3 in range(0, ev_length):
            LocationCounter = LocationCounter + 1

            evRow = ev_df.iloc[index3]  # 31
            Dist1 = float(evRow[0])
            T0 = float(evRow[1])
            T1 = float(evRow[2])
            T2 = float(evRow[3])
            P0 = float(evRow[4])
            P1 = float(evRow[5])
            P2 = float(evRow[6])

            prRow = pr_df.iloc[index3]  # 32
            Dist2 = float(prRow[0])
            Elev = float(prRow[1])
            ObHt = float(prRow[2])
            ObCode = str(prRow[3])
            ObType = str(prRow[4])

            if(abs(T0) < .1):
                T0 = 0
            if(abs(T1) < .1):
                T1 = 0
            if(abs(T2) < .1):
                T2 = 0
            if(abs(P0) < .1):
                P0 = 0
            if(abs(P1) < .1):
                P1 = 0
            if(abs(P2) < .1):
                P2 = 0
            if(abs(Elev) < .1):
                Elev = 0

            T0 = str(T0)
            T1 = str(T1)
            T2 = str(T2)
            P0 = str(P0)
            P1 = str(P1)
            P2 = str(P2)
            Elev = str(Elev)

            if(LocationCounter == 1):

                Tdata0File.write(str(Dist1) + chr(9) + Elev + "\n")
                Tdata1File.write(str(Dist1) + chr(9) + Elev + "\n")
                if(Flag2 == 1):
                    Tdata2File.write(str(Dist1) + chr(9) + Elev + "\n")
                Path = float(Elev) + float(AntennaHeight1)
                if(abs(Path) < .1):
                    Path = 0
                Path = str(Path)
                Pdata0File.write(str(Dist1) + chr(9) + Path + "\n")
                Pdata1File.write(str(Dist1) + chr(9) + Path + "\n")
                if(Flag2 == 1):
                    Pdata2File.write(str(Dist1) + chr(9) + Path + "\n")
                    continue

            Delta1 = float(T1) - float(T0)
            Delta2 = float(T2) - float(T0)

            Ht0 = float(Elev)
            Ht1 = Ht0 + Delta1
            Ht2 = Ht0 + Delta2

            if(abs(Ht0) < .1):
                Ht0 = 0
            if(abs(Ht1) < .1):
                Ht1 = 0
            if(abs(Ht2) < .1):
                Ht1 = 0

            Ht0 = str(Ht0)
            Ht1 = str(Ht1)
            Ht2 = str(Ht2)

            Tdata0File.write(str(Dist1) + chr(9) + Ht0 + "\n")
            Tdata1File.write(str(Dist1) + chr(9) + Ht1 + "\n")
            if(Flag2 == 1):
                Tdata2File.write(str(Dist1) + chr(9) + Ht2 + "\n")
            Pdata0File.write(str(Dist1) + chr(9) + P0 + "\n")
            Pdata1File.write(str(Dist1) + chr(9) + P1 + "\n")
            if(Flag2 == 1):
                Pdata2File.write(str(Dist1) + chr(9) + P2 + "\n")

        Tdata0File.close()
        Tdata1File.close()
        Tdata2File.close()
        Pdata0File.close()
        Pdata1File.close()
        del ev_df
        del pr_df

        return


def endProgram():  # 9999
    print("\nProgram Completed")
    input("\nPress <Enter> key to clear this window")
    sys.exit(app.exec_())


################################################# PyQT GUI Class ###################################################
# Based on code from https://pythonspot.com/pyqt5-file-dialog/
class App(PyQt5.QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = ''
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

    def openFolderNameDialog(self, folderPrompt):
        folderName = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, folderPrompt)
        if folderName:
            folderName = os.path.normpath(folderName)
            return folderName


################################################# End PyQT GUI Class ###################################################
# Create PyQT Object
app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = App()

os.system('cls' if os.name == 'nt' else 'clear')

print("Path Profile Plotting Program")
print("\n(C) TeleVision, Inc.")
print("georgekizer@gmail.com")
print("972.333.0712 / 972.618.2890\n")

FolderPath = ex.openFolderNameDialog(
    "Enter name of folder(s) containing the input (e.g., ProfData)")

ProfileA_Window = PyQt5.QtWidgets.QMainWindow()
ex = Ui_ProfileA_Window(ProfileA_Window)
ProfileA_Window.show()
ProfileA_Window.Btn_start.clicked.connect()

def reportProgress(n):
    ProfileA_Window.progressBar.setProperty("value", n*20)

def runProfileA():
    
    thread = QThread()
    
    worker = Worker()
    
    worker.moveToThread(thread)
    
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    worker.progress.connect(reportProgress)
    
    
    thread.start()
    
    

endProgram()
