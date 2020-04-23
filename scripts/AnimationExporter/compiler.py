import os
from pyside2uic import compileUi
import glob
import subprocess

dirPath = os.path.dirname(os.path.realpath(__file__))
uiCompiledDest = os.path.join(dirPath, r"fsBatcher/ui/")
rccCompileDest = os.path.join(dirPath, r"fsBatcher/rcc/")
resourcesDir = os.path.join(dirPath, r"resources")
uiFiles = (glob.glob("{0}/*.ui".format(resourcesDir)))
qrcFiles = (glob.glob("{0}/*.qrc".format(resourcesDir)))

for uiFilePath in uiFiles:
    fileName = os.path.basename(uiFilePath)
    name = os.path.splitext(fileName)[0]
    pyfile = open(r"{destDir}\{name}_ui.py".format(destDir=uiCompiledDest, name=name), 'w')
    compileUi(r"{sourceDir}\{name}.ui".format(sourceDir=resourcesDir, name=name), pyfile, False, 4, False)
    pyfile.close()

for qrcFile in qrcFiles:
    fileName = os.path.basename(qrcFile)
    name = os.path.splitext(fileName)[0]
    pyfile = r"{0}\{1}_rc.py".format(rccCompileDest, name)
    try:
        subprocess.call(["pyrcc5", qrcFile, "-o", pyfile])
    except:
        print("You must install pyrcc5")
