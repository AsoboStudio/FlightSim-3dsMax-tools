from pymxs import runtime as rt

def setUserProp(node, keyName, value):
    if isinstance(value, str):
        rt.setUserProp(node, keyName, value)
    if isinstance(value, unicode):
        rt.setUserProp(node, keyName, value)
    if isinstance(value, int):
        rt.setUserProp(node, keyName, str(value))
    if isinstance(value, float):
        rt.setUserProp(node, keyName, str(value))


def getUserProp(node, keyName, defaultValue = None):
    res = rt.getUserProp(node, keyName)
    if res:
        return res
    else:
        return defaultValue


def getUserPropDict(node, propName, keyName=None):
    res = rt.getUserProp(node, propName)
    dictRes = dict()
    try:
        keyValue = res.split(";")

        for kv in keyValue:
            k = kv.split("~")[0]
            v = kv.split("~")[1]
            dictRes.update({k: v})
        if not keyName:
            return dictRes
        else:
            return dictRes[keyName]
    except:
        return dictRes



def setUserPropDict(node, propName, dictObj):
    if isinstance(dictObj,dict):
        propertyValue = ""
        for i in range(len(dictObj.items())):
            key = list(dictObj.keys())[i]
            value = list(dictObj.values())[i]
            propertyValue += "{0}~{1}".format(str(key), str(value))
            if i < len(dictObj.items()) -1:
                propertyValue +=";"
        rt.setUserProp(node, propName, propertyValue)

def removeUserProp(node, keyName):
    rt.deleteUserProp(node,keyName)

def openUserPropertyWindow():
    if(rt.UserDefinedPlus_isOpen):
        rt.macros.run("ASOBO","UserDefinedPlus") # if open, close it first
    rt.macros.run("ASOBO","UserDefinedPlus") # and open/reopen it to focus     
