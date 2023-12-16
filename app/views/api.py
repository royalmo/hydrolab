# This file is used to serve Apache-Cordova's font-end.

from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
from requests import put

from ..extensions import db, auth_header_required
from ..extensions.login_manager import load_user_from_auth_header
from ..models import Sensor, FirebaseToken, SensorHistory, Monitor
import os
import re

app = Blueprint('api', __name__)

########################

@app.route('/sensors')
@auth_header_required
def sensors():
    response = [
        {
            "id" : sensor.id,
            "name" : sensor.name,
            "status" : sensor.lastActiveStatus,
            "location": sensor.location
        }
        for server in Sensor.query.all()
    ]
    return make_response(jsonify({'data' : response, 'admin' : load_user_from_auth_header().role == "Admin"}), 200)

@app.route('/monitoring')
@auth_header_required
def monitors():
    return make_response(jsonify({'data' : Monitor.get_monitor_data(), 'admin' : load_user_from_auth_header().role == "Admin"}), 200)

########################

@app.route('/register_token', methods=['POST'])
@auth_header_required
def register_token():
    current_user = load_user_from_auth_header()
    data = request.get_json()
    token = data.get('token')

    FirebaseToken.register_token(current_user, token)

    return make_response('OK', 200)

@app.route('/unregister_token', methods=['POST'])
@auth_header_required
def unregister_token():
    current_user = load_user_from_auth_header()
    data = request.get_json()
    token = data.get('token')

    FirebaseToken.unregister_token(current_user, token)

    return make_response('OK', 200)

########################

@app.route('/sensor/<int:id>/start', methods=['GET', 'POST'])
@auth_header_required
def start(id):
    current_user = load_user_from_auth_header()
    if not current_user.role == "Admin":
        return make_response('Forbidden', 403)

    Sensor.query.get_or_404(id).start(current_user)
    return make_response("Sensor started", 204)

@app.route('/ttn/<string:id>/history', methods=['GET'])
def history(id):

    history = SensorHistory.query.filter_by(eui=id)
    print(history)

    return make_response(history, 200)
    
@app.route('/ttn/uplink', methods=['POST'])
def uplink():
    headersApiKey = request.headers.get('X-Downlink-Apikey')
    ApiKey = os.getenv('X-UPLINK-APIKEY')

    if (ApiKey != headersApiKey):
        return make_response('Forbidden', 403)

    body = request.json
    import json
    print(json.dumps(body, indent=4))
    dev_eui = int(body['end_device_ids']['device_id'][4:], 16)
    sensor = Sensor.query.filter_by(eui=dev_eui)
    if not sensor:
        return make_response('Not found', 404)

    time_trim = body['received_at'][:-4] + "Z"
    timestamp = datetime.strptime(time_trim, "%Y-%m-%dT%H:%M:%S.%fZ")
    payload = body['uplink_message']['decoded_payload']['text']
    
    parsed_data = parse_custom_string(payload)
    if not parsed_data:
        print("Invalid input string")
        return make_response('Bad request', 400)

    rx_metadata = body['uplink_message']['rx_metadata'][0]
    rssi = rx_metadata['rssi']
    snr = rx_metadata['snr']
    location = rx_metadata['location']

    settings = body['uplink_message']['settings']
    bandwidth = settings['data_rate']['lora']['bandwidth']
    frequency = settings['frequency']

    new_history = SensorHistory(eui=dev_eui,
                                timestamp=timestamp,
                                humidity=parsed_data['H'],
                                battery=parsed_data['V'],
                                temperature=parsed_data['T'],
                                bandwidth=bandwidth, 
                                frequency=frequency, 
                                snr=snr, 
                                rssi=rssi)
    db.session.add(new_history)
    db.session.commit()

    return make_response("Sensor updated", 200)

def parse_custom_string(input_string):
    # Define individual patterns for each parameter
    patterns = {
        'T': r'T(\d+(?:\.\d+)?)',
        'H': r'H(\d+)',
        'V': r'V(\d+)',
        'R': r'R([0-9A-Fa-f]{4})',
        'L': r'L(\d+(?:\.\d+)?)',
        '@': r'%@(\d+)',
        'Z': r'Z(\d+)'
    }
    
    result = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, input_string)
        if match:
            # If pattern matches a float (contains a dot), convert to float, otherwise to int
            if '.' in match.group(1):
                result[key] = float(match.group(1))
            else:
                # For the 'R' key, we want the string value
                if key == 'R':
                    result[key] = match.group(1)
                else:
                    result[key] = int(match.group(1))
        else:
            # If no match is found, set the key to None
            result[key] = None

    return result