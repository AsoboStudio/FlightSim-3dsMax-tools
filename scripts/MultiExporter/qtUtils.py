import os


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import MaxPlus
from pymxs import runtime as rt

# add checkbox to a widget. 
# x=0 y=0 represent the top left corner of the widget
def createCheckBox(qtWidget, x = 14, y = 2, w = 17, h = 17):
    headerGeom = qtWidget.geometry()
    frameTopLeft = headerGeom.topLeft()
    fx = frameTopLeft.x()
    fy = frameTopLeft.y()
    posX = x + fx 
    posY = y + fy
    topLeft = QPoint(posX, posY)
    botRight = QPoint(posX + w, posY + h)
    geom = QRect(topLeft,botRight)
    checkBox = QCheckBox(qtWidget)
    checkBox.setGeometry(geom)
    return checkBox

def validateLineEdit(x):
    try:
        return float(x)            
    except:
        try:
            return float(x.replace(",",".")) # turns comma into period and try again
        except:
            print "Invalid float entered"
    return None

def getNewMessageBox(text,title = ""):
    msgBox = QMessageBox()
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    return msgBox

def popup(text, title = ""):
    msgBox = getNewMessageBox(text,title)
    msgBox.exec_()

def popup_Yes_No(text, title = ""):
    msgBox = getNewMessageBox(text,title)
    buttons = QMessageBox.Yes | QMessageBox.No    
    msgBox.setStandardButtons(buttons)
    msgBox.setButtonText(0,"lol")
    output = msgBox.exec_()
    if(output == QMessageBox.Yes):
        return True
    else:
        return False

def popup_Yes_YesToAll_No(text, title = ""):
    msgBox = getNewMessageBox(text,title)
    buttons = QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No
    
    msgBox.setStandardButtons(buttons)
    output = msgBox.exec_()
    if(output == QMessageBox.Yes):
        return 2
    if(output == QMessageBox.YesToAll):
        return 1
    else:
        return 0

def popup_Yes_YesToAll_No_NoToAll(text, title = ""):
    msgBox = getNewMessageBox(text,title)
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
    else: #default
        print "Default"
        return 1
