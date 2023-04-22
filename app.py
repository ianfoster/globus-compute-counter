from flask import Flask
import json
import requests
import time

app = Flask(__name__)

globus_url = "https://transfer.api.globus.org/v0.10/private/web_stats"

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
  
cache = {}
cache['earlier_value'] = 0
cache['earlier_time']  = 0
cache['last_value']    = get_data(globus_url)
cache['last_time']     = int(time.time())


# If Globus web counter value hasn't changed, then estimate it to be
#     <time since last reading> * <counter change rate>
# Where:
#     <counter change rate> = <recent change in value> / <recent change in seconds>
#                           = (last_value - earlier_value)/ (last_time - earlier_time))
#

@app.route('/')
def hello_world():
    next_value    = get_data(globus_url)
    next_time     = int(time.time())
    last_value    = cache['last_value']
    last_time     = cache['last_time']
    earlier_value = cache['earlier_value']
    earlier_time  = cache['earlier_time']
    
    if next_value == last_value:  # If no change in web counter
        # Set increment as above
        #  Should check for not first time?
        increment = int( ((this_time - last_time)*(last_value - earlier_value)/(last_time - earlier_time)) * 0.8 )
        print(f'Increment: {increment} ({this_time} - {last_time})*({last_value} - {earlier_value})/({last_time} - {earlier_time}))')
        next_value += increment
    else:
        print(f'Update: {next_value}')

    cache['earlier_value'] = last_value
    cache['earlier_time']  = last_time
    cache['last_value']    = next_value
    cache['last_time']     = next_time
    
    rv = f'{{"number": {next_value}}}'
    return rv
