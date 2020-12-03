from influxdb import InfluxDBClient, client

ql = '''
SELECT * FROM "mobile"
'''

client = InfluxDBClient(
    host='127.0.0.1',
    port=18086,
    username='root',
    password='root',
    database='IoTPole',
)

data = client.query(ql)
print(data)
