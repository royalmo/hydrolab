from ..extensions import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.String(80))
    name = db.Column(db.String(80))
    description = db.Column(db.String(80), default=[])
    location = db.Column(db.JSON)
    status = db.Column(db.String, default=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
