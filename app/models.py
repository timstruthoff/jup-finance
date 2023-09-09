from datetime import datetime
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import VARCHAR
from config import Config

from app import db
import uuid

def generateUUID():
    return str(uuid.uuid4())

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(255), index = True, nullable = False)
    email = db.Column(db.String(255), index = True, unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    capital = db.relationship('UserCapital', uselist = False, backref='user')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    stock_shares = db.relationship('StockShare', backref='user', lazy='dynamic')
    session = db.relationship('Session', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Session(db.Model):
    id = db.Column(VARCHAR(255), primary_key = True, default = lambda: str(uuid.uuid4()), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return '<Session {}>'.format(self.id)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    amount = db.Column(db.Integer(), nullable = False)
    type = db.Column(db.Text(), nullable = False)
    timestamp = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Numeric, nullable = False)
    user_balance = db.Column(db.Numeric, nullable = False)

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

class UserCapital(db.Model):
    id = db.Column(db.Integer,    nullable = False, primary_key = True)
    balance = db.Column(db.Numeric,    nullable = False, default = Config.START_CAPITAL)
    stockassets = db.Column(db.Numeric,    nullable = False, default = 0.0) # Try to remove
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<UserCapital {}>'.format(self.id)

class Stock(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    wkn = db.Column(db.Text, nullable = False)
    company_name = db.Column(db.Text, nullable = False)
    current_value = db.Column(db.Numeric)
    current_change_rate = db.Column(db.Numeric)
    values = db.relationship('StockValue', backref='stock', lazy='dynamic')
    stock_shares = db.relationship('StockShare', backref='stock', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='stock', lazy='dynamic')

    def __repr__(self):
        return '<Stock {}>'.format(self.company_name)

class StockValue(db.Model):

    id = db.Column(db.Integer, nullable = False, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    value = db.Column(db.Numeric)
    stock_change_rate = db.Column(db.Numeric)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __repr__(self):
        return '<StockValue {}>'.format(self.timestamp)

class StockShare(db.Model):
    id = db.Column(db.Integer,    nullable = False, primary_key = True)
    amount = db.Column(db.Integer,    nullable = False, default = 0)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<StockShare {}>'.format(self.id)