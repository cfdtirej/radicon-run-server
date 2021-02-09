import requests
import json
import datetime
from pathlib import Path

import yaml


dt_now = datetime.datetime.now()

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

conf_yaml = Path(__file__).parent/'client_config.yaml'
with open(conf_yaml, 'r') as f:
    conf = yaml.safe_load(f)
    requests.post(url=conf['polePost'], json=post_json)