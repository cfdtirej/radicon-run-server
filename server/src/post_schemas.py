from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class GNSS_RTK:
    Latitude_deg: float
    Longitute_deg: float
    Quality: int

@dataclass
class WiFi_RTK:
    PoleID: int
    Distance_m: float

@dataclass
class Position:
    GNSS_RTK: GNSS_RTK
    WiFi_RTK: List[WiFi_RTK]

@dataclass
class CarPost:
    CarID: int
    DateTime: str
    Position: Position
    Azimuth_deg: int
    Speed_level: int
    Steering_level: int
    ObstacleDistance_m: float
  
car_post: CarPost = \
{
    "CarID": 1,
    "DateTime": '2021/1/1 10:15:20.223',
    "Position": {
        "GNSS-RTK": {
            "Latitude_deg": 36.1234,
            "Longitute_deg": 137.332,
            "Quality": 1
        },
        "WiFi-RTT": [
            {
                "PoleID": 1,
                "Distance_m": 25.333
            },
            {
                "PoleID": 2,
                "Distance_m": 5.322
            },
            {
                "PoleID": 3,
                "Distance_m": 15.324
            }
        ]
    },
    "Azimuth_deg": -30,
    "Speed_level": 5,
    "Steering_level": 3,
    "ObstacleDistance_m": 2.432
}


@dataclass
class COM1:
    Object_name: int
    Size: int
    Distance: int
    Angle: int

@dataclass
class PolePost:
    poleID: int
    DateTime: str
    Position: Dict[str, COM1]

pole_post: PolePost = \
{
    'poleID': 1,
    'DateTime': '2021-02-05 17:44:58.543414',
    "Position": {
        'COM1': {
            'Object_name': 1,
            "Size" : 250,
            "Distance" : 300,
            "Angle" : 75
        }
    }
}

if __name__ == '__main__':
    print(CarPost(**car_post))
    print(PolePost(**pole_post))
    car_post_s = CarPost(**car_post)
    print(asdict(car_post_s))
