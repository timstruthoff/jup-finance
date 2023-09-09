from app import app, db
from app.models import User, Transaction, UserCapital, Stock, StockValue, StockShare

def make_shell_context():
    with app.app_context():
        return {
            "db": db, 
            "User": User, 
            "Transaction": Transaction,
            "UserCapital": UserCapital, 
            "Stock": Stock, 
            "StockValue": StockValue, 
            "StockShare": StockShare
        }
