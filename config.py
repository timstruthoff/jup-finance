import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # The location of the SQLite database file.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    START_CAPITAL = 10000 # The money each user has in their balance at the start of the game.
    PERSISTENT_DATABASE = True # Whether data should be kept after the application is closed.
    STOCK_DATA_REFRESH_INTERVAL = 4 # The time in seconds between each refresh of the stock data.
    SESSION_DURATION = 10 # The amount of hours a user can be able to stay logged in.
    USE_RANDOMLY_GENERATED_STOCK_DATA = False # Whether to use real Stock data from the website traderfox.de or randomly generated data.