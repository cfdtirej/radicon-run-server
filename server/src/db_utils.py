import yaml
from influxdb import InfluxDBClient


class IoTPoleDB:

    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        self.client = InfluxDBClient(
            host = config['InfluxDB']['host'],
            port = config['InfluxDB']['port'],
            username = config['InfluxDB']['username'],
            password = config['InfluxDB']['password'],
            database = config['InfluxDB']['database']
        )
    
    def write_data(self, json_data):
        self.client.write_points(json_data)
