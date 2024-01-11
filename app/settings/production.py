# Flask settings
DEBUG = False
DEVELOPMENT = False
SECRET_KEY = 'please-change-this-in-prod'
SQLALCHEMY_DATABASE_URI = 'sqlite:///hydrolab_db/hydrolab.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SMTP_PASSWORD = ''
SMTP_USERNAME = 'ericroyalmonacid@gmail.com'
WEATHER_API_KEY = ''
VAPID_PRIVATE = ''
# Put this public key also in serviceworker_register.js
VAPID_PUBLIC = 'BKnamwulEZy2ioRbctK0aehcQU2WH3j76MVtpt8hXzLvRp-UQKYMLl5IfzGF4u6nAu3beet3amCeWFrESxJLIyE'
VAPID_SUBJECT = 'eric@ericroy.net'

DOWNLINK_APIKEY=""
UPLINK_APIKEY=""
