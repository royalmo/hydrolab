from ..extensions import db
from . import Uplink, Downlink

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.String(80))
    name = db.Column(db.String(80))
    description = db.Column(db.String(80), default='')
    location = db.Column(db.JSON)

    minutes_since_last_watering = db.Column(db.Integer)
    time_between_waterings = db.Column(db.Integer)
    watering_time = db.Column(db.Integer)
    hours_range = db.Column(db.Integer)
    watering_threshold = db.Column(db.Integer)
    minutes_between_uplinks = db.Column(db.Integer)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def get_last_uplink(self):
        return Uplink.query.where({'sensor_id' : self.id}).order({'received_at' : 'desc'}).first()
    def det_last_downlink(self, received=True):
        return Uplink.query.where({'sensor_id' : self.id}).order({'sent_at' : 'desc'}).first()
