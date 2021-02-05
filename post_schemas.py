from datetime import datetime


car_post = \
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

pole_post = \
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
print(datetime.now())
