from .firebase import get_bearer_token, send_notification
from .db import db

def send_to_admins(title, message, role=3):
    # Importing it here so it doesn't give circular import error.
    from ..models import FirebaseToken, User

    fts = db.session.query(FirebaseToken).join(User, User.id == FirebaseToken.user_id).filter(User.admin == True).all()
    if len(fts) == 0: return

    server_token = get_bearer_token()
    for ft in fts:
        client_token = ft.token
        r = send_notification(title, message, client_token, server_token)
        if not r: # Failed to deliver notification, remove FT.
            db.session.delete(ft)

    db.session.commit()

def notify_new_user(new_user):
    send_to_admins("New user", f"User {new_user.name} just landed, activate their account!")

def notify_sensor_watered(sensor, user):
    send_to_admins("Sensor started", f"Sensor {sensor.name} been manually watered by {user.name}.", role=2)

def notify_sensor_inactive(sensor):
    send_to_admins("Sensor inactive", f"Sensor {sensor.name} is not sending uplinks!", role=2)
