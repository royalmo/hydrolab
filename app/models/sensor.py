from ..extensions import db, mailer, notification_manager

from datetime import datetime, timedelta
from flask_babel import gettext

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eui = db.Column(db.String(80))
    name = db.Column(db.String(80))
    description = db.Column(db.String(80), default='')
    location = db.Column(db.JSON)
    inactivity_notification_sent = db.Column(db.Boolean, default=False)

    last_watered_at = db.Column(db.String(80), default="N.A.")
    time_between_waterings = db.Column(db.Integer, default=600)
    watering_time = db.Column(db.Integer, default=10)
    hours_range = db.Column(db.Integer, default=0xFF000F)
    watering_threshold = db.Column(db.Integer, default=30)
    minutes_between_uplinks = db.Column(db.Integer, default=30)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def get_last_uplink(self):
        from .uplink import Uplink
        return Uplink.query.filter(Uplink.sensor_id == self.id).order_by(Uplink.received_at.desc()).first()
    def get_last_downlink(self, received=True):
        from .downlink import Downlink
        return Downlink.query.filter(Downlink.sensor_id == self.id).order_by(Downlink.sent_at.desc()).first()
    
    def process_uplink(self, uplink):
        from .downlink import Downlink

        if uplink.minutes_since_last_watering is not None:
            event_timestamp = datetime.now() - timedelta(minutes=uplink.minutes_since_last_watering)
            self.last_watered_at = event_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()

        template_downlink = Downlink(sensor_id=self.id)
        template_downlink.fill_with_differences()

        if self.should_water_now():
            template_downlink.water_now_seconds = self.watering_time

        # We could set the immediate_uplink flag but overkill?

        if template_downlink.get_payload() != 'Z':
            # not empty message, send it
            db.session.add(template_downlink)
            db.session.commit()
            template_downlink.send()

    def should_water_now(self):
        # Returns true if the sensor should be watered now.
        if self.hours_range is None or not in_hour_range(datetime.now().hour, self.hours_range):
            return False
        
        last_uplink = self.get_last_uplink()
        if last_uplink is None: return False # Impossible case?

        if self.watering_threshold is None or last_uplink.humidity >= self.watering_threshold: return False

        if self.last_watered_at == 'N.A.' or self.time_between_waterings is None: return False

        last_watered_at = datetime.strptime(self.last_watered_at, "%Y-%m-%d %H:%M:%S")
        threshold_time = datetime.now() - timedelta(minutes=self.time_between_waterings)

        return last_watered_at < threshold_time

    def parsed_errors(self):
        from .uplink import Uplink
        errors = []

        hours_without_uplinks = self.hours_since_last_uplink()
        if hours_without_uplinks > 12:
            errors.append(['E', gettext('More than 12h without any uplink!')])
        elif hours_without_uplinks > 2:
            errors.append(['W', gettext('More than 2h without any uplink!')])
        
        # Checking if rebooted or watchdog in the last 5 hours
        recent_uplinks = Uplink.query.filter(Uplink.sensor_id == self.id).filter(Uplink.received_at > (datetime.now() - timedelta(hours=5))).all()
        already_included_errors = []
        for ul in recent_uplinks:
            if '1' in ul.errors and '1' not in already_included_errors:
                already_included_errors.append('1')
                errors.append(['W', gettext('Sensor rebooted recently!')])
            if '2' in ul.errors and '2' not in already_included_errors:
                already_included_errors.append('2')
                errors.append(['W', gettext('Sensor rebooted recently due to WatchDog!')])

        # Battery warning or error
        last_uplink = self.get_last_uplink()
        if last_uplink is not None and '3' in last_uplink.errors:
            errors.append(['W', gettext('Low battery!')])

        return errors

    def hours_since_last_uplink(self):
        uplink = self.get_last_uplink()
        if uplink is None: return 101 # More than 100 hours is considered infinite

        return (datetime.now() - uplink.received_at).total_seconds() / 3600
    
    def notify_inactivity(self):
        if self.inactivity_notification_sent: return
        if self.hours_since_last_uplink() <= 12: return

        self.inactivity_notification_sent = True
        db.session.commit()

        mailer.sensor_inactive(self)
        notification_manager.notify_sensor_inactive(self)

    def has_an_error(self):
        return 'E' in [x[0] for x in self.parsed_errors()]
    
    def has_a_warning(self):
        return 'W' in [x[0] for x in self.parsed_errors()]

def in_hour_range(hour, hour_range):
    # Range is an integer of 24 bits minimum. Each bit represents
    # an hour. For example, 0xFF0000 represents the hours from 0 to 8am.
    # This function returns true if the hour is in the range.
    return (1 << (hour % 24)) & hour_range != 0
