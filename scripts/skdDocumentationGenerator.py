import os
import sys
import re
import inspect

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import types

from maxsdk import layer
import MultiExporter.optionsMenu as optionsMenu

def printDoc(moduleToPrint):
    print(moduleToPrint.__name__)
    print(moduleToPrint.__doc__)
    for di in sorted(dir(moduleToPrint)):
        #if di[0:2] != "__":
        func = getattr(moduleToPrint, di)
        if type(func) == types.FunctionType:        
            printFunction(func)
        if isClass(str(func)):
            printClass(func)

def printClass(classToPrint):
    print("----------------------")
    printDoc(classToPrint)

        

def printFunction(funcToPrint):
    print("----------------------")
    print("def {0}".format(funcToPrint.__name__))
    print("")
    description = funcToPrint.__doc__
    if description is not None:
        lines = description.splitlines()
        for line in lines:
            test = re.match("^ *$",line)
            if test is None:
                print(line)

class TEST(QComboBox):
    def __init__(self):
        QComboBox.__init__(self)

def isClass(toTest):
    return re.match(r"^<class .+$", toTest) is not None

#printDoc(optionsMenu)

members = inspect.getmembers(optionsMenu.ComboBoxOptionPreset)

members = dir(optionsMenu.ComboBoxOptionPreset)

print(inspect.getmembers(optionsMenu))
#print members
#for mem in members:
#    if mem[0:2] != "__":
#        print("---------------------------------")
#        func = getattr(optionsMenu.ComboBoxOptionPreset, mem)
#        print mem
#        if func.__doc__ is not None:
#            print(func.__doc__)

#
#for name, doc in members:
#    print("--------")
#    print(name)
#    print("")
#    print(doc)