import sys
import importlib
import os
#________Parameters_________
ECHO_ENABLED = True
MAIN_DIR_NAME = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEBUG_FILES = "debug.py"
COMPILER_FILES = "compiler.py"
PYTHON_PATH_LIST = []
PYTHON_FILES_LIST = []  
MOD_LIST = []  

def ListdirFullpath(_dir):
    """Get full given directory path """
    return [os.path.join(_dir, f) for f in os.listdir(_dir)]


def IsAcceptableFile(f):
    if not os.path.isfile(f):
        return False
    if (".pyc" in f):
        return False
    if (".py" not in f):
        return False
    if (DEBUG_FILES in f):
        return False
    if (COMPILER_FILES in f):
        return False
    # if ("main.py" in f):
    #     return False
    # if ("ViewportCustomizer.py" in f):
    #     return False
    if (os.path.basename(__file__) in f):
        return False
    return True
    
def ReloadPackages():
    """ Reload all pakages inside a project """
    global PYTHON_PATH_LIST
    global PYTHON_FILES_LIST
    global MOD_LIST

    if sys.version_info >= (3, 0):
        importlib.invalidate_caches()

    for _CurFile in ListdirFullpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):        
        if os.path.isdir(_CurFile):                             # & ("ui" not in _CurFile):
            GetSubPyFiles(_CurFile)
            #print(_CurFile)


        if IsAcceptableFile(_CurFile):
            PYTHON_PATH_LIST += [_CurFile]
            #print(_CurFile)
    
    for _pythModPath in PYTHON_PATH_LIST:

        if sys.version_info >= (3, 0):
            pathSinceWorkFile = os.path.basename(_pythModPath)
        else:
            pathToScript = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # pathtoScript #os.path.dirname(__file__).replace(os.path.basename(__file__), "")
            pathSinceWorkFile = _pythModPath.replace(pathToScript,"")# MAIN_DIR_NAME) #max2019
            pathSinceWorkFile = pathSinceWorkFile.replace("\\", ".") #max2019
            pathSinceWorkFile = pathSinceWorkFile[1:]

        pathSinceWorkFile = pathSinceWorkFile.replace(".py", "")
        PYTHON_FILES_LIST += [pathSinceWorkFile]

    for _pythMod in PYTHON_FILES_LIST:  #Importing
        try:
            _mod = importlib.import_module(_pythMod)
            if ECHO_ENABLED:
                print("Imported >>> {0}".format(_mod))
                MOD_LIST += [_mod]
        except Exception as error:
            print("Module cannot be imported because {0}".format(error))


    for _modLoc in MOD_LIST:            #Reloading
        if sys.version_info >= (3, 0):
            importlib.reload(_modLoc)
        else:
            reload(_modLoc)
        if ECHO_ENABLED:
            print("Reloaded >>> {0}".format(_modLoc))
    
    print("There is {0} modules imported".format(len(MOD_LIST)))

    if sys.version_info >= (3, 0):
        print("uper 3.0")
        PYTHON_PATH_LIST.clear()
        PYTHON_FILES_LIST.clear()
        MOD_LIST.clear()
    else:
        del PYTHON_PATH_LIST[:]
        del PYTHON_FILES_LIST[:]
        del MOD_LIST[:]


    print("Finished Reload all ")


def GetSubPyFiles(_CurFolders):
    """ Iterate throught all subfile to get py files """
    global PYTHON_PATH_LIST

    for _SubCurrFile in ListdirFullpath(_CurFolders):               
        if os.path.isdir(_SubCurrFile):
            GetSubPyFiles(_SubCurrFile)

        if IsAcceptableFile(_SubCurrFile):
            PYTHON_PATH_LIST += [_SubCurrFile]

# ReloadPackages()