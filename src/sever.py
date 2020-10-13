import os

import yaml
from flask import Flask, jsonify, request

from db_utils import IoTPoleDB


app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    req = request.get_json()
    return req


if __name__ == '__main__':
    with open('config.yaml', 'r') as yf:
        config = yaml.safe_load(yf)
        host = config['Server']['host']
        port = config['Server']['port']

    app.run(host=host, port=port, debug=True)

