import json


def energyConsumptionExtractor(x):
    j = json.loads(x)
    return list((
        j["name"], j["measuring"]["value"], j["measuring"]["measuring Unit"]
    ))


