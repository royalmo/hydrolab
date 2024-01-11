from flask import Blueprint, render_template, url_for, redirect, request, make_response, send_from_directory, jsonify
from flask_login import current_user
from ..extensions import login_required
from flask_babel import gettext

from .users import app as users_view
from .sensors import app as sensors_view
from .monitors import app as monitors_view
from .api import app as api_view
from ..models import Sensor, SearchForm
import json

app = Blueprint('main', __name__)
app.register_blueprint(users_view, url_prefix='')
app.register_blueprint(sensors_view, url_prefix='')
app.register_blueprint(monitors_view, url_prefix='')
app.register_blueprint(api_view, url_prefix='')

@app.route('/')
def index():
    return redirect(url_for('.map'))

@app.route('/map', methods=['GET'])
@login_required
def map():
    sensors = Sensor.query.all()
    sens = []
    center_lat = request.args.get('lat')
    center_lon = request.args.get('lon')
    center = []
    if (center_lat and center_lon):
        center = [center_lat, center_lon]
    for sensor in sensors:
        sens.append(sensor)
    
    return render_template('pages/map.html.j2', sensors=sens, center=center, navbar_highlight_map=True)
    

@app.route('/serviceworker.js')
def service_worker():
    response = make_response(send_from_directory('static/js/','serviceworker.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

# (A2) FLASK SETTINGS + INIT - CHANGE TO YOUR OWN!
VAPID_SUBJECT = "mailto:your@email.com"
VAPID_PRIVATE = "YOUR-PRIVATE-KEY"

# (B3) PUSH DEMO
@app.route("/subscribe", methods=["POST"])
@login_required
def push():
    # (B3-1) GET SUBSCRIBER
    sub = json.loads(request.form["sub"])
    current_user.new_subscription(sub)
    return 'OK'
