from ..extensions import db
from ..settings import VAPID_PRIVATE, VAPID_SUBJECT
from pywebpush import webpush, WebPushException
import json

class SubscriptionToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def get_user(self):
        from .user import User
        return User.query.get(self.user_id)

    def send(self, title, body):
        #   sub = json.loads(request.form["sub"])

        result = True
        try:
            print(webpush(
                subscription_info = self.data,
                data = json.dumps({
                    "title" : title,
                    "body" : body,
                    #"icon" : "static/i-ico.png",
                    #"image" : "static/i-banner.png"
                }),
                vapid_private_key = VAPID_PRIVATE,
                vapid_claims = { "sub": f"mailto:{VAPID_SUBJECT}" }
            ))
        except WebPushException as ex:
            print(ex)
            result = False
        return result
