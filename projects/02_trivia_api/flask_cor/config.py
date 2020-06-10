import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
DATABASE = "postgresql"
USERNAME = "marco"
PASSWORD = ":" + "123456"
HOST = "localhost"
PORT = "5432"
DBNAME = "bookstore"

# IMPLEMENT DATABASE URL
# You may need to replace the postgresql data link as you like 
SQLALCHEMY_DATABASE_URI = f'{DATABASE}://{USERNAME}{PASSWORD}@{HOST}:{PORT}/{DBNAME}'



