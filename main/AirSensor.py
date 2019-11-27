import json


def airExtractor(x):
    j = json.loads(x)
    return list((
        j["name"],
        j["measuring"]["value"],
        j["measuring"]["measuring Unit"],
        j["sensor Info"]["Measuring range"]["from"],
        j["sensor Info"]["Measuring range"]["upTo"]
    ))