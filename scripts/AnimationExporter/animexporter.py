from maxsdk import utility

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from pymxs import runtime as rt
import AnimationExporter.fsBatcher.ui.mainwindow_ui as mainWindowUI
reload(mainWindowUI)
import AnimationExporter.fsBatcher.max.AnimationTeamBatcher as AnimExport
reload(AnimExport)

class MainWindow(QWidget,mainWindowUI.Ui_MainWindow):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.readSettings()

        self.batchPaths = []
        self.exportPaths = []
        self.exportBtn.clicked.connect(self.export)
        self.browseExportBtn.clicked.connect(self.browseFolderExport)

        self.exportFolderCmb.setCurrentIndex(self.exportFolderCmb.count() - 1)
        self.cleanLog()
        self.maxProcess = QProcess()

    def browseFolderExport(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)
        fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        folder = fileDialog.getExistingDirectory(self, "Chose Folder", "/", options=QFileDialog.ReadOnly)
        self.exportPaths.append(folder)
        self.exportFolderCmb.addItem(folder)
        self.exportFolderCmb.setCurrentIndex(self.exportFolderCmb.count() - 1)

    def export(self):
        exportType = self.exportTypeCmb.currentText()
        exportPath = self.exportFolderCmb.currentText()
        bakeAnim = self.bakeAnimChk.isChecked()

        if not exportPath or not exportType:
            return

        AnimExport.exportScene(exportPath=exportPath,bakeAnim=bakeAnim,exportType=exportType)

    def log(self, text):
        self.logger.setText(text)

    def cleanLog(self):
        self.logger.setText("")

    def writeSettings(self):
        settings = QSettings("Asobo Studio", "FlightSim Batch Exporter")
        settings.beginGroup("Main Settings")

        settings.beginWriteArray("exportPaths")
        for i in range(self.exportFolderCmb.count()):
            settings.setArrayIndex(i)
            settings.setValue("exportPath", self.exportFolderCmb.itemText(i))
        settings.endArray()

        settings.setValue("exportType", self.exportTypeCmb.currentIndex())
        settings.endGroup()

    def readSettings(self):
        settings = QSettings("Asobo Studio", "FlightSim Batch Exporter")
        settings.beginGroup("Main Settings")

        exportPathCount = settings.beginReadArray("exportPaths")
        for i in range(exportPathCount):
            settings.setArrayIndex(i)
            item = settings.value("exportPath")
            self.exportFolderCmb.addItem(item)
        settings.endArray()

        exportTypeIndex = settings.value("exportType", 0)
        self.exportTypeCmb.setCurrentIndex(exportTypeIndex)
        settings.endGroup()

    def closeEvent(self, QCloseEvent):
        self.writeSettings()
        super(MainWindow, self).closeEvent(QCloseEvent)

if __name__ == '__main__':
    animationExporter = MainWindow()
    utility.attachToMax(animationExporter)
    animationExporter.show()
