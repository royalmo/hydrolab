from flask import Blueprint, render_template, url_for, redirect, jsonify, make_response, request
from flask_login import current_user
from flask_babel import gettext

from ..extensions import db, login_required, admin_required
from ..models import Sensor, SensorForm, SearchForm, Downlink

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
    return render_template('pages/newsensor.html.j2', title=gettext("New Sensor"), current_user=current_user, sensor=form, new=True, navbar_highlight_sensors=True)

@app.route('/sensor/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    sensor = Sensor.query.get_or_404(id)
    # sensor_history_list = SensorHistory.query.filter_by(id=id).order_by(SensorHistory.timestamp.desc()).limit(10).all()
    sensor_form=SensorForm(obj=sensor)
    sensor_form.hours=sensor.hours_range
    # substitute sensor_form with the value of hours_range such that you can access it
    if sensor_form.is_submitted():
        print(sensor_form)
        if current_user.role == "Admin": # Only admins can edit
            for key, val in sensor_form.data.items():
                print("KEY VAL: ", key, val)
                if key in ['submit', 'csrf_token']: continue
                setattr(sensor, key, val)
            db.session.commit()
        return redirect(url_for('main.map'))
    return render_template('pages/newsensor.html.j2', title=gettext("Edit Sensor"), current_user=current_user, sensor=sensor_form, new=False, id=id, navbar_highlight_sensors=True) #, sensor_history_list=sensor_history_list)

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

@app.route('/sensor/<int:id>/water', methods=['POST'])
@admin_required
def water(id):
    sensor = Sensor.query.get_or_404(id)
    t = Downlink(sensor_id=sensor.id, water_now_seconds=sensor.watering_time)
    db.session.add(t)
    db.session.commit()
    t.send()
    return make_response("Watering Request sent", 200)

@app.route('/sensor/<int:id>/info', methods=['GET', 'POST'])
@admin_required
def info(id):
    sensor = Sensor.query.get_or_404(id)
    return render_template('pages/sensor_information.html.j2', title=gettext("Sensor Information"), current_user=current_user, sensor=sensor, navbar_highlight_sensors=True)

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
