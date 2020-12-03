import requests
sample_json = {
  "CarID" : 1,
  "DateTime" : '2020/10/1 10:15:20.223',
  "Position" : {
    "GNSS-RTK" : {
      "Latitude_deg" : 36.1234,
      "Longitute_deg" : 137.332,
      "Quality" : 1
    },
    "WiFi-RTT" : [
      {
        "PoleID" : 1,
        "Distance_m" : 25.333
      },
      {
        "PoleID" : 2,
        "Distance_m" : 5.322
      },
      {
        "PoleID" : 3,
        "Distance_m" : 15.324
      }
    ]
  },
  "Azimuth_deg" : -30,
  "Speed_level" : 5,
  "Steering_level" : 3,
  "ObstacleDistance_m" : 2.432
}

def send(url, data):
    res = requests.post(url, json=data)
    print(res.json())

if __name__ == '__main__':
    host = 'http://127.0.0.1'
    port = 3000
    url = f'{host}:{port}/'
    send(url, sample_json)