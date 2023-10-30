# This file is used to serve Apache-Cordova's font-end.

from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
from requests import put

from ..extensions import db, auth_header_required
from ..extensions.login_manager import load_user_from_auth_header
from ..models import Sensor, FirebaseToken, SensorHistory
from ..models.monitor import get_monitor_data
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
    return make_response(jsonify({'data' : response, 'admin' : load_user_from_auth_header().admin}), 200)

@app.route('/monitoring')
@auth_header_required
def monitors():
    return make_response(jsonify({'data' : get_monitor_data(), 'admin' : load_user_from_auth_header().admin}), 200)

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
    if not current_user.admin:
        return make_response('Forbidden', 403)

    Sensor.query.get_or_404(id).start(current_user)
    return make_response("Sensor started", 204)

@app.route('/ttn/<string:id>/history', methods=['GET'])
def history(id):

    history = SensorHistory.query.filter_by(eui=id)
    print(history)

    return make_response(history, 200)
    
@app.route('/ttn/uplink', methods=['POST'])
async def uplink(id):
    headersApiKey = request.headers.get('x-downlink-apikey')
    ApiKey = os.getenv('X-DOWNLINK-APIKEY')

    if (ApiKey != headersApiKey):
        return make_response('Forbidden', 403)


    body = request.json
    dev_eui = int(body.end_device_ids.dev_eui, 16)
    sensor = Sensor.query.filter_by(eui=dev_eui)
    if not sensor:
        return make_response('Not found', 404)

    timestamp = body.end_device_ids.received_at
    payload = body.decoded_payload.text
    
    
    parsed_data = parse_custom_string(payload)
    if parsed_data:
        print(parsed_data)
    else:
        print("Invalid input string")
        return make_response('Bad request', 400)

    rx_metadata = body.uplink_message.rx_metadata[0]
    rssi = rx_metadata.rssi
    snr = rx_metadata.snr
    location = rx_metadata.location

    settings = body.uplink_message.settings
    bandwidth = settings.data_rate.lora.bandwidth
    frequency = settings.data_rate.frequency

    await SensorHistory.create({eui: dev_eui, 
                                timestamp: timestamp,
                                humidity: parsed_data.H,
                                battery: parsed_data.V,
                                temperature: parsed_data.T,
                                bandwidth: bandwidth, 
                                frequency: frequency, 
                                snr: snr, 
                                rssi: rssi})

    return make_response("Sensor updated", 200)


def parse_custom_string(input_string):
    # Define a regular expression pattern to match the required format
    pattern = r'T(\d+)H(\d+)R([0-9A-Fa-f]{4})L(\d+)%@(\d+)Z'

    # Use regular expressions to extract values from the input string
    match = re.match(pattern, input_string)

    if match:
        # Extract values from the matched groups
        t_value = int(match.group(1))
        h_value = int(match.group(2))
        r_value = match.group(3)
        l_value = float(match.group(4))
        z_value = int(match.group(5))

        # Create a dictionary to store the key-value pairs
        result = {
            'T': t_value,
            'H': h_value,
            'R': r_value,
            'L': l_value,
            '@': z_value
        }
        
        return result
    else:
        # If the input string doesn't match the expected format, return None
        return None