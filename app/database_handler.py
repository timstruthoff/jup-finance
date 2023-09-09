from config import Config
from app import app, db
from app.models import Transaction, Stock
import uuid
import datetime


class DatabaseHandler:
    """A class for handling all interaction with the database.

    """

    def __init__(self):
        self.create_tables()
        if not Config.PERSISTENT_DATABASE:
            self.reset_tables()
        pass
    
    def create_tables(self):
        """Create all missing tables in the database."""
        with app.app_context():
            db.create_all()
            db.session.commit()

    def reset_tables(self):
        """Empty all data from the database."""
        Transaction.query.delete()
        Stock.query.delete()
        db.session.commit()

    def add_stock(self, company_name, current_value):
        """Add a company stock to the database

        Usage::

            >>> db_handler.addStock("871981", "Adobe Inc.", 10000)

        :param wkn: The wkn number of the stock.
        :param company_name: The name of the company.
        :rtype: A :class:`Stock <Stock>`
        """
        
        with app.app_context():
            stock = Stock(company_name = company_name, current_value = current_value)
            db.session.add(stock)
            db.session.commit()
            db.session.expunge(stock)
            return stock

    def get_stock(self, wkn):
        """Get a stock object from the database.

        Usage::

            >>> db_handler.get_stock("871981")

        :param wkn: The wkn number of the stock.
        :rtype: A :class:`Stock <Stock>`
        """
        with app.app_context():
            return Stock.query.filter(Stock.wkn == wkn).first()

    def get_all_stocks(self):
        """Get all stocks objects from the dabase."""
        return Stock.query.all()