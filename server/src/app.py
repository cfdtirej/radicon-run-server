import os

import yaml
from flask import Flask, jsonify, request, abort

from utils import IoTPoleDBClient


config_yaml = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_yaml, 'r') as f:
    conf = yaml.safe_load(f)
    client = IoTPoleDBClient(
        host=conf['InfluxDB']['host'],
        port=conf['InfluxDB']['port'],
        username=conf['InfluxDB']['username'],
        password=conf['InfluxDB']['password'],
        database=conf['InfluxDB']['database']
    )

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        res = list(client.query("SELECT * FROM mobile"))[0]
        return jsonify({'Data':res})
    elif request.method == 'POST':
        req = request.get_json()
        try:
            line_protocol = client.req_json_to_line_plotocol(req)
            client.write_points(line_protocol)
            return jsonify(line_protocol)
        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

if __name__ == '__main__':
    app.run(
        host=conf['Server']['host'],
        port=conf['Server']['port'],
        debug=True
    )
