from .db import db

def send_to_admins(title, message, role=3):
    # Importing it here so it doesn't give circular import error.
    from ..models import SubscriptionToken, User

    sts = db.session.query(SubscriptionToken)\
        .join(User, User.id == SubscriptionToken.user_id)\
            .filter(User._role >= role)\
            .filter(User.notifications == True).all()
    if len(sts) == 0: return

    for st in sts:
        st.send(title, message)

def notify_new_user(new_user):
    send_to_admins("New user", f"User {new_user.name} just landed, activate their account!")

def notify_sensor_watered(sensor, user):
    send_to_admins("Sensor started", f"Sensor {sensor.name} been manually watered by {user.name}.", role=2)

def notify_sensor_inactive(sensor):
    send_to_admins("Sensor inactive", f"Sensor {sensor.name} is not sending uplinks!", role=2)
