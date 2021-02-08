import json
import os
from pathlib import Path
from datetime import date

import yaml
from flask import Flask, jsonify, request, abort

import rrt1
import sokuchi_field
import post_schemas
import pole_calc
from utils import IoTPoleDBClient


config_yaml = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_yaml, 'r') as f:
    conf = yaml.safe_load(f)
    client = IoTPoleDBClient(**conf['InfluxDB'])

app = Flask(__name__)


@app.route('/')
def home():
    res = list(client.query("SELECT * FROM mobile ORDER BY DESC LIMIT 10"))[0]
    return jsonify({'Data': res})


@app.route('/car', methods=['GET', 'POST'])
def car():
    if request.method == "GET":
        car_id = request.args.get('car_id')
        data = list(client.query('SELECT * FROM mobile LIMIT 1'))[0][0]
        sokuchi_x = (data["GRSS_RTK_x"])
        sokuchi_y = (data["GRSS_RTK_y"])
        dt = (data["time"])
        a, b = sokuchi_field.sokuchi_field(sokuchi_x,sokuchi_y)
        field_x = a
        field_y = b
        return jsonify(rrt1.main(car_id, dt, field_x, field_y))

    elif request.method == 'POST':
        req: post_schemas.CarPost = request.get_json()
        # post jsonを記録（日毎）
        DATE = date.today().isoformat().replace('-', '')
        post_log = Path(__file__).parents[2]/'car_log'/f'{DATE}_post'
        if not post_log.parent.is_dir():
            post_log.parent.mkdir()
        with open(post_log, 'a') as f:
            write_json = json.dumps(req, indent=4)
            f.write(f'{write_json},\n')
        # 座標変換＋DBに記録
        try:
            line_protocol = client.req_json_to_line_plotocol(req)
            client.write_points(line_protocol)
            return jsonify(line_protocol)
        except Exception as e:
            return jsonify({'error': f'{e}'}), 500


@app.route('/pole', methods=['POST'])
def pole():
    if request.method == 'POST':
        req: post_schemas.PolePost = request.get_json()
        # post jsonを記録（日毎）
        DATE = date.today().isoformat().replace('-', '')
        post_log = Path(__file__).parents[2]/'pole_log'/f'{DATE}_post'
        if not post_log.parent.is_dir():
            post_log.parent.mkdir()
        with open(post_log, 'a') as f:
            write_json = json.dumps(req, indent=4)
            f.write(f'{write_json},\n')
        # 座標変換＋DBに記録
        try:
            line_protocol = client.pole_json_lineprotocol(req)
            client.write_points(line_protocol)
        except Exception as e:
            return jsonify({'error': f'{e}'}), 500
    return jsonify()



@app.route('/sokuchi')
def hello():
    car_id = request.args.get('car_id')
    data = list(client.query('SELECT * FROM mobile LIMIT 1'))[0][0]
    sokuchi_x = (data["GRSS_RTK_x"])
    sokuchi_y = (data["GRSS_RTK_y"])
    dt = (data["time"])
    a, b = sokuchi_field.sokuchi_field(sokuchi_x,sokuchi_y)
    field_x = a
    field_y = b
    # time.sleep(10)
    # return jsonify(create_json.create_json(Car_ID, DateTime))
    return jsonify(rrt1.main(car_id, dt, field_x, field_y))

if __name__ == '__main__':
    app.run(**conf['Server'])
