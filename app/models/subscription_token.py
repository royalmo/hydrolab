from ..extensions import db

class SubscriptionToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(20), default='fcm')
    token = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def get_user(self):
        from .user import User
        return User.query.get(self.user_id)
    
    @classmethod
    def register_token(model, current_user, token):
        st = model.query.filter(model.token == token).first()
        if not st:
            st = model(user_id=current_user.id, token=token)
            db.session.add(st)
        else:
            st.user_id = current_user.id

        db.session.commit()

    @classmethod
    def unregister_token(model, current_user, token):
        st = model.query.filter(model.token == token).first()

        # Preventing someone deleting randomly tokens
        if st and st.user_id == current_user.id:
            db.session.delete(st)

        db.session.commit()
