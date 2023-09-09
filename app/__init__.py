from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.jsonencoder import DateJSONEncoder

# Start the flask app
app = Flask(__name__)

# Import config properties from config file
app.config.from_object(Config)

# JSON Encoder that is needed for encoding decimal objects for the api.
app.json_encoder = DateJSONEncoder

# Create an instance of SQLAlchemy used throughout the.
db = SQLAlchemy(app, session_options= {
    "expire_on_commit": False
})

# SQLAlchemy Migrate is used to handle changes to a persisting database.
# It automatically writes a protocol of every change in the structure
# of the database and then lets administrators mirror this change to all
# deployments of the app.
migrate = Migrate(app, db)


# Create a new instance of the database handler
from app.database_handler import DatabaseHandler
dbHandler = DatabaseHandler()

from app.controller import Controller
controller = Controller()

# Create a new app module which loads the rest of the app.
from app import routes, models