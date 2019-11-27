import json


def barometerExtractor(x):
    j = json.loads(x)
    return list((
        j["name"],
        j["measuring"]["value"],
        j["measuring"]["measuring Unit"],
        j["sensor Info"]["Measuring range"]["from"],
        j["sensor Info"]["Measuring range"]["upTo"]
    ))


def averagePressure(values):
    noneCount = 0
    sum = 0
    for value in values:
        if value[1] is None:
            noneCount = noneCount + 1
        else:
            sum = sum + value[1]

    if (noneCount <= 1):
        return sum / (len(values) - noneCount)
    return None
