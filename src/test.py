import json
from pathlib import Path
from random import choice
import pyvista as pv
from pyvista import examples

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