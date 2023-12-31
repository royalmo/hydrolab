from ..extensions import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.String(80))
    name = db.Column(db.String(80))
    description = db.Column(db.String(80), default='')
    location = db.Column(db.JSON)

    minutes_since_last_watering = db.Column(db.Integer, default=-1)
    time_between_waterings = db.Column(db.Integer, default=600)
    watering_time = db.Column(db.Integer, default=10)
    hours_range = db.Column(db.Integer, default=0xFF000F)
    watering_threshold = db.Column(db.Integer, default=30)
    minutes_between_uplinks = db.Column(db.Integer, default=30)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def get_last_uplink(self):
        from .uplink import Uplink
        return Uplink.query.where({'sensor_id' : self.id}).order({'received_at' : 'desc'}).first()
    def det_last_downlink(self, received=True):
        from .uplink import Uplink
        return Uplink.query.where({'sensor_id' : self.id}).order({'sent_at' : 'desc'}).first()
