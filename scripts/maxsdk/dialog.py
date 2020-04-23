from PySide2.QtWidgets import *
from PySide2.QtCore import *
import MaxPlus


def showMessage(message):
    if message:
        dialog = QMessageBox(text=message, parent=MaxPlus.GetQMaxMainWindow())
        dialog.show()