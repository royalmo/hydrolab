from ..extensions import db
from datetime import datetime, timedelta

from .sensor_history import SensorHistory
from .sensor import Sensor

class Monitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    # The units of that monitor (Temperature (K), ...)
    label = db.Column(db.String(80), nullable=False)
    # The minimum and maximum value that should be displayed on the graph.
    min_value = db.Column(db.Float, nullable=True)
    max_value = db.Column(db.Float, nullable=True)

    @classmethod
    def get_monitor_data(cls, time_range='24h'):
        monitors = cls.query.all()
        data = []

        # Determine the starting time based on the selected time range
        time_delta = {
            '1h': timedelta(hours=1),
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
        }.get(time_range, timedelta(hours=24))  # Default to 24 hours if no match

        start_time = datetime.utcnow() - time_delta
        print(f"Start time for query: {start_time}")

        # Get all unique sensors with their EUIs and Names
        sensors = db.session.query(SensorHistory.eui, Sensor.name).join(Sensor, SensorHistory.eui == Sensor.eui).distinct().all()

        for monitor in monitors:
            monitor_data = []
            for eui, name in sensors:
                # Get the sensor history for each sensor EUI based on the monitor's key
                # and within the specified time range.
                sensor_history = SensorHistory.query.filter(
                    SensorHistory.eui == eui
                ).order_by(SensorHistory.timestamp.desc()).limit(100)

                sensor_history = SensorHistory.query.filter(
                    SensorHistory.eui == eui,
                    SensorHistory.timestamp >= start_time
                ).order_by(SensorHistory.timestamp.desc()).limit(100)

                x_axis = [history.timestamp.strftime('%Y-%m-%d %H:%M:%S') for history in sensor_history]
                y_axis = [getattr(history, monitor.key) for history in sensor_history]

                # Reverse the lists to have time go from past to present
                x_axis.reverse()
                y_axis.reverse()

                monitor_data.append({
                    'sensor_name': name,  # Use sensor.name instead of sensor_eui
                    'x_axis': x_axis,
                    'y_axis': y_axis
                })

            # Combine all sensor data for the current monitor
            data.append({
                'id': monitor.id,
                'title': monitor.title,
                'key': monitor.key,
                'label': monitor.label,
                'min_value': monitor.min_value if monitor.min_value is not None else 'undefined',
                'max_value': monitor.max_value if monitor.max_value is not None else 'undefined',
                'sensor_data': monitor_data
            })

        return data