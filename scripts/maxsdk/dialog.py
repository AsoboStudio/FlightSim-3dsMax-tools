from PySide2.QtWidgets import *
from PySide2.QtCore import *
from maxsdk.globals import *


def showMessage(message):
    if message:
        dialog = QMessageBox(text=message, parent=GetMaxMainWindow())
        dialog.show()