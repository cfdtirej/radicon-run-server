import json
import os
from pathlib import Path
from datetime import date

import yaml
from flask import Flask, jsonify, request, abort

import rrt1
import sokuchi_field
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
        res = list(client.query("SELECT * FROM mobile ORDER BY DESC LIMIT 10"))[0]
        return jsonify({'Data': res})
    elif request.method == 'POST':
        req = request.get_json()
        DATE = date.today().isoformat().replace('-', '')
        post_log = Path(__file__).parents[2]/'post_log'/f'{DATE}_post_json'
        if not post_log.parent.is_dir():
            post_log.parent.mkdir()
        with open(post_log, 'a') as f:
            write_json = json.dumps(req, indent=4)
            f.write(f'{write_json},')
        line_protocol = client.req_json_to_line_plotocol(req)
        try:
            client.write_points(line_protocol)
            print(line_protocol)
            return jsonify(line_protocol)
        except Exception as e:
            return jsonify({'message': f'{e}'}), 500

@app.route('/sokuchi')
def hello():
    car_id = request.args.get('car_id')
    dt = request.args.get('date')
    data = list(client.query(f"SELECT * FROM mobile WHERE time = '{dt}'"))[0][0]
    sokuchi_x = (data["GRSS_RTK_x"])
    sokuchi_y = (data["GRSS_RTK_y"])
    a, b = sokuchi_field.sokuchi_field(sokuchi_x,sokuchi_y)
    field_x = a
    field_y = b
    # time.sleep(10)
    # return jsonify(create_json.create_json(Car_ID, DateTime))
    return jsonify(rrt1.main(car_id, dt, field_x, field_y))

if __name__ == '__main__':
    app.run(
        host=conf['Server']['host'],
        port=conf['Server']['port'],
        debug=True
    )
