from ..extensions import db
from datetime import datetime

class SensorHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    humidity = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    battery = db.Column(db.Integer)
    bandwidth = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    snr = db.Column(db.Integer)
    rssi = db.Column(db.Integer)

    def get_sensor(self):
        return Sensor.query.get(self.eui)

