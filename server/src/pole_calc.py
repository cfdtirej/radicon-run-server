import json
from typing import List, Dict, Union
from pathlib import Path

import numpy as np


APPOS_JSON = Path(__file__).parent/'APPOS.json'

with open(APPOS_JSON, 'r') as f:
    appos = json.load(f)['AP Pos']


def pole_obstacle_xy(pole_id: int, distance: float, angle: float) -> Dict[str, float]:
    for pos in appos:
        if pos['Pole id '] == pole_id:
            x = pos['Position '][0] + distance * np.cos(angle)
            y = pos['Position '][1] + distance * np.sin(angle)
            return {'x': x, 'y': y}
