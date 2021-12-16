import json

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork 

    # Use only if geo coder class is needed
#from PyQt5 import QtWebEngineWidgets


# class for scrollable label
class ScrollLabel(QtWidgets.QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QtWidgets.QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QtWidgets.QVBoxLayout(content)

        # creating label
        self.label = QtWidgets.QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
        
    def text(self):
        return self.label.text()

class Ui_Window(QtWidgets.QMainWindow):
    def __init__(self, i):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi()
        
        
        if (i == 1):
            self.profileAsetup()
        elif (i == 2):
            self.scriptSetup()
        
        else:
            self.label_err = QtWidgets.QLabel(self.frame_MainBody)
            self.label_err.setGeometry(QtCore.QRect(570, 160, 230, 70))
            self.label_err.setStyleSheet("color: rgb(255, 255, 255);")
            self.label_err.setAlignment(QtCore.Qt.AlignCenter)
            self.label_err.setObjectName("label_err")
            self.label_err.setText("No module for Id: " + str(i) + " exists")
            
        self.setupEvents()

    def setupUi(self):
        self.setWindowTitle("UI_Window")
        self.resize(1232, 1000)
        self.accountFrame = QtWidgets.QFrame(self)
        self.accountFrame.setGeometry(QtCore.QRect(0, 0, 231, 1022))
        self.accountFrame.setAcceptDrops(False)
        self.accountFrame.setAutoFillBackground(False)
        self.accountFrame.setStyleSheet("background-color: rgb(8, 44, 108);")
        self.accountFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.accountFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.accountFrame.setObjectName("accountFrame")
        self.Btn_home = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_home.setGeometry(QtCore.QRect(0, 260, 231, 71))
        self.Btn_home.setMouseTracking(True)
        self.Btn_home.setStyleSheet("""
                                        QPushButton
                                        {
                                        font: 87 8pt "Arial Black";
                                        color:white;
                                        border: none;
                                        }
                                        QPushButton:hover
                                        {
                                        font: 87 8pt "Arial Black";
                                        background-color: rgb(255, 255, 255);
                                        color: rgb(8, 44, 108);
                                        }
                                        """
                                    )
        self.Btn_home.setFlat(True)
        self.Btn_home.setObjectName("Btn_home")

        self.Btn_NetCorfig = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_NetCorfig.setGeometry(QtCore.QRect(0, 350, 231, 71))
        self.Btn_NetCorfig.setMouseTracking(True)
        self.Btn_NetCorfig.setStyleSheet("""
                                             QPushButton
                                        {
                                        font: 87 8pt "Arial Black";
                                        color:white;
                                        border: none;
                                        }
                                        QPushButton:hover
                                        {
                                        font: 87 8pt "Arial Black";
                                        background-color: rgb(255, 255, 255);
                                        color: rgb(8, 44, 108);
                                        }
                                        
                                        """
                                         )
        self.Btn_NetCorfig.setFlat(True)
        self.Btn_NetCorfig.setObjectName("Btn_NetCorfig")
        self.Btn_FAQ = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_FAQ.setGeometry(QtCore.QRect(0, 550, 231, 71))
        self.Btn_FAQ.setMouseTracking(True)
        self.Btn_FAQ.setStyleSheet("""
                                             QPushButton
                                        {
                                        font: 87 8pt "Arial Black";
                                        color:white;
                                        border: none;
                                        }
                                        QPushButton:hover
                                        {
                                        font: 87 8pt "Arial Black";
                                        background-color: rgb(255, 255, 255);
                                        color: rgb(8, 44, 108);
                                        }
                                        
                                        """
                                   )
        self.Btn_FAQ.setCheckable(False)
        self.Btn_FAQ.setFlat(True)
        self.Btn_FAQ.setObjectName("Btn_FAQ")
        self.Btn_CheckOut = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_CheckOut.setGeometry(QtCore.QRect(0, 700, 231, 71))
        self.Btn_CheckOut.setMouseTracking(True)
        self.Btn_CheckOut.setStyleSheet("""
                                            QPushButton
                                        {
                                        font: 87 8pt "Arial Black";
                                        color:white;
                                        border: none;
                                        }
                                        QPushButton:hover
                                        {
                                        font: 87 8pt "Arial Black";
                                        background-color: rgb(255, 255, 255);
                                        color: rgb(8, 44, 108);
                                        }
                                        
                                        """
                                        )
        self.Btn_CheckOut.setFlat(True)
        self.Btn_CheckOut.setObjectName("Btn_CheckOut")
        self.label_actName = QtWidgets.QLabel(self.accountFrame)
        self.label_actName.setGeometry(QtCore.QRect(60, 180, 111, 20))
        self.label_actName.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_actName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_actName.setObjectName("label_actName")
        self.label_userEmail = QtWidgets.QLabel(self.accountFrame)
        self.label_userEmail.setGeometry(QtCore.QRect(60, 200, 111, 31))
        self.label_userEmail.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_userEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.label_userEmail.setObjectName("label_userEmail")
        self.frame_UsrImg = QtWidgets.QFrame(self.accountFrame)
        self.frame_UsrImg.setGeometry(QtCore.QRect(60, 40, 111, 111))
        self.frame_UsrImg.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "border:1px solid black;\n"
                                        "border-radius: 55px;")
        self.frame_UsrImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_UsrImg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_UsrImg.setObjectName("frame_UsrImg")

        self.frame_MainBody = QtWidgets.QFrame(self)
        self.frame_MainBody.setGeometry(QtCore.QRect(230, 0, 1000, 1000))
        self.frame_MainBody.setAutoFillBackground(False)
        self.frame_MainBody.setStyleSheet("background-color:white;")
        self.frame_MainBody.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_MainBody.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_MainBody.setObjectName("frame_MainBody")

        self.frm_TerminalBg = QtWidgets.QFrame(self.frame_MainBody)
        self.frm_TerminalBg.setGeometry(QtCore.QRect(5, 620, 1000, 321))
        self.frm_TerminalBg.setAutoFillBackground(False)
        self.frm_TerminalBg.setStyleSheet("background-color: balck;")
        self.frm_TerminalBg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_TerminalBg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_TerminalBg.setObjectName("frm_TerminalBg")
        self.label_terminalTxt = ScrollLabel(self.frm_TerminalBg)
        self.label_terminalTxt.setGeometry(QtCore.QRect(10, 10, 980, 301))
        self.label_terminalTxt.setStyleSheet("color : green;")
        self.label_terminalTxt.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_terminalTxt.setObjectName("label_terminalTxt")
        self.progressBar = QtWidgets.QProgressBar(self.frame_MainBody)
        self.progressBar.setGeometry(QtCore.QRect(5, 943, 1000, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.Btn_home.setText("Home")
        self.Btn_NetCorfig.setText("Network Configuration")
        self.Btn_FAQ.setText("FAQ")
        self.Btn_CheckOut.setText("Check out")
        self.label_actName.setText("User Name")
        self.label_userEmail.setText("username@email.com")
        self.label_terminalTxt.setText("> _")

        self.frame_MainBody.raise_()
        self.accountFrame.raise_()
        self.frm_TerminalBg.raise_()
        self.progressBar.raise_()

    def setupEvents(self):
        print("setting up events")

    def profileAsetup(self):
        self.Btn_start = QtWidgets.QPushButton(self.frame_MainBody)
        self.Btn_start.setGeometry(QtCore.QRect(570, 160, 230, 70))
        self.Btn_start.setMouseTracking(True)
        self.Btn_start.setStyleSheet("""
                                            QPushButton
                                            {
                                                font: 87 8pt "Arial Black";
                                                color:white;
                                                background-color: rgb(8, 44, 108);
                                                border: none;
                                                border-radius: 10px;
                                            }
                                            QPushButton:hover
                                                {
                                                font: 87 8pt "Arial Black";
                                                background-color: rgb(72, 128, 225);
                                                color: rgb(192, 192, 192);
                                                border: 2px solid rgb(13, 61, 144);
                                                border-radius: 10px
                                                }
                                            """
                                     )
        self.Btn_start.setFlat(True)
        self.Btn_start.setObjectName("Btn_start")
        self.Btn_start.setText("start")

    def scriptSetup(self):
        self.frame_Script = QtWidgets.QFrame(self.frame_MainBody)
        self.frame_Script.setGeometry(QtCore.QRect(5, 5, 1001, 600))
        self.frame_Script.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Script.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Script.setObjectName("frame_Script")
        self.frame_ScriptStep1 = QtWidgets.QFrame(self.frame_Script)
        self.frame_ScriptStep1.setGeometry(QtCore.QRect(0, 0, 1001, 601))
        self.frame_ScriptStep1.setAutoFillBackground(True)
        self.frame_ScriptStep1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ScriptStep1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ScriptStep1.setObjectName("frame_ScriptStep1")
        self.checkBox_landUse = QtWidgets.QCheckBox(self.frame_ScriptStep1)
        self.checkBox_landUse.setGeometry(QtCore.QRect(50, 530, 221, 17))
        self.checkBox_landUse.setObjectName("checkBox_landUse")
        self.checkBox_RetainIndex = QtWidgets.QCheckBox(self.frame_ScriptStep1)
        self.checkBox_RetainIndex.setGeometry(QtCore.QRect(50, 550, 261, 17))
        self.checkBox_RetainIndex.setObjectName("checkBox_RetainIndex")
        self.Lab_DataFolderPath = QtWidgets.QLabel(self.frame_ScriptStep1)
        self.Lab_DataFolderPath.setGeometry(QtCore.QRect(40, 20, 101, 31))
        self.Lab_DataFolderPath.setObjectName("Lab_DataFolderPath")
        self.Lab_DataFolderPath_2 = QtWidgets.QLabel(self.frame_ScriptStep1)
        self.Lab_DataFolderPath_2.setGeometry(QtCore.QRect(40, 90, 101, 31))
        self.Lab_DataFolderPath_2.setObjectName("Lab_DataFolderPath_2")
        self.btn_Folder_2 = QtWidgets.QPushButton(self.frame_ScriptStep1)
        self.btn_Folder_2.setGeometry(QtCore.QRect(680, 120, 31, 31))
        self.btn_Folder_2.setObjectName("btn_Folder_2")
        self.btn_Folder = QtWidgets.QPushButton(self.frame_ScriptStep1)
        self.btn_Folder.setGeometry(QtCore.QRect(680, 50, 31, 31))
        self.btn_Folder.setObjectName("btn_Folder")
        self.comboBox = QtWidgets.QComboBox(self.frame_ScriptStep1)
        self.comboBox.setGeometry(QtCore.QRect(240, 190, 41, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.btn_submit_1 = QtWidgets.QPushButton(self.frame_ScriptStep1)
        self.btn_submit_1.setGeometry(QtCore.QRect(650, 540, 75, 23))
        self.btn_submit_1.setObjectName("btn_submit_1")
        self.btn_terrainOptionsHelp = QtWidgets.QPushButton(
            self.frame_ScriptStep1)
        self.btn_terrainOptionsHelp.setGeometry(QtCore.QRect(170, 190, 21, 21))
        self.btn_terrainOptionsHelp.setObjectName("btn_terrainOptionsHelp")
        self.txtbrsr_dataFolder = QtWidgets.QTextBrowser(
            self.frame_ScriptStep1)
        self.txtbrsr_dataFolder.setGeometry(QtCore.QRect(40, 50, 621, 31))
        self.txtbrsr_dataFolder.setObjectName("txtbrsr_dataFolder")
        self.listWidget = QtWidgets.QListWidget(self.frame_ScriptStep1)
        self.listWidget.setGeometry(QtCore.QRect(40, 230, 681, 281))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.lab_terrainOptions = QtWidgets.QLabel(self.frame_ScriptStep1)
        self.lab_terrainOptions.setGeometry(QtCore.QRect(40, 190, 141, 16))
        self.lab_terrainOptions.setObjectName("lab_terrainOptions")
        self.txtbrsr_dataFolder_2 = QtWidgets.QTextBrowser(
            self.frame_ScriptStep1)
        self.txtbrsr_dataFolder_2.setGeometry(QtCore.QRect(40, 120, 621, 31))
        self.txtbrsr_dataFolder_2.setObjectName("txtbrsr_dataFolder_2")
        
        self.checkBox_landUse.setText(
             "add land use & land cover (LULC) data")
        self.checkBox_RetainIndex.setText(
             "Retain Index (Only if the input file has an index)")
        self.Lab_DataFolderPath.setText(
             "Data Folder Path")
        self.Lab_DataFolderPath_2.setText(
             "Data Folder Path")
        self.btn_Folder_2.setText( "...")
        self.btn_Folder.setText( "...")
        self.comboBox.setItemText(0,  "1")
        self.comboBox.setItemText(1,  "2")
        self.comboBox.setItemText(2,  "3")
        self.comboBox.setItemText(3,  "4")
        self.comboBox.setItemText(4,  "5")
        self.comboBox.setItemText(5,  "6")
        self.comboBox.setItemText(6,  "7")
        self.comboBox.setItemText(7,  "8")
        self.btn_submit_1.setText( "Submit")
        self.btn_terrainOptionsHelp.setText( "?")
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(
             "1   USGS NATIONAL ELEVATION DATABASE FOR THE US (10 METER NED) [includes Hawaii]")
        item = self.listWidget.item(2)
        item.setText(
             "2   USGS NATIONAL ELEVATION DATABASE FOR THE US (30 METER NED)[includes Hawaii (30 meter) and Alasaka (60 meter)]")
        item = self.listWidget.item(4)
        item.setText(
             "3   USGS PUERTO RICO AND THE US VIRGIN ISLANDS (30 METER DEM)")
        item = self.listWidget.item(6)
        item.setText(
             "4   SHUTTLE TERRAIN DATA FOR THE US (30 METER SRTM)")
        item = self.listWidget.item(8)
        item.setText(
             "5   SHUTTLE TERRAIN DATA FOR THE WORLD (90 METER SRTM)")
        item = self.listWidget.item(10)
        item.setText(
             "6   USGS GTOPO30 TERRAIN DATABASE FOR THE WORLD (1 KM GRID)")
        item = self.listWidget.item(12)
        item.setText(
             "7   CANADA CDED 1: 50,000 SCALE TERRAIN DATA FILES (10 - 20 METER)")
        item = self.listWidget.item(14)
        item.setText(
             "8   CANADA CDED 1:250,000 SCALE TERRAIN DATA FILES (30 - 90 METER)")
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.lab_terrainOptions.setText(
             "Terrain Database Options")


"""
class GeoCoder(QtNetwork.QNetworkAccessManager):
    class NotFoundError(Exception):
        pass

    def geocode(self, location, api_key):
        url = QtCore.QUrl("https://maps.googleapis.com/maps/api/geocode/xml")

        query = QtCore.QUrlQuery()
        query.addQueryItem("key", api_key)
        query.addQueryItem("address", location)
        url.setQuery(query)
        request = QtNetwork.QNetworkRequest(url)
        reply = self.get(request)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        reply.deleteLater()
        self.deleteLater()
        return self._parseResult(reply)

    def _parseResult(self, reply):
        xml = reply.readAll()
        reader = QtCore.QXmlStreamReader(xml)
        while not reader.atEnd():
            reader.readNext()
            if reader.name() != "geometry":
                continue
            reader.readNextStartElement()
            if reader.name() != "location":
                continue
            reader.readNextStartElement()
            if reader.name() != "lat":
                continue
            latitude = float(reader.readElementText())
            reader.readNextStartElement()
            if reader.name() != "lng":
                continue
            longitude = float(reader.readElementText())
            return latitude, longitude
        raise GeoCoder.NotFoundError


class QGoogleMap(QtWebEngineWidgets.QWebEngineView):
    mapMoved = QtCore.pyqtSignal(float, float)
    mapClicked = QtCore.pyqtSignal(float, float)
    mapRightClicked = QtCore.pyqtSignal(float, float)
    mapDoubleClicked = QtCore.pyqtSignal(float, float)

    markerMoved = QtCore.pyqtSignal(str, float, float)
    markerClicked = QtCore.pyqtSignal(str, float, float)
    markerDoubleClicked = QtCore.pyqtSignal(str, float, float)
    markerRightClicked = QtCore.pyqtSignal(str, float, float)

    def __init__(self, api_key, parent=None):
        super(QGoogleMap, self).__init__(parent)
        self._api_key = api_key
        channel = QtWebChannel.QWebChannel(self)
        self.page().setWebChannel(channel)
        channel.registerObject("qGoogleMap", self)
        self.page().runJavaScript(JS)

        html = HTML.replace("API_KEY", "YOUR_API_KEY_HERE")
        self.setHtml(html)
        self.loadFinished.connect(self.on_loadFinished)
        self.initialized = False

        self._manager = QtNetwork.QNetworkAccessManager(self)

    @QtCore.pyqtSlot()
    def on_loadFinished(self):
        self.initialized = True

    def waitUntilReady(self):
        if not self.initialized:
            loop = QtCore.QEventLoop()
            self.loadFinished.connect(loop.quit)
            loop.exec_()

    def geocode(self, location):
        return GeoCoder(self).geocode(location, self._api_key)

    def centerAtAddress(self, location):
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            print("Not found {}".format(location))
            return None, None
        self.centerAt(latitude, longitude)
        return latitude, longitude

    def addMarkerAtAddress(self, location, **extra):
        if 'title' not in extra:
            extra['title'] = location
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None
        return self.addMarker(location, latitude, longitude, **extra)

    @QtCore.pyqtSlot(float, float)
    def mapIsMoved(self, lat, lng):
        self.mapMoved.emit(lat, lng)

    @QtCore.pyqtSlot(float, float)
    def mapIsClicked(self, lat, lng):
        self.mapClicked.emit(lat, lng)

    @QtCore.pyqtSlot(float, float)
    def mapIsRightClicked(self, lat, lng):
        self.mapRightClicked.emit(lat, lng)

    @QtCore.pyqtSlot(float, float)
    def mapIsDoubleClicked(self, lat, lng):
        self.mapDoubleClicked.emit(lat, lng)

    # markers
    @QtCore.pyqtSlot(str, float, float)
    def markerIsMoved(self, key, lat, lng):
        self.markerMoved.emit(key, lat, lng)

    @QtCore.pyqtSlot(str, float, float)
    def markerIsClicked(self, key, lat, lng):
        self.markerClicked.emit(key, lat, lng)

    @QtCore.pyqtSlot(str, float, float)
    def markerIsRightClicked(self, key, lat, lng):
        self.markerRightClicked.emit(key, lat, lng)

    @QtCore.pyqtSlot(str, float, float)
    def markerIsDoubleClicked(self, key, lat, lng):
        self.markerDoubleClicked.emit(key, lat, lng)

    def runScript(self, script, callback=None):
        if callback is None:
            self.page().runJavaScript(script)
        else:
            self.page().runJavaScript(script, callback)

    def centerAt(self, latitude, longitude):
        self.runScript("gmap_setCenter({},{})".format(latitude, longitude))

    def center(self):
        self._center = {}
        loop = QtCore.QEventLoop()

        def callback(*args):
            self._center = tuple(args[0])
            loop.quit()

        self.runScript("gmap_getCenter()", callback)
        loop.exec_()
        return self._center

    def setZoom(self, zoom):
        self.runScript("gmap_setZoom({})".format(zoom))

    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript(
            "gmap_addMarker("
            "key={!r}, "
            "latitude={}, "
            "longitude={}, "
            "{}"
            "); ".format(key, latitude, longitude, json.dumps(extra)))

    def moveMarker(self, key, latitude, longitude):
        return self.runScript(
            "gmap_moveMarker({!r}, {}, {});".format(key, latitude, longitude))

    def setMarkerOptions(self, keys, **extra):
        return self.runScript(
            "gmap_changeMarker("
            "key={!r}, "
            "{}"
            "); "
            .format(keys, json.dumps(extra)))

    def deleteMarker(self, key):
        return self.runScript(
            "gmap_deleteMarker("
            "key={!r} "
            "); ".format(key))
"""

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Window(1)
    ui.show()
    sys.exit(app.exec_())
