from flask import Blueprint, request, make_response
from datetime import datetime

from ..extensions import db, auth_header_required
from ..extensions.login_manager import load_user_from_auth_header
from ..models import Sensor, Uplink

import os

app = Blueprint('api', __name__)

########################

# @app.route('/register_token', methods=['POST'])
# @auth_header_required
# def register_token():
#     current_user = load_user_from_auth_header()
#     data = request.get_json()
#     token = data.get('token')

#     FirebaseToken.register_token(current_user, token)

#     return make_response('OK', 200)

# @app.route('/unregister_token', methods=['POST'])
# @auth_header_required
# def unregister_token():
#     current_user = load_user_from_auth_header()
#     data = request.get_json()
#     token = data.get('token')

#     FirebaseToken.unregister_token(current_user, token)

#     return make_response('OK', 200)

########################
    
@app.route('/ttn/uplink', methods=['POST'])
def uplink():
    headersApiKey = request.headers.get('X-Downlink-Apikey')
    ApiKey = os.getenv('X-UPLINK-APIKEY')

    if (ApiKey != headersApiKey):
        return make_response('Forbidden', 403)

    body = request.json
    print(body)

    dev_eui = body['end_device_ids']['device_id']
    sensor = Sensor.query.filter_by(eui=dev_eui)
    if not sensor:
        return make_response('Not found', 404)

    time_trim = body['received_at'][:-4] + "Z"
    timestamp = datetime.strptime(time_trim, "%Y-%m-%dT%H:%M:%S.%fZ")
    payload = body['uplink_message']['decoded_payload']['text']
    # Example payload
    # T24.63H8V0L0M0N0@-1S0E3R0Z
    
    parsed_data = parse_custom_string(payload)
    if not parsed_data:
        print("Invalid input string")
        return make_response('Bad request', 400)

    rx_metadata = body['uplink_message']['rx_metadata'][0]
    rssi = rx_metadata['rssi']
    location = rx_metadata['location']

    uplink = Uplink(sensor_id=sensor.id,
                    received_at=timestamp,

                    humidity=int(parsed_data['H']),
                    battery=int(parsed_data['V']),
                    temperature=float(parsed_data['T']),

                    minutes_since_last_watering = int(parsed_data['@']),
                    time_between_waterings = int(parsed_data['M']),
                    watering_time = int(parsed_data['N']),
                    hours_range = int(parsed_data['R'], base=16),
                    watering_threshold = int(parsed_data['L']),
                    minutes_between_uplinks = int(parsed_data['S']),

                    rssi=rssi)
    db.session.add(uplink)
    sensor.location = location
    db.session.commit()

    return make_response("Created", 201)

def parse_custom_string(input_string):
    # Define individual patterns for each parameter

    current_command = None
    buffer = ""

    found_commands = {
        'T' : None,
        'H' : None,
        'V' : None,
        'R' : None,
        'L' : None,
        '@' : None,
        'S' : None,
        'M' : None,
        'N' : None,
        'E' : None,
        'Z' : None
    }

    payload = input_string
    while len(payload) > 0:
        if payload[0] in found_commands.keys():
            if current_command is not None:
                found_commands[current_command] = buffer
            current_command = payload[0]
            if current_command == 'E':
                found_commands[payload[:2]] = True
                payload = payload[1:]
        else:
            buffer += payload[0]

        payload = payload[1:]

    return found_commands
