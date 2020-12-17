from os import error
from client import send
import glob
import json
import requests
from typing import Dict, List


# log_postのJSONの末尾に','がなかったときのやつ
def format_log_old_ver(log_file: str) -> List[dict]:
    with open(log_file, 'r') as f:
        read_strings = ''.join([s.strip() for s in f.readlines()])
    brackets = {'{': '}', '[': ']'}
    stack = []
    json_string = '['
    for string in read_strings:
        if string in brackets.keys():
            stack.append(brackets[string])
        if string in brackets.values():
            stack.pop(-1)
            if not stack:
                json_string += string
                json_string += ','
                continue
        json_string += string
    json_string = json_string[:-1] + ']'
    return json.loads(json_string)


def send_log(url: str, data_list: List[dict]):
    for data in data_list:
        res = requests.post(url, json=data)
        try:
            print(res, res.json())
        except Exception:
            print(res)


if __name__ == '__main__':
    url = 'http://127.0.0.1:13000/'
    log_files = glob.glob('./log_post/*')
    for log_file in log_files:
        send_log(url, data_list=format_log_old_ver(log_file))