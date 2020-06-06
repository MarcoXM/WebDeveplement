import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# IMPLEMENT DATABASE URL
# You may need to replace the postgresql data link as you like 
SQLALCHEMY_DATABASE_URI = 'postgresql://sqlmarco:4mysiri@localhost:5432/bookingsite'
