from pymxs import runtime as rt
from maxsdk import node as sdknode
from maxsdk.globals import *
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ContainerResolver.ui.containerResolver_ui as containerResolver

class LoggerItemUI(QWidget, containerResolver.Ui_ContainerResolver):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

class ContainersLogger(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Containers Logger")
        self.mainLayout = QVBoxLayout(self)
        self.run()
        

    def addContainerLog(self,containerName,path,status,info):
        self.logItem = LoggerItemUI()
        self.logItem.name_lbl.setText(containerName)
        self.logItem.status_lbl.setText(status)
        self.logItem.path_lbl.setText(path)
        self.logItem.info_lbl.setText(info)
        
        self.mainLayout.addWidget(self.logItem)

    def run(self):
        containers = sdknode.get_all_containers()
        if not containers or containers.count == 0:
            self.addContainerLog("","","","No containers found in the scene")
            return
            
        for c in containers:
            path =  c.sourceDefinitionFilename
            if not path :
                path = c.localDefinitionFilename
            if not path:
                info =  "probably merged in the scene during last save...cannot resolve it"
                self.addContainerLog(c.Name,"",status="broken",info=info)
                continue
            absolutePath = os.path.join(rt.pathConfig.getCurrentProjectFolder(),path)
            if os.path.exists(absolutePath):
                self.addContainerLog(c.Name,path=absolutePath,status="ok",info="")
                continue
            else:
                s = path.split(r"KittyHawk_Data")[1]
                newSource = rt.pathConfig.getCurrentProjectFolder() +s
                if os.path.exists(newSource):
                    c.sourceDefinitionFilename = newSource
                    c.UpdateContainer()
                    self.addContainerLog(c.Name,path=newSource,status="resolved",info="")
        
            

    