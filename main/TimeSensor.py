import json


def simTimeExtractor(x):
    j = json.loads(x)
    return list((
        j["name"],
        j["simTime"]
    ))