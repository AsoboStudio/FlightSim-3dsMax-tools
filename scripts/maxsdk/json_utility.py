from globals import *
if MAXVERSION() < MAX2021:
    import MaxPlus

def encodePositionController(controller):
    num_keys = controller.GetNumKeys()
    result = []
    for i in range(num_keys):
        key_time = controller.GetKeyTime(i)
        MaxPlus.Animation.SetTime(key_time, False)
        pos = controller.GetPoint3Value()

        keys = {"point3": encodePoint3(pos),
                "key": key_time / 160}
        result.append(keys)

    return result


def encodeRotationController(controller):
    num_keys = controller.GetNumKeys()
    result = []
    for i in range(num_keys):
        key_time = controller.GetKeyTime(i)
        MaxPlus.Animation.SetTime(key_time, False)
        rot = controller.GetQuatValue()
        keys = {"quat": encodeQuaternion(rot), "key": key_time / 160}
        result.append(keys)
    return result


def encodeScaleController(controller):
    num_keys = controller.GetNumKeys()
    result = []
    for i in range(num_keys):
        key_time = controller.GetKeyTime(i)
        MaxPlus.Animation.SetTime(key_time, False)
        rot = controller.GetQuatValue()
        keys = {"scale": encodeQuaternion(rot), "key": key_time / 160}
        result.append(keys)
    return result


def decodePositionController(controller, data):
    num_keys = len(data)
    # print num_keys
    MaxPlus.Animation.SetAnimateButtonState(True)
    for i in range(num_keys):
        d = data[i]
        key_time = d["key"] * 160
        MaxPlus.Animation.SetTime(key_time, False)
        point = decodePoint3(d["point3"])
        controller.SetPoint3Value(point)
    MaxPlus.Animation.SetAnimateButtonState(False)


def decodeRotationController(controller, data):
    num_keys = len(data)

    MaxPlus.Animation.SetAnimateButtonState(True)
    for i in range(num_keys):
        d = data[i]
        key_time = d["key"] * 160
        MaxPlus.Animation.SetTime(key_time, False)
        quat = decodeQuaternion(d["quat"])
        controller.SetQuatValue(quat)
    MaxPlus.Animation.SetAnimateButtonState(False)


def encodePoint3(value):
    if not isinstance(value, MaxPlus.Point3):
        raise ValueError(str(value) + "is not a Point3 ")

    v = {"x": value.GetX(), "y": value.GetY(), "z": value.GetZ()}
    return v


def decodePoint3(value):
    v = MaxPlus.Point3()
    v.SetX(value["x"])
    v.SetY(value["y"])
    v.SetZ(value["z"])
    return v


def encodeQuaternion(value):
    if not isinstance(value, MaxPlus.Quat):
        raise ValueError(str(value) + "is not a Quat")

    q = {"x": value.GetX(),
         "y": value.GetY(),
         "z": value.GetZ(),
         "w": value.GetW()}

    return q


def decodeQuaternion(value):
    q = MaxPlus.Quat()

    q.SetX(value["x"])
    q.SetY(value["y"])
    q.SetZ(value["z"])
    q.SetW(value["w"])
    return q


def encodeFloat(key, value):
    result = {}
    if type(value) is float:
        result[key] = value
    return result


def encodeMatrix3(value):
    if not isinstance(value, MaxPlus.Matrix3):
        raise ValueError(str(value) + "is not a Matrix3 ")

    result = {"a1": encodePoint3(value[0]),
              "a2": encodePoint3(value[1]),
              "a3": encodePoint3(value[2]),
              "a4": encodePoint3(value[3])}

    return result


def decodeMatrix3(value):
    result = {"a1": encodePoint3(value[0]),
              "a2": encodePoint3(value[1]),
              "a3": encodePoint3(value[2]),
              "a4": encodePoint3(value[3])}

    return result
