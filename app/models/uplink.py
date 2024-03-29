from ..extensions import db
from datetime import datetime

class Uplink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.now)

    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    battery = db.Column(db.Integer)

    # Errors are single-byte chars
    errors = db.Column(db.String(5))

    minutes_since_last_watering = db.Column(db.Integer)
    time_between_waterings = db.Column(db.Integer)
    watering_time = db.Column(db.Integer)
    hours_range = db.Column(db.Integer)
    watering_threshold = db.Column(db.Integer)
    minutes_between_uplinks = db.Column(db.Integer)

    # Provided by TTN
    rssi = db.Column(db.Integer)

    def get_sensor(self):
        from .sensor import Sensor
        return Sensor.query.get(self.sensor_id)
