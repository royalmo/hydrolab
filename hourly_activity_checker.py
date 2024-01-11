# This file should be executed every hour (approx).
# It checks if the sensors are receiving uplinks and notifies the admin if not.
from app import app
from app.models import Sensor

with app.app_context():
    for sensor in Sensor.query.all():
        sensor.notify_inactivity()
