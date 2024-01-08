from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import current_user
from flask_babel import gettext

from ..extensions import login_required
from ..models import Uplink, Sensor
from datetime import datetime, timedelta

app = Blueprint('monitors', __name__)

@app.route('/monitoring')
@login_required
def monitoring():
    # Get the time range from the query string, default to 24 hours
    data = get_monitor_data()

    return render_template('pages/monitoring.html.j2',
                           title=gettext("Monitoring"),
                           current_user=current_user,
                           navbar_highlight_monitoring=True,
                           data=data)

@app.route('/monitoring/raw')
@login_required
def monitoring_raw():
    data = get_monitor_data()
    return jsonify(data)

def get_monitor_data():
    data = {'current': datetime.now().isoformat()}

    # Get all sensors, not just those with uplinks
    all_sensors = Sensor.query.all()

    deltas = {
        '1hour' : datetime.now() - timedelta(hours=1),
        '1day'  : datetime.now() - timedelta(days=1),
        '7days' : datetime.now() - timedelta(days=7)
    }

    for delta_name, delta in deltas.items():
        delta_data = {}

        for sensor in all_sensors:
            uplinks = Uplink.query.filter(Uplink.received_at >= delta)\
                .filter(Uplink.sensor_id == sensor.id)\
                .order_by(Uplink.received_at.asc()).all()

            time_axis = [ul.received_at.strftime('%Y-%m-%d %H:%M:%S') for ul in uplinks]
            temperature_axis = [ul.temperature for ul in uplinks]
            humidity_axis = [ul.humidity for ul in uplinks]
            battery_axis = [ul.battery for ul in uplinks]
            rssi_axis = [ul.rssi for ul in uplinks]

            delta_data[sensor.name] = {
                'time': time_axis,
                'temperature': temperature_axis,
                'humidity': humidity_axis,
                'battery': battery_axis,
                'rssi': rssi_axis
            }

        data[delta_name] = delta_data

    return data
