from flask import Blueprint, render_template, url_for, redirect, jsonify, make_response, request
from flask_login import current_user
from flask_babel import gettext

from ..extensions import db, login_required, admin_required
from ..models import Sensor, SensorForm, SearchForm
from app.models.sensor_history import SensorHistory
from datetime import datetime
from requests import put
import os

app = Blueprint('sensors', __name__)

@app.route('/sensors')
@login_required
def sensors():
    search_form = SearchForm(request.form)
    search_query = request.args.get('search')
    if search_query:
        sensors = Sensor.query.filter(Sensor.name.contains(search_query)).all()
    else:
        sensors = Sensor.query.all()
    
    return render_template('pages/sensors.html.j2',
                            sensors=sensors,
                            search_form=search_form,
                            navbar_highlight_sensors=True,
                            title=gettext('Sensors'))


@app.route('/sensor/new', methods=['GET', 'POST'])
@login_required
def newsensor():
    form = SensorForm()

    if form.is_submitted():
        new_sensor = Sensor(**{key : val for key, val in form.data.items() if key not in ['submit', 'csrf_token']})
        db.session.add(new_sensor)
        db.session.commit()
        return redirect(url_for('main.map'))
    return render_template('pages/newsensor.html.j2', title=gettext("New Sensor"), current_user=current_user, sensor=form, new=True)

@app.route('/sensor/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    sensor = Sensor.query.get_or_404(id)
    sensor_history_list = SensorHistory.query.filter_by(id=id).order_by(SensorHistory.timestamp.desc()).limit(10).all()
    sensor_form=SensorForm(obj=sensor)
    if sensor_form.is_submitted():
        print(sensor_form)
        if current_user.role == "Admin": # Only admins can edit
            for key, val in sensor_form.data.items():
                print("KEY VAL: ", key, val)
                if key in ['submit', 'csrf_token']: continue
                setattr(sensor, key, val)
            db.session.commit()
        return redirect(url_for('main.map'))
    return render_template('pages/newsensor.html.j2', title=gettext("Edit Sensor"), current_user=current_user, sensor=sensor_form, new=False, id=id, sensor_history_list=sensor_history_list)

@app.route('/sensor/<int:id>/remove', methods=['GET', 'POST'])
@admin_required
def remove(id):
    Sensor.query.filter(Sensor.id == id).delete()
    db.session.commit()
    return redirect(url_for('main.map'))

@app.route('/sensor/<int:id>/start', methods=['GET', 'POST'])
@admin_required
def start(id):
    Sensor.query.get_or_404(id).start(current_user)
    return make_response("Sensor started", 204)

@app.route('/sensor/<int:id>/stop', methods=['GET', 'POST'])
@admin_required
def stop(id):
    Sensor.query.get_or_404(id).stop(current_user)
    return make_response("Sensor stopped", 204)

@app.route('/sensor/raw')
@login_required
def raw_data():
    Sensor.update_status(all=True)

    sensors = Sensor.query.all()
    #data = [{'id' : server.id, 'status' : server.status} for server in servers]

    #return jsonify(data)

    return

import requests

@app.route('/get_addresses', methods=['POST'])
@login_required
def get_addresses():
    data = request.get_json()
    print("DATA: ", data)
    lat = data['lat']
    lon = data['lon']
    #api_key = os.getenv('GEOAPIFY_KEY')

    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        address = response.json()
    else:
        address = "Address not available"

    return jsonify({'address': address})
