import json
import os
from datetime import date, datetime
from typing import List, Dict, Union

from scipy.optimize import minimize
import numpy as np
from influxdb import InfluxDBClient

import car_calc
import pole_calc


def to_rfc3339(dt):
    try:
        dt_3339 = datetime.strptime(
            dt+'+0900', '%Y/%m/%d %H:%M:%S.%f%z').isoformat()
        return dt_3339
    except ValueError:
        dt_3339 = datetime.strptime(
            dt+'+0900', '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
        return dt_3339


class IoTPoleDBClient(InfluxDBClient):

    @classmethod
    def req_json_to_line_plotocol(cls, request_json: dict) -> list:
        GNSS_RTK_xy = car_calc.calc_xy(request_json['Position']['GNSS-RTK']['Latitude_deg'],
                              request_json['Position']['GNSS-RTK']['Longitute_deg'])
        WiFi_RTT_xy = car_calc.multilateration(request_json['Position']['WiFi-RTT'])
        WiFi_RTT_dist = car_calc.poleID_dist_m(request_json['Position']['WiFi-RTT'])
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'mobile',
            'tags': {
                'CarID': request_json['CarID']
            },
            'fields': {
                'GRSS_RTK_x': GNSS_RTK_xy['x'],
                'GRSS_RTK_y': GNSS_RTK_xy['y'],
                'Quality': request_json['Position']['GNSS-RTK']['Quality'],
                'WiFi_RTT_x': WiFi_RTT_xy['x'],
                'WiFi_RTT_y': WiFi_RTT_xy['y'],
                'Azimuth_deg': request_json['Azimuth_deg'],
                'Speed_level': request_json['Speed_level'],
                'Steering_level': request_json['Steering_level'],
                'ObstacleDistance_m': request_json['ObstacleDistance_m'],
                **WiFi_RTT_dist
            }
        }]
        return line_protocol

    @classmethod
    def pole_json_lineprotocol(cls, request_json: dict) -> List[dict]:
        obstacle_xy = pole_calc.pole_obstacle_xy(
            pole_id=request_json['poleID'],
            distance=request_json['Position']['COM1']['Object_name'],
            angle=request_json['Position']['COM1']['Angle'])
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'obstacle',
            'tags': {
                'pole_id': request_json['poleID'],
                'object_name': request_json['Position']['COM1']['Object_name']
            },
            'fields': {
                'pole_id': request_json['poleID'],
                **request_json['Position']['COM1'],
                **obstacle_xy
            }
        }]
        return line_protocol
    
    # 座標変換しない
    @classmethod
    def _pole_json_lineprotocol_tmp(cls, request_json) -> List[dict]:
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'obstacle',
            'tags': {
                'pole_id': request_json['PoleID'],
                'object_name': request_json['Position']['COM1']['Object_name']
            },
            'fields': {
                **request_json['Position']['COM1']
            }
        }]

    
    @classmethod
    def _car_json_lineplotocol(cls, request_json: dict) -> list:
        GNSS_RTK_xy = car_calc.calc_xy(request_json['Position']['GNSS-RTK']['Latitude_deg'],
                              request_json['Position']['GNSS-RTK']['Longitute_deg'])
        WiFi_RTT_dist = car_calc.poleID_dist_m(request_json['Position']['WiFi-RTT'])
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'mobile',
            'tags': {
                'CarID': request_json['CarID']
            },
            'fields': {
                'GRSS-RTK_x': GNSS_RTK_xy['x'],
                'GRSS-RTK_y': GNSS_RTK_xy['y'],
                'Quality': request_json['Position']['GNSS-RTK']['Quality'],
                'pole1_dist_m': WiFi_RTT_dist['pole1_dist_m'],
                'pole2_dist_m': WiFi_RTT_dist['pole2_dist_m'],
                'pole3_dist_m': WiFi_RTT_dist['pole3_dist_m'],
                'Azimuth_deg': request_json['Azimuth_deg'],
                'Speed_level': request_json['Speed_level'],
                'Steering_level': request_json['Steering_level'],
                'ObstacleDistance_m': request_json['ObstacleDistance_m']
            }
        }]
        return line_protocol
        
if __name__ == '__main__':
    request_json = {
        'poleID': 1,
        'DateTime': str(datetime.now()),
        "Position": {
            'COM1': {
                'Object_name': 1,
                "Size" : 250,
                "Distance" : 300,
                "Angle" : 75
            }
        }
    }
    print(IoTPoleDBClient.pole_json_lineprotocol(request_json))