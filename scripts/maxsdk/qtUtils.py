import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pymxs import runtime as rt


class CustomFileDialog(QFileDialog):
    def __init__(self, *args, **kwards):
        QFileDialog.__init__(self, *args, **kwards)


class ScrollMessageBox(QMessageBox):
    def __init__(self, text, title="", *args, **kwargs):
        lineCount = text.count("\n")
        print(lineCount)
        self.minHeight = 150 + lineCount * 10
        if self.minHeight > 400:
            self.minHeight = 400
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.setWindowTitle(title)
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        self.content.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        txt = QLabel(text, self)
        txt.setWordWrap(True)
        lay.addWidget(txt)
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QMessageBox.event(self, e)
        if(self.minHeight is not None):
            self.setMinimumHeight(self.minHeight)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(400)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)
        return result


def truncateStringFromLeft(string, maxLength):
    """Truncate a string from the left side until the string's length is less than maxLength
    """
    stringLen = len(string)
    truncString = string[max(stringLen-maxLength, 0):stringLen]
    if (stringLen > maxLength):
        truncString = "..." + truncString
    return truncString
# add checkbox to a widget.
# x=0 y=0 represent the top left corner of the widget


def createCheckBox(qtWidget, x=14, y=2, w=17, h=17):
    """Adds a checkbox to a widget and returns a reference to it
    """
    headerGeom = qtWidget.geometry()
    frameTopLeft = headerGeom.topLeft()
    fx = frameTopLeft.x()
    fy = frameTopLeft.y()
    posX = x + fx
    posY = y + fy
    topLeft = QPoint(posX, posY)
    botRight = QPoint(posX + w, posY + h)
    geom = QRect(topLeft, botRight)
    checkBox = QCheckBox(qtWidget)
    checkBox.setGeometry(geom)
    return checkBox


def openSaveFileNameDialog(parent=None, caption="", _dir="", _filter="", forcedExtension=".gltf"):
    """Opens a Save File dialog and returns the chosen path
    """
    dialog = QFileDialog(parent, caption, _dir, _filter)
    dialog.setDirectory(_dir)
    if dialog.exec_() == 1:
        filePath = dialog.selectedFiles()
        if len(filePath) > 0:
            ext = os.path.splitext(filePath[0])
            if forcedExtension is not None:
                if (ext[1] != forcedExtension):
                    filePath[0] = ext[0] + forcedExtension
            if (filePath[0] != ""):
                return filePath[0]
    return None

def openSaveFolderPathDialog(_caption ="Choose a folder", _dir ="" ):
    dialog = QFileDialog.getExistingDirectory(caption = _caption, dir = _dir)
    return dialog

def validateFloatLineEdit(x):
    """ Turn a string into a float. Will replace comma by full stop if needed
    """
    try:
        return float(x)
    except:
        try:
            # turns comma into period and try again
            return float(x.replace(",", "."))
        except:
            print("Invalid float entered")
    return None


def _getNewMessageBox(text, title=""):
    """Creates a message box and returns a reference to it
    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setMaximumHeight(500)
    msgBox.setMaximumSize
    msgBox.setText(text)
    flagsOnTop = Qt.WindowFlags(Qt.WindowStaysOnTopHint)
    msgBox.setWindowFlags(flagsOnTop)
    return msgBox


def popup(text, title=""):
    """Opens a message popup
    """
    msgBox = _getNewMessageBox(text, title)
    msgBox.exec_()


def popup_detail(text, title="", detail=""):
    """Opens a message popup with a detail rollout
    """
    msgBox = _getNewMessageBox(text, title)
    msgBox.setDetailedText(detail)
    msgBox.exec_()


def popup_scroll(text, title=""):
    """Opens a message popup with a scrollbar
    """
    msgBox = ScrollMessageBox(text=text, title=title)
    msgBox.exec_()


def popup_Yes_No(text, title=""):
    """Opens a Yes or No message popup.
    Returns True if yes is pressed"""
    msgBox = _getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.No
    msgBox.setStandardButtons(buttons)
    msgBox.setButtonText(0, "lol")
    output = msgBox.exec_()
    if(output == QMessageBox.Yes):
        return True
    else:
        return False


def popup_Yes_YesToAll_No(text, title=""):
    """Opens a Yes YesToAll and No message popup
    Returns 2 for yes, 1 for YesToAll and 0 for No
    """
    msgBox = _getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    if(output == QMessageBox.Yes):
        return 2
    if(output == QMessageBox.YesToAll):
        return 1
    else:
        return 0


def popup_Yes_YesToAll_No_NoToAll(text, title=""):
    """Opens a Yes, YesToAll, No and NoToAll message popup.
    Returns 3 for Yes, 2 for YesToAll, 1 for No and 0 for NoToAll
    """
    msgBox = _getNewMessageBox(text, title)
    buttons = QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    if(output == QMessageBox.Yes):
        return 3
    if(output == QMessageBox.YesToAll):
        return 2
    if(output == QMessageBox.No):
        return 1
    if(output == QMessageBox.NoToAll):
        return 0
    else:  # default
        print("Default")
        return 1
