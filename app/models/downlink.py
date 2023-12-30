from ..extensions import db
from datetime import datetime
from .sensor import Sensor

class Downlink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now)

    water_now_seconds = db.Column(db.Integer)

    minutes_since_last_watering = db.Column(db.Integer)
    time_between_waterings = db.Column(db.Integer)
    watering_time = db.Column(db.Integer)
    hours_range = db.Column(db.Integer)
    watering_threshold = db.Column(db.Integer)
    minutes_between_uplinks = db.Column(db.Integer)

    def get_sensor(self):
        return Sensor.query.get(self.sensor_id)
