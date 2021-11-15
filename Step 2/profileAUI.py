import json

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork, QtWebEngineWidgets


class Ui_ProfileA_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #QtWidgets.QMainWindow.__init__(self)
        self.setupUi()
        self.setupEvents()
    
    def setupUi(self):
        self.setWindowTitle("ProfileA_Window")
        self.resize(1110, 791)
        self.accountFrame = QtWidgets.QFrame(self.)
        self.accountFrame.setGeometry(QtCore.QRect(0, 0, 231, 791))
        self.accountFrame.setAcceptDrops(False)
        self.accountFrame.setAutoFillBackground(False)
        self.accountFrame.setStyleSheet("background-color: rgb(8, 44, 108);")
        self.accountFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.accountFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.accountFrame.setObjectName("accountFrame")
        self.Btn_home = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_home.setGeometry(QtCore.QRect(0, 260, 231, 71))
        self.Btn_home.setMouseTracking(True)
        self.Btn_home.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                    "color:white;\n"
                                    "border: none;\n"
                                    )
        self.Btn_home.setFlat(True)
        self.Btn_home.setObjectName("Btn_home")
        self.pushButton_2 = QtWidgets.QPushButton(self.accountFrame)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 360, 231, 71))
        self.pushButton_2.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                        "color:white;\n"
                                        "border: none;\n"
                                        "QPushButton::hover"
                                        "{"
                                        "background-color: rgb(255, 255, 255);"
                                        "color: rgb(8, 44, 108);"
                                        "}"
                                        )
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.Btn_NetCorfig = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_NetCorfig.setGeometry(QtCore.QRect(0, 340, 231, 71))
        self.Btn_NetCorfig.setMouseTracking(True)
        self.Btn_NetCorfig.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                         "color:white;\n"
                                         "border: none;\n"
                                         "QPushButton::hover"
                                         "{"
                                         "background-color: rgb(255, 255, 255);"
                                         "color: rgb(8, 44, 108);"
                                         "}"
                                         )
        self.Btn_NetCorfig.setFlat(True)
        self.Btn_NetCorfig.setObjectName("Btn_NetCorfig")
        self.Btn_FAQ = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_FAQ.setGeometry(QtCore.QRect(0, 550, 231, 71))
        self.Btn_FAQ.setMouseTracking(True)
        self.Btn_FAQ.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                   "color:white;\n"
                                   "border: none;\n"
                                   "QPushButton::hover"
                                   "{"
                                   "background-color: rgb(255, 255, 255);"
                                   "color: rgb(8, 44, 108);"
                                   "}"
                                   )
        self.Btn_FAQ.setCheckable(False)
        self.Btn_FAQ.setFlat(True)
        self.Btn_FAQ.setObjectName("Btn_FAQ")
        self.Btn_CheckOut = QtWidgets.QPushButton(self.accountFrame)
        self.Btn_CheckOut.setGeometry(QtCore.QRect(0, 630, 231, 71))
        self.Btn_CheckOut.setMouseTracking(True)
        self.Btn_CheckOut.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                        "color:white;\n"
                                        "border: none;\n"
                                        "QPushButton::hover"
                                        "{"
                                        "background-color: rgb(255, 255, 255);"
                                        "color: rgb(8, 44, 108);"
                                        "}"
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
        
        self.frame_MainBody = QtWidgets.QFrame()
        self.frame_MainBody.setGeometry(QtCore.QRect(-1, -1, 1171, 831))
        self.frame_MainBody.setAutoFillBackground(False)
        self.frame_MainBody.setStyleSheet("background-color:white;")
        self.frame_MainBody.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_MainBody.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_MainBody.setObjectName("frame_MainBody")
        
        self.frm_TerminalBg = QtWidgets.QFrame(self.frame_MainBody)
        self.frm_TerminalBg.setGeometry(QtCore.QRect(230, 420, 881, 321))
        self.frm_TerminalBg.setAutoFillBackground(False)
        self.frm_TerminalBg.setStyleSheet("background-color: balck;")
        self.frm_TerminalBg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_TerminalBg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_TerminalBg.setObjectName("frm_TerminalBg")
        self.label_terminalTxt = QtWidgets.QLabel(self.frm_TerminalBg)
        self.label_terminalTxt.setGeometry(QtCore.QRect(10, 10, 861, 301))
        self.label_terminalTxt.setStyleSheet("color : green;")
        self.label_terminalTxt.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_terminalTxt.setObjectName("label_terminalTxt")
        self.progressBar = QtWidgets.QProgressBar(self.frame_MainBody)
        self.progressBar.setGeometry(QtCore.QRect(230, 740, 881, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        
        self.Btn_start = QtWidgets.QPushButton(self.frame_MainBody)
        self.Btn_start.setGeometry(QtCore.QRect(570, 160, 230, 70))
        self.Btn_start.setMouseTracking(True)
        self.Btn_start.setStyleSheet("font: 87 8pt \"Arial Black\";\n"
                                     "color:white;\n"
                                     "background-color: rgb(8, 44, 108);"
                                     "border: none;\n"
                                     )
        self.Btn_start.setFlat(True)
        self.Btn_start.setObjectName("Btn_start")
        
        self.Btn_home.setText("Home")
        self.pushButton_2.setText("PushButton")
        self.Btn_NetCorfig.setText("Network Configuration")
        self.Btn_FAQ.setText( "FAQ")
        self.Btn_CheckOut.setText("Check out")
        self.Btn_start.setText( "start")
        self.label_actName.setText("User Name")
        self.label_userEmail.setText("username@email.com")
        self.label_terminalTxt.setText( "> _")
        
        self.frame_MainBody.raise_()
        self.accountFrame.raise_()
        self.frm_TerminalBg.raise_()
        self.progressBar.raise_()

    def setupEvents(self):
        print("setting up events")

    def onQApplcationStart(self):
        print("started")


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




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_ProfileA_Window()
    ui.show()
    sys.exit(app.exec_())
