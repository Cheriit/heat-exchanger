from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import io
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/get_liquids')
def get_liquids():
    liquids = [("Water", 4190, 997), ("Linseed oil", 1840, 924), ("Kerosene", 2100, 820)]
    result = []
    for x,y,z in liquids:
        result.append({
            'name': x,
            'heatSpecific': y,
            'density': z
        })

    return jsonify(result)

@app.route('/get_water_temperature')
def get_water_temperature():
    heat_specific = float(request.args.get('heatSpecific'))
    density = float(request.args.get('density'))
    volume = float(request.args.get('startVolume')) / 1000
    startTemp = float(request.args.get('startTemp'))

    efficiency = float(request.args.get('efficiency')) / 100
    power = float(request.args.get('power'))

    timestamp = float(request.args.get('timestamp'))
    temperature_limit = float(request.args.get('targetTemp'))

    mass = volume * density
    y = startTemp
    result = {
        'times': [],
        'temperatures': [startTemp]
    }
    time_current = 0

    while y < temperature_limit:
        y = (power * efficiency * timestamp) / (mass * heat_specific) + y
        result['temperatures'].append(y)
        result['times'].append(round(time_current/60, 2))
        time_current += timestamp

    return jsonify(result)

@app.route('/get_live_simulation')
def get_live_simulation():
    heat_specific = float(request.args.get('heatSpecific'))
    power = float(request.args.get('power'))
    volume_in = float(request.args.get('volIn')) /1000
    volume_out = float(request.args.get('volOut')) /1000
    volume_old = float(request.args.get('startVolume')) /1000
    timestamp = float(request.args.get('timestamp'))
    temperature_limit = float(request.args.get('targetTemp'))
    temperature_current = float(request.args.get('startTemp'))
    temperature_in = float(request.args.get('tempIn'))
    density = float(request.args.get('density'))
    efficiency = float(request.args.get('efficiency')) / 100

    timestamp_hour = timestamp/3600
    volume_current = volume_old-volume_out*timestamp_hour+volume_in*timestamp_hour
    if volume_current > 0:
        temperature_next = ((volume_old-volume_out*timestamp_hour)*temperature_current+volume_in*timestamp_hour*temperature_in)/volume_current
        mass = volume_current * density
        if temperature_next < temperature_limit:
            temperature_2 = (power * efficiency * timestamp) / (mass * heat_specific) + temperature_next
        else:
            temperature_2 = temperature_next
        
    else:
        volume_current = 0
        temperature_2 = 0

    result = {
        'volume': volume_current*1000,
        'temperature': temperature_2
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)