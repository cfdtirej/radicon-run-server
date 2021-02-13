import json
from typing import List, Dict, Union
from pathlib import Path

import numpy as np


APPOS_JSON = Path(__file__).parent/'APPOS.json'


def pole_obstacle_xy(pole_id: int, distance: float, angle: float) -> Dict[str, float]:
    with open(APPOS_JSON, 'r') as f:
        appos = json.load(f)['AP Pos']
    for pos in appos:
        if pos['Pole id '] == pole_id:
            x = pos['Position '][0] + distance * np.cos(angle)
            y = pos['Position '][1] + distance * np.sin(angle)
            return {'x': x, 'y': y}

if __name__ == '__main__':
    from datetime import datetime
    dt_now = datetime.now()
    post_json = {
        'poleID': 1,
        'DateTime': str(dt_now),
        'Position': {
            'COM1': {
                'Object_name': 1,
                'Size' : 250,
                'Distance' : 300,
                'Angle' : 75
            }
        }
    }
    xy = pole_obstacle_xy(
        post_json['poleID'], 
        post_json['Position']['COM1']['Distance'], 
        post_json['Position']['COM1']['Angle']
    )
    print(xy)