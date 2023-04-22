from flask import Flask
import json
import requests

app = Flask(__name__)

globus_url = "https://transfer.api.globus.org/v0.10/private/web_stats"

initial_values = 

"""
Example:
{
  "new": {
    "bytes": 1955402227052862012,
    "files": 209318008246,
    "time": "2023-04-22 22:47:02.125357"
  },
  "old": {
    "bytes": 1955398391739215761,
    "files": 209317930020,
    "time": "2023-04-22 22:42:01.610209"
  }
}
"""

def get_data(url):
    response = requests.get(url)

    data = response.json()
    json_data = json.dumps(data, indent=2)
    data = json.loads(json_data)

    bytes_value = int(data['new']['bytes'])
    print(f'Returned bytes_value: {bytes_value}')
    bytes_value /= 10 ** 9
    bytes_value %= 10 ** 7
    bytes_value = int(bytes_value)
    print(f'    extracted: {bytes_value}')
    return(bytes_value)

last_value = get_data(globus_url)

@app.route('/')
def hello_world():
    next_value = get_data(globus_url)
    if next_value == last_value:
        next_value += 1
    print(f' Bytes: {next_value}')
    rv = f'{{"number": {next_value}}}'
    print(f'Response: {rv}')
    last_value = next_value
    return rv
