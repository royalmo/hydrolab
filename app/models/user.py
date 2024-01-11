from ..extensions import db, bcrypt
from flask_login import UserMixin
from babel import Locale

class User(db.Model, UserMixin):

    # Roles defined in a dictionary
    ROLES = {
        "User": 1,
        "Manager": 2,
        "Admin": 3,
    }

    # Reverse lookup dictionary to map role IDs back to role names
    ROLES_REVERSE = {v: k for k, v in ROLES.items()}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    _role = db.Column('role', db.Integer, nullable=False, default=ROLES["User"])
    lang = db.Column(db.String(10), nullable=False, default="en")
    notifications = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def role(self):
        # Return the role name from the role ID
        return self.ROLES_REVERSE.get(self._role, "Unknown Role")

    @role.setter
    def role(self, role_name):
        # Set the role ID based on the role name
        if role_name in self.ROLES:
            self._role = self.ROLES[role_name]
        else:
            raise ValueError("Invalid role name")
    
    def permit(self, permission_level):
        return self._role >= permission_level

    def parsed_lang(self):
        return Locale(self.lang).get_display_name().capitalize()
    
    def update_with_form(self, form, admin=False):
        print(form.notifications)
        user = self
        user.name = form.name.data
        user.email = form.email.data
        user.lang = form.language.data
        if form.password.data and form.password.data == form.password_confirm.data:
            user.password = bcrypt.generate_password_hash(form.password.data)
        if admin and hasattr(form, 'role'):
            # Assuming form.role.data is the role name as a string
            user.role = form.role.data
        user.active = ((not admin) and user.active) or (admin and form.active.data)
        user.notifications = form.notifications.data
        db.session.commit()
