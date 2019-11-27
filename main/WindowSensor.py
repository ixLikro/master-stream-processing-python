import json


def windowExtraction(x):
    j = json.loads(x)
    ret = list((
        j["name"],
        j["room ID"],
    ))

    windows = j["windows"]
    oneOpen = False
    for window in windows:
        if window["isOpen"]:
            oneOpen = True

    ret.append(oneOpen)

    return ret
