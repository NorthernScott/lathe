import json
from random import choice


def getPlanetName() -> str:
    """_summary_

    Returns:
        _description_
    """
    f = open("planetnames.json")
    data = json.load(f)
    names = data["planetNames"]

    return choice(names)


print(getPlanetName())
