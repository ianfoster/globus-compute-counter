from flask import Flask
import json
import requests
import time

app = Flask(__name__)

globus_url = "https://compute.api.globus.org/v2/stats"

"""
Example:
{"total_function_invocations":21889152}
"""

def get_data(url):
    response = requests.get(url)

    data = response.json()
    json_data = json.dumps(data, indent=2)
    data = json.loads(json_data)

    value = int(data['total_function_invocations'])
    to_show = value
    to_show %= 10 ** 7
    to_show = int(to_show)
    print(f'    extracted: {to_show} from {value}')
    return(to_show)
  
cache = {}
cache['last_value']    = get_data(globus_url)
cache['last_time']     = int(time.time())
"""
cache['earlier_value'] = cache['last_value'] - 1
cache['earlier_time']  = cache['last_time'] - 1
"""
cache['index']         = 0

# If Globus web counter value hasn't changed, then estimate it to be
#     <time since last reading> * <counter change rate>
# Where:
#     <counter change rate> = <recent change in value> / <recent change in seconds>
#                           = (last_value - earlier_value)/ (last_time - earlier_time))
#
# The web counter can stay the same for a while, so this can result in estimates getting ahead of reports. 
# If so, then switch to increasing by just 1 at a time.

@app.route('/')
def hello_world():
    this_value    = get_data(globus_url)
    this_time     = int(time.time())
    last_value    = cache['last_value']
    last_time     = cache['last_time']
    """
    earlier_value = cache['earlier_value']
    earlier_time  = cache['earlier_time']
    """
    index         = cache['index']
    
    # print(f'== Round {cache["index"]}:')
    # print(f'    Old : {earlier_value} at {earlier_time}') 
    # print(f'    Last: {last_value} at {last_time}') 
    # print(f'    New : {this_value} at {this_time}') 
    
    if this_value == last_value:  # If no change in web counter
        # Set increment as above
        print(f'{index}: No change, still {this_value}')
    elif this_value > last_value:
        print(f'{index}: Increase by {this_value-last_value} to {this_value}')
    else:  # this_value < last_value, which should not happen
        print(f'{index}: AHEAD ERROR')
    
    """
    if this_value == last_value:  # If no change in web counter
        # Set increment as above
        increment = int( ((this_time - last_time)*(last_value - earlier_value)/(last_time - earlier_time)) * 0.8 )
        print(f'{index}: No change, so increase by estimated {increment} to {this_value+increment}') # ({this_time} - {last_time})*({last_value} - {earlier_value})/({last_time} - {earlier_time})*0.8')
        this_value += increment
    elif this_value > last_value:
        print(f'{index}: Increase by {this_value-last_value} to {this_value}')
    else:  # this_value < last_value, which means that we increased by too much last time
        this_value = last_value + 1
        print(f'{index}: Ahead, so increment by 1 to  {this_value}')
    
    cache['earlier_value'] = last_value
    cache['earlier_time']  = last_time
    cache['last_value']    = this_value
    cache['last_time']     = this_time
    """
    cache['index']         = cache['index'] + 1
    
    rv = f'{{"number": {this_value}}}'
    return rv
