import json


def extractTemperature(x):
    j = json.loads(x)
    return list((
        j["name"],
        j["measuring"]["value"],
        j["measuring"]["measuring Unit"],
        j["sensor Info"]["Measuring range Temperature"]["from"],
        j["sensor Info"]["Measuring range Temperature"]["upTo"]
    ))