from PySide2 import QtWidgets, QtCore
import MaxPlus

def ShowFileDialog():
    # move this to ui file
    w = QtWidgets.QFileDialog()

    w.resize(250, 100)
    w.setWindowTitle('Mirror Animation')

    # Attaches the QWidget to the 3dsmax mainwindow
    MaxPlus.AttachQWidgetToMax(w)


    return w