import json

def convertFromKToDegrees(x):
    x[1] = x[1] - 273.15
    return x

def extractTemperature(x):
    j = json.loads(x)
    return list((
        j["name"],
        j["measuring"]["value"],
        j["measuring"]["measuring Unit"],
        j["sensor Info"]["Measuring range Temperature"]["from"],
        j["sensor Info"]["Measuring range Temperature"]["upTo"]
    ))

