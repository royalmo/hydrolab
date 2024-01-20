from ..extensions import db
from ..settings import DOWNLINK_APIKEY
from datetime import datetime
from requests import post
from os import environ
import base64

class Downlink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    sent_at = db.Column(db.DateTime, default=None)
    ack_at = db.Column(db.DateTime, default=None)

    water_now_seconds = db.Column(db.Integer)

    time_between_waterings = db.Column(db.Integer)
    watering_time = db.Column(db.Integer)
    hours_range = db.Column(db.Integer)
    watering_threshold = db.Column(db.Integer)
    minutes_between_uplinks = db.Column(db.Integer)

    immediate_uplink = db.Column(db.Boolean, default=False)

    def get_sensor(self):
        from .sensor import Sensor
        return Sensor.query.get(self.sensor_id)
    
    def get_payload(self):
        result = ''

        if self.water_now_seconds is not None:
            result += f'W{self.water_now_seconds}'
        if self.time_between_waterings is not None:
            result += f'M{self.time_between_waterings}'
        if self.watering_time is not None:
            result += f'N{self.watering_time}'
        if self.hours_range is not None:
            result += f'R{hex(self.hours_range)[2:]}'
        if self.watering_threshold is not None:
            result += f'L{self.watering_threshold}'
        if self.minutes_between_uplinks is not None:
            result += f'S{self.minutes_between_uplinks}'
        if self.immediate_uplink:
            result += 'Y1'

        return result + 'Z'
    
    def acknowledge_now(self):
        self.ack_at = datetime.now()
        db.session.commit()

    def send(self):

        url = f'https://hydrolab.eu2.cloud.thethings.industries/api/v3/as/applications/hydrolab/webhooks/hydrolab/devices/{self.get_sensor().eui}/down/replace'

        headers = {
            'Authorization': f'Bearer {DOWNLINK_APIKEY}',
            'Content-Type': 'application/json'
        }

        payload = self.get_payload()
        if payload == 'Z': return 418
        base64_payload = base64.b64encode(payload.encode('ASCII')).decode('utf-8')

        data = {
            'downlinks': [{
                'frm_payload': base64_payload,
                'f_port': 1,
                'priority': 'NORMAL',
                'confirmed' : True,
            }]
        }

        response = post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.sent_at = datetime.now()
            if self.water_now_seconds is not None and self.water_now_seconds > 0:
                self.get_sensor().last_watered_at = datetime.now()
            db.session.commit()

        return response.status_code
    
    def fill_with_differences(self, uplink):
        ATTRIBUTES = [
            'time_between_waterings',
            'watering_time',
            'hours_range',
            'watering_threshold',
            'minutes_between_uplinks',
            ]
        
        sensor = self.get_sensor()
        for attribute in ATTRIBUTES:
            sensor_attr = getattr(sensor, attribute)
            uplink_attr = getattr(uplink, attribute)

            if sensor_attr is not None and uplink_attr is not None and sensor_attr!=uplink_attr:
                setattr(self, attribute, sensor_attr)
