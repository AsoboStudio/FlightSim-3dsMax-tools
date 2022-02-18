from pymxs import runtime as rt
from maxsdk.globals import *
def setUserProp(node, keyName, value):
    if isinstance(value, str):
        rt.setUserProp(node, keyName, value)
    if MAXVERSION() < MAX2021:    
        if isinstance(value, unicode):
            rt.setUserProp(node, keyName, value)
    if isinstance(value, int):
        rt.setUserProp(node, keyName, str(value))
    if isinstance(value, float):
        rt.setUserProp(node, keyName, str(value))


def getUserProp(node, keyName, defaultValue=None):
    
    res = rt.getUserProp(node, keyName)
    if res != None:
        return res
    else:
        return defaultValue


def dictToString(dictObj):
    """Turns a dictionary into a string. 
    Entries are separated by ; and key/values are separated by ~
    \nexample = keyA\~valueA;keyB\~valueB;keyC\~valueC
    """
    if isinstance(dictObj, dict):
        propertyValue = ""
        for i in range(len(dictObj.items())):
            key = list(dictObj.keys())[i]
            value = list(dictObj.values())[i]
            propertyValue += "{0}~{1}".format(str(key), str(value))
            if i < len(dictObj.items()) - 1:
                propertyValue += ";"
        return propertyValue
    return None


def stringToDict(string):
    """Turns a string to a dictionary and keeps every keys and values as string
    """
    dictRes = dict()
    keyValue = string.split(";")
    for kv in keyValue:
        k = kv.split("~")[0]
        v = kv.split("~")[1]
        dictRes.update({k: v})
    return dictRes

def string_to_typed_dict(string):
    """Turns a string to a dictionary and guesses the obvious types if possible
    """
    dictRes = dict()
    keyValue = string.split(";")
    for kv in keyValue:
        k = kv.split("~")[0]
        v = kv.split("~")[1]
        v = convertUserPropToObviousType(v)
        dictRes.update({k: v})
    return dictRes


def setUserPropHeadedDict(node, propName, nameDict):
    """headedDictionary = tuple(str, dict)
    """
    header = nameDict[0]
    dictObj = nameDict[1]
    if isinstance(dictObj, dict):
        propertyValue = "{0};".format(str(header))
        propertyValue += dictToString(dictObj)
        setUserProp(node, propName, propertyValue)

def getUserPropHeadedDict(node, propName):
    """
    reads the user property propName in the node and turns it into a tuple( header, dictionary ).\n 
    
    in: node=pymxs.MXSWrapperBase, propName=str, keyName=str\n 
    out: tuple(str,dict) 
    """
    res = getUserProp(node, propName)
    if res is not None:
        headless = res.split(";", 1)
        if (len(headless) == 1):
            return (headless[0], dict())
        if (headless[1] != ""):
            dictObj = string_to_typed_dict(headless[1])
            return (headless[0], dictObj)
        else:
            return (headless[0], dict())
    else:
        return 


def getUserPropDict(node, propName, keyName=None):
    """If no keyname specified, returns the dictionary otherwise returns only the kay associated value as a string"""
    res = getUserProp(node, propName)
    dictRes = dict()
    try:
        dictRes = stringToDict(res)
        if not keyName:
            return dictRes
        else:
            return dictRes[keyName]
    except:
        return dictRes

def setUserPropDict(node, propName, dictObj):
    """Set a dictionary in the user property of a node.
    """
    if isinstance(dictObj, dict):
        propertyValue = dictToString(dictObj)
        setUserProp(node, propName, propertyValue)

def setUserPropList(node, propName, listObj):
    """Set a list in the user property of a node.
    """
    if isinstance(listObj, list):
        propertyValue = ""
        objCount = len(listObj)
        for i in range(objCount):
            if listObj[i] is None:
                continue
            propertyValue += cleanupStringForPropListStorage(listObj[i])
            #if (i < objCount - 1):
            propertyValue += ";"
        rt.setUserProp(node, propName, propertyValue)

def getUserPropList(node, propName):
    """Get a list from the user property of a node
    """
    res = rt.getUserProp(node, propName)
    if (res is None):
        return None
    listRes = list()    
    values = res.split(";")
    for v in values:
        if (v != None and v != ""):            
            listRes.append(v)
    return listRes

def parseUserPropAsList(string):
    """Get a list from a string. Member are separated by semi colon ;
    """
    res = string
    if (res is None):
        return None
    listRes = list()    
    values = res.split(";")
    for v in values:
        if (v != None and v != ""):            
            listRes.append(v)
    return listRes

def removeUserProp(node, keyName):
    """Removes a user property from a node
    """
    rt.deleteUserProp(node, keyName)
    
def getUserPropBuffer(node):
    """Returns the complete user property buffer of an object
    """
    propBuffer = rt.getUserPropBuffer(node)
    return propBuffer

def setUserPropBuffer(node, buffer):
    rt.setUserPropBuffer(node,buffer)

def openUserPropertyWindow():
    if(rt.UserDefinedPlus_isOpen):
        rt.macros.run("ASOBO","UserDefinedPlus") # if open, close it first
    rt.macros.run("ASOBO", "UserDefinedPlus")  # and open/reopen it to focus  

def cleanupStringForPropListStorage(string):
    """Remove all the non-ASCII character, tide and semicolon.
    This function should be used before putting a string in the setUserPropList or setUserPropDict
    """
    cleanString = str()
    for c in string:        
        if (ord(c) < 128) and c != ";" and c != "~":
            cleanString += c
    return cleanString

def convertUserPropToObviousType(i):
    """
    Convert a string into another type if the type is obvious.

    \nin:
    i=string to convert

    \nout:
    bool / None / int / float / str / unicode
    """
    if isinstance(i,str) or isinstance(i,unicode):
        if (i == "False"):
            return False
        elif (i == "True"):
            return True
        elif (i == "None"):
            return None
    try:
        return int(i)
    except:
        try:
            return float(i)
        except:
            try:
                return str(i)
            except:
                return unicode(i)

