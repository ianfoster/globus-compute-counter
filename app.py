from flask import Flask
import json
import requests

app = Flask(__name__)

globus_url = "https://transfer.api.globus.org/v0.10/private/web_stats"

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

@app.route('/')
def hello_world():
    bytes = get_data(globus_url)
    print(f' Bytes: {bytes}')
    rv = f"{{'number', {bytes}}}"
    print(f'Response: {rv}')
    return rv
