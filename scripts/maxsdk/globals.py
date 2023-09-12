import pymxs

rt = pymxs.runtime

MAX2023 = 25000
MAX2022 = 24000
MAX2021 = 23000
MAX2020 = 22000
MAX2019 = 21000
MAX2018 = 20000
MAX2017 = 19000

def DEBUG_MODE():
    vGlobal = rt.name("DEBUG_MODE")
    try:
        if rt.globalVars.get(vGlobal):
            return True
        else:
            return False
    except:
        return False

def MAXVERSION():
    return rt.maxversion()[0]
    
def GetMaxMainWindow():
    if MAXVERSION() >= MAX2021:
        import qtmax
        return qtmax.GetQMaxMainWindow()
    else:
        import MaxPlus
        return MaxPlus.GetQMaxMainWindow()
        
def isMAX2019V3_SUP():
    version = rt.maxversion()
    if version[0] > 21000:
        return True
    elif version.count >=6 and version[0] == 21000 and version[4] >= 3 and version[5] >= 0:
        return True
    else:
        return False