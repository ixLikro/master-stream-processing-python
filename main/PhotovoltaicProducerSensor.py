import json


def produceExtractor(x):
    j = json.loads(x)
    return list((
        j["name"], j["measuring"]["value"], j["measuring"]["measuring Unit"]
    ))


