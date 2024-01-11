# Flask settings
DEBUG = True
DEVELOPMENT = True
SECRET_KEY = 'do-i-really-need-this'
SQLALCHEMY_DATABASE_URI = 'sqlite:///hydrolab_db/hydrolab.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SMTP_PASSWORD = ''
SMTP_USERNAME = 'ericroyalmonacid@gmail.com'
WEATHER_API_KEY = ''
VAPID_PRIVATE = ''
# Put this public key also in serviceworker_register.js
VAPID_PUBLIC = ''
VAPID_SUBJECT = 'eric@ericroy.net'
