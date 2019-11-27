import json


def batteryExtractor(x):
    j = json.loads(x)
    return list((
        j["name"], j["measuring"]["value"], j["measuring"]["measuring Unit"], j["battery Info"]["Usable capacity"]
    ))

