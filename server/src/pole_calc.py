import json
from pathlib import Path
from typing import List, Dict, Union
import math

import numpy as np


APPOS_JSON = Path(__file__).parent / 'APPOS.json'


def pole_obstacle_xy(pole_id: int, distance: Union[int, float], angle: Union[int, float]) -> Dict[str, float]:
    distance = distance / 100
    appos_json = Path(__file__).parent / 'APPOS.json'
    with open(appos_json, 'r') as f:
       appos = json.load(f)['AP Pos']
    if pole_id == 1:
        x1, y1 = appos[0]['Position ']
        x2, y2 = appos[2]['Position ']
    elif pole_id == 2:
        x1, y1 = appos[1]['Position ']
        x2, y2 = appos[0]['Position ']
    elif pole_id == 3:
        x1, y1 = appos[2]['Position ']
        x2, y2 = appos[1]['Position ']
    alpha = math.atan2(y1-y2, x1-x2)
    u = distance * math.cos(angle)
    v = distance * math.sin(angle)
    obstacle_xy = np.array([
        [math.cos(alpha), -math.sin(alpha)],
        [math.sin(alpha), math.cos(alpha)]
    ]) @ np.array([u,v]) + np.array([x1, y1])
    
    return {'x': obstacle_xy[0], 'y': obstacle_xy[1]}


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