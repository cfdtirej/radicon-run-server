import os
from influxdb.client import InfluxDBClient

import yaml
from flask import Flask, jsonify, request

from utils import IoTPoleDBClient


config_yaml = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_yaml, 'r') as f:
    conf = yaml.safe_load(f)

app = Flask(__name__)

client = IoTPoleDBClient(
    host=conf['InfluxDB']['host'],
    port=conf['InfluxDB']['port'],
    username=conf['InfluxDB']['username'],
    password=conf['InfluxDB']['password'],
    database=conf['InfluxDB']['database']
)

@app.route('/', methods=['POST'])
def home():
    req = request.get_json()
    print(req)
    return jsonify(req)


if __name__ == '__main__':
    app.run(
        host=conf['Server']['host'],
        port=conf['Server']['port'],
        debug=True
    )
