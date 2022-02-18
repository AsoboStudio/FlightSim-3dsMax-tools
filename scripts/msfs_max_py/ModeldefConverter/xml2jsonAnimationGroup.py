import json
import os
import re
import uuid
import xml.etree.ElementTree as ET
import maxsdk.utility as utility
import maxsdk.qtUtils as qtUtils
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from pymxs import runtime as rt

if sys.version_info >= (3, 0):
    from ModeldefConverter.ui import converterWindow_ui
else:
    from ui import converterWindow_ui

MODELDEF = "E:\\KittyHawk_Staging_ccreutz\\ASSETS\\KittyHawk_Data\\Tools\\3DSMAX\FSX_MaxExporter\\modeldef.xml"
OUTPUT = "E:\\KittyHawk_Staging_ccreutz\\ASSETS\\KittyHawk_Data\\Tools\\3DSMAX\FSX_MaxExporter\\modeldef.json"


class ConverterWindow(QWidget, converterWindow_ui.Ui_XMLtoJSON):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setMaximumHeight(100)
        self.btnGenerate.clicked.connect(self._clickedGenerate)
        self.btnBrowseJSON.clicked.connect(self._clickedBrowseJSON)
        self.btnBrowseXML.clicked.connect(self._clickedBrowseXML)
    
    def _clickedBrowseXML(self):
        string = qtUtils.openSaveFileNameDialog(_filter="XML(*.xml)", forcedExtension=None)
        if(string != None):
            self.lineXML.setText(string)

    def _clickedBrowseJSON(self):
        string = qtUtils.openSaveFileNameDialog(_filter="JSON(*.json)", forcedExtension=None)
        if(string != None):
            self.lineJSON.setText(string)

    def _clickedGenerate(self):
        xmlFile = self.lineXML.text()
        jsonFile = self.lineJSON.text()
        try:
            convert(xmlFile, jsonFile)
            qtUtils.popup(title="json file succesfully created", text="Successfully created :\n{0}".format(jsonFile))
        except Exception as exception:
            qtUtils.popup(title="Error", text=str(exception))

def convert(xmlPath, outputPath):
    result = []
    parsedMDL = ET.parse(xmlPath)
    root = parsedMDL.getroot()
    overrider = {}
    for x in root.iter():
        if x.tag == "PartInfo":
            nameAttrib = x.find("Name")
            if nameAttrib is not None:
                nameOverride = nameAttrib.text
            lengthAttrib = x.find("AnimLength")
            if lengthAttrib is not None:
                lengthOverride = lengthAttrib.text
            overrider[nameOverride] = lengthOverride            
    
    for x in root.iter():
        if x.tag == "Animation":
            animLength = 0
            name = ""
            animDict = {}
            if x.attrib.has_key("name"):
                name = x.attrib["name"]
            if x.attrib.has_key("length"):
                animLength = x.attrib["length"]
            if x.attrib.has_key("typeParam2"):
                overriderName = x.attrib["typeParam2"]         
                if overrider.has_key(overriderName):
                    animLength = overrider[overriderName]
            if name != "":
                animDict["Name"] = name
                animDict["TicksStart"] = 0
                animDict["TicksEnd"] = int(animLength) * 160
                animDict["AnimationGroupNodes"] = None
                result.append(animDict)

    print(len(result))

    with open(outputPath, 'w') as jf:
        jsonFile = json.dump(result, jf)
        print("Created {0}".format(outputPath))

window = None

def run():
    global window
    window = ConverterWindow()
    window.show()
