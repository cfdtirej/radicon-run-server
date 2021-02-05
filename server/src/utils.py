import json
import os
from datetime import date, datetime
from typing import List, Dict, Union

from scipy.optimize import minimize
import numpy as np
from influxdb import InfluxDBClient


APPOS_JSON = os.path.join(os.path.dirname(__file__), 'APPOS.json')


def calc_xy(phi_deg, lambda_deg, phi0_deg=36.0, lambda0_deg=137.0 + 10/60) -> Dict[str, float]:
    # 緯度経度・平面直角座標系原点をラジアンに直す
    phi_rad = np.deg2rad(phi_deg)
    lambda_rad = np.deg2rad(lambda_deg)
    phi0_rad = np.deg2rad(phi0_deg)
    lambda0_rad = np.deg2rad(lambda0_deg)

    # 補助関数
    def A_array(n):
        A0 = 1 + (n**2)/4. + (n**4)/64.
        A1 = -     (3./2)*(n - (n**3)/8. - (n**5)/64.)
        A2 = (15./16)*(n**2 - (n**4)/4.)
        A3 = -   (35./48)*(n**3 - (5./16)*(n**5))
        A4 = (315./512)*(n**4)
        A5 = -(693./1280)*(n**5)
        return np.array([A0, A1, A2, A3, A4, A5])

    def alpha_array(n):
        a0 = np.nan  # dummy
        a1 = (1./2)*n - (2./3)*(n**2) + (5./16)*(n**3) + \
            (41./180)*(n**4) - (127./288)*(n**5)
        a2 = (13./48)*(n**2) - (3./5)*(n**3) + \
            (557./1440)*(n**4) + (281./630)*(n**5)
        a3 = (61./240)*(n**3) - (103./140)*(n**4) + (15061./26880)*(n**5)
        a4 = (49561./161280)*(n**4) - (179./168)*(n**5)
        a5 = (34729./80640)*(n**5)
        return np.array([a0, a1, a2, a3, a4, a5])
    # 定数 (a, F: 世界測地系-測地基準系1980（GRS80）楕円体)
    m0 = 0.9999
    a = 6378137.
    F = 298.257222101
    # (1) n, A_i, alpha_iの計算
    n = 1. / (2*F - 1)
    A_array = A_array(n)
    alpha_array = alpha_array(n)
    # (2), S, Aの計算
    A_ = ((m0*a)/(1.+n))*A_array[0]  # [m]
    S_ = ((m0*a)/(1.+n))*(A_array[0]*phi0_rad + np.dot(
        A_array[1:], np.sin(2*phi0_rad*np.arange(1, 6))))  # [m]
    # (3) lambda_c, lambda_sの計算
    lambda_c = np.cos(lambda_rad - lambda0_rad)
    lambda_s = np.sin(lambda_rad - lambda0_rad)
    # (4) t, t_の計算
    t = np.sinh(np.arctanh(np.sin(phi_rad)) - ((2*np.sqrt(n)) / (1+n))
                * np.arctanh(((2*np.sqrt(n)) / (1+n)) * np.sin(phi_rad)))
    t_ = np.sqrt(1 + t*t)
    # (5) xi', eta'の計算
    xi2 = np.arctan(t / lambda_c)  # [rad]
    eta2 = np.arctanh(lambda_s / t_)
    # (6) x, yの計算
    x = A_ * (xi2 + np.sum(np.multiply(alpha_array[1:],
                                       np.multiply(np.sin(2*xi2*np.arange(1, 6)),
                                                   np.cosh(2*eta2*np.arange(1, 6)))))) - S_  # [m]
    y = A_ * (eta2 + np.sum(np.multiply(alpha_array[1:],
                                        np.multiply(np.cos(2*xi2*np.arange(1, 6)),
                                                    np.sinh(2*eta2*np.arange(1, 6))))))  # [m]
    return {'x': x, 'y': y}


def gps_solve(distances_to_station, stations_coordinates):
    def error(x, c, r):
        return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])
    l = len(stations_coordinates)
    S = sum(distances_to_station)
    # compute weight vector for initial guess
    W = [((l - 1) * S) / (S - w) for w in distances_to_station]
    # get initial guess of point location
    x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])

    # optimize distance from signal origin to border of spheres
    return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x


def multilateration(wifi_rtt: List[Dict[str, Union[int, float]]]) -> Dict[str, float]:
    distances_to_station = []
    for idx in range(1, 4):
        for pole_info in wifi_rtt:
            if pole_info['PoleID'] == idx:
                distances_to_station.append(pole_info['Distance_m'])
    with open(APPOS_JSON, 'r') as f:
        appos = json.load(f)['AP Pos']
        appos_lists: List[List[float, float]] = [
            ap['Position '] for ap in appos]
        stations: List[np.ndarray[np.float, np.float]] = list(
            np.array(appos_lists))

    coordinate = gps_solve(distances_to_station, stations)
    return {'x': coordinate[0], 'y': coordinate[1]}


def poleID_dist_m(data: List[Dict[str, Union[int, float]]]) -> Dict[str, float]:
    '''
    data: request_json['Position']['WiFi-RTT']
    [
        {
            'PoleID': int,
            Distance_m: float
        },
    ]
    '''
    pole_dist_m = {}
    for pole_dist in data:
        pole_number = pole_dist['PoleID']
        key = f'pole{pole_number}_dist_m'
        pole_dist_m[key] = pole_dist['Distance_m']
    return pole_dist_m


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
        GNSS_RTK_xy = calc_xy(request_json['Position']['GNSS-RTK']['Latitude_deg'],
                              request_json['Position']['GNSS-RTK']['Longitute_deg'])
        WiFi_RTT_xy = multilateration(request_json['Position']['WiFi-RTT'])
        WiFi_RTT_dist = poleID_dist_m(request_json['Position']['WiFi-RTT'])
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'mobile',
            'tag': {
                'CarID': request_json['CarID']
            },
            'fields': {
                'GRSS_RTK_x': GNSS_RTK_xy['x'],
                'GRSS_RTK_y': GNSS_RTK_xy['y'],
                'Quality': request_json['Position']['GNSS-RTK']['Quality'],
                'WiFi_RTT_x': WiFi_RTT_xy['x'],
                'WiFi_RTT_y': WiFi_RTT_xy['y'],
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
    
    @classmethod
    def req_pole_lineprotocol(cls, reqest_json: dict) -> List:
        return 

    @classmethod
    def req_json_to_line_plotocol_old_version(cls, request_json: dict) -> list:
        GNSS_RTK_xy = calc_xy(request_json['Position']['GNSS-RTK']['Latitude_deg'],
                              request_json['Position']['GNSS-RTK']['Longitute_deg'])
        WiFi_RTT_dist = poleID_dist_m(request_json['Position']['WiFi-RTT'])
        line_protocol = [{
            'time': to_rfc3339(request_json['DateTime']),
            'measurement': 'mobile',
            'tag': {
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
        
