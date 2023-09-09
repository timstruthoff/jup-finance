from datetime import datetime
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import VARCHAR
from config import Config

from app import db
import uuid

def generateUUID():
    return str(uuid.uuid4())

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    amount = db.Column(db.Numeric, nullable = False)
    name = db.Column(db.Text(), nullable = False)
    timestamp = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

class Stock(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    company_name = db.Column(db.Text, nullable = False)
    current_value = db.Column(db.Numeric)
    transactions = db.relationship('Transaction', backref='stock', lazy='dynamic')

    def __repr__(self):
        return '<Stock {}>'.format(self.company_name)
