# Database initialization, see README.md for more info.
from app import app, db, bcrypt
import sqlite3, os

DEFAULT_PWD = os.environ['NAVLAB_DEFAULT_PASSWORD'] if 'NAVLAB_DEFAULT_PASSWORD' in os.environ else 'root12.$'
ENCRYPTED_DEFAULT_PWD = bcrypt.generate_password_hash(DEFAULT_PWD)

# Remove the database file if it exists
if os.path.exists('app/hydrolab_db/hydrolab.db'):
    os.remove('app/hydrolab_db/hydrolab.db')

# Create app tables
with app.app_context():
    db.create_all()

# Connect to the database and populate them
conn = sqlite3.connect('app/hydrolab_db/hydrolab.db')

with open('db_seed.sql', 'r') as f:
    sql = f.read().format(ENCRYPTED_DEFAULT_PWD.decode('utf-8'))

conn.executescript(sql)
conn.commit()
conn.close()
