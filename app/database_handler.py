from config import Config
from app import app, db
from app.models import Session, User, Transaction, UserCapital, Stock, StockValue, StockShare
from app.password_hash_utility import PasswordHashUtility
import uuid
import datetime


class DatabaseHandler:
    """A class for handling all interaction with the database.

    """

    password_hash_utility = PasswordHashUtility()

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
        User.query.delete()
        Transaction.query.delete()
        UserCapital.query.delete()
        Stock.query.delete()
        StockValue.query.delete()
        StockShare.query.delete()
        db.session.commit()

    def add_stock(self, wkn, company_name):
        """Add a company stock to the database

        Usage::

            >>> db_handler.addStock("871981", "Adobe Inc.", 10000)

        :param wkn: The wkn number of the stock.
        :param company_name: The name of the company.
        :rtype: A :class:`Stock <Stock>`
        """
        with app.app_context():
            stock = Stock(wkn = wkn, company_name = company_name)
            db.session.add(stock)
            db.session.commit()
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

    def add_stock_crawl_result(self, wkn, company_name, value, stock_change_rate):
        """Add the result of a website crawl to the database.
        The method checks whether the company is already listed in the database and then adds the
        current value to its record.

        Usage::

            >>> db_handler.add_stock_crawl_result("871981", "Adobe Inc.", 10000, 466.298, 1.17)

        :param wkn: The wkn number of the stock.
        :param company_name: The name of the company.
        :param value: The current value as a clean float number
        :param stock_change_rate: The most recent change in percent.
        :rtype: A :class:`Stock <Stock>`
        """
        with app.app_context():
            stock = self.get_stock(wkn)

            if stock == None:
                stock = self.add_stock(wkn, company_name)

            stock_value = StockValue(value = value, stock_change_rate = stock_change_rate)
            db.session.add(stock_value)
            
            stock.values.append(stock_value)
            stock.current_value = value
            stock.current_change_rate = stock_change_rate
            
            db.session.commit()

    def get_stocks_data(self):
        """Get the current stocks data from the database.


        :rtype: A collection of dictionaries, each describing the stock of one company
        """

        all_stocks = self.get_all_stocks()

        returnList = []

        for current_stock in all_stocks:
            returnList.append({
                "company_name": current_stock.company_name,
                "wkn": current_stock.wkn,
                "value": current_stock.current_value,
                "stock_change_rate": current_stock.current_change_rate
            })


        return returnList

    def get_all_stocks(self):
        """Get all stocks objects from the dabase."""
        return Stock.query.all()

    def get_user_by_email(self, email):
        """Get the user with the specified email address.
        The email address uniquly identifies users.


        :param email: The email address of the user.
        :rtype: A :class:`User <User>`
        """

        print("===== get_user =====")
        print("Arguments:")
        print(f"email: {email}")
        result = User.query.filter(User.email == email).first()

        print(f"Result: {result}")

        return result

    def check_login_password(self, email, password):
        """Check whether a combination of email address and password is a valid set of credentials


        :param email: The email address of the user.
        :param password: The password in clear type. This password is then hashed.
        :rtype: A :class:`User <User>`
        """

        print("===== get_user =====")
        print("Arguments:")
        print(f"email: {email}")


        user = self.get_user_by_email(email)

        if user == None:
            raise Exception("User not found")
        else:
            user_password_hash = user.password
            if self.password_hash_utility.check_password(password, user_password_hash):
                print("Password valid")
                return user
            else:
                raise Exception("Password invalid")
        
    def create_session(self, user):
        """Create a temporary session for the user.


        :param user: The user for whom the session shall be created.
        :rtype: A :class:`Session <Session>`
        """
        session = Session(id = str(uuid.uuid4()), user = user)
        db.session.add(session)
        db.session.commit()
        return session

    def check_session(self, session_id):
        """Check whether there is a session with the session id and whether it is still valid.


        :param session_id: An id of a session
        :rtype: A boolean, true if the session is valid, false if not.
        """

        if session_id == None or session_id == "":
            return False

        # Try to find the session in the database
        session = Session.query.filter(Session.id == session_id).first()

        if session == None:
            return False

        # Check if the session is older than 10 hours and thus expired.
        print(f"creation_date: {datetime.datetime.now()}")
        expiry_date = session.creation_date + datetime.timedelta(hours = Config.SESSION_DURATION)
        print(f"expiry_date: {expiry_date}")

        print(expiry_date < datetime.datetime.now())

        if (session == None):
            return False
        else:
            if expiry_date > datetime.datetime.now():
                return True
            else:
                return False

    def get_user_from_session(self, session_id):
        """Get the user that is associated with a session.


        :param session_id: An id of a session
        :rtype: A :class:`User <User>`
        """

        session = Session.query.filter(Session.id == session_id).first()

        if session == None:
            return None

        else:
            return session.user

    def add_user(self, username, email, password):
        """Add a user to the database

        Usage::

            >>> db_handler.add_user("Evans Hills", "evans.hills@mail.com", "very-secure123")

        :param username: A display name for the user. This is usually the first and last name separated by a space.
        :param email: The email address of the user
        :param password: The password in clear type. This password is then hashed and stored in the database.
        :rtype: A :class:`User <User>`
        """

        print("===== Add User =====")
        print("Arguments:")
        print(f"Username: {username}, email: {email}")

        hashed_password = self.password_hash_utility.get_hashed_password(password)
        print(f"Hashed Password: {hashed_password}")

        new_user_capital = UserCapital()

        new_user = User(
            username = username, 
            email = email, 
            password = hashed_password, 
            capital = new_user_capital 
        )

        

        db.session.add(new_user)
        db.session.add(new_user_capital)
        db.session.commit()

        return new_user

    def buy_stock(self, user, stock, amount):
        """Buy a stock share for a user.
        May raise an exception if the user is not able to buy the stock share.

        Usage::

            >>> db_handler.buy_stock(evans_hills, adobe, 3)

        :param user: The object of the user that should buy the stock
        :param stock: The object of the stock that should be bought
        :param amount: The amount of stock shares to buy.
        """

        print("===== BUY STOCK =====")
        print("Arguments:")
        print(f"User: {user}, stock: {stock}, amount: {amount}")

        # Check all parameters for validity.
        if user == None:
            raise Exception("Invalid parameters: User is None!")

        if stock == None:
            raise Exception("Invalid parameters: Stock is None!")

        if amount == None:
            raise Exception("Invalid parameters: Amount is None!")

        if amount < 1:
            raise Exception("Invalid parameters: Amount is smaller than 1!")
        
        # Get the available balance of the user
        available_balance = self.get_user_balance(user)
        print(f"Available balance: {available_balance}")

        # Calculate hoe much money is required to buy the stocks.
        required_balance = amount * stock.current_value
        print(f"required_balance: {required_balance}")

        # Check whether the user has enough money to buy the stocks.
        if required_balance <= available_balance:
            print("User can buy stock")

            # Reduce the user's money balance by the amount required to buy the stocks. 
            user.capital.balance = user.capital.balance - required_balance
            print(f"Reduced user balance to {user.capital.balance}")

            # Search for a share for the user and stock. A share specifies 
            # how many stocks a user owns of a specific company.
            share = StockShare.query.filter(StockShare.stock == stock, StockShare.user == user).first()

            # If there is no share, create one.
            if (share == None):
                share = StockShare(amount = 0, stock = stock, user = user)

            # Increase the amount of stocks in the share by the amount 
            # the user bought. 
            share.amount = share.amount + amount

            print(f"Increased share amount to {share.amount}")

            # Create a record of the transaction
            transaction = Transaction(
                stock = stock, 
                user = user, 
                amount = amount, 
                value = stock.current_value * amount * (-1),
                user_balance = user.capital.balance,
                type = "buy"
            )

            # Write all changes to the Database.
            db.session.add(transaction)

            print(f"Values stock value: {stock.current_value}, amount: {amount}, cvalue: {stock.current_value * amount * (-1)}, balance: {user.capital.balance}")

            db.session.commit()

        else:
            raise Exception(f"You do not have sufficient funds to buy {amount} stocks of {stock.company_name}")

        print("Buying process completed")

    def sell_stock(self, user, stock, amount):
        """Sell a stock share for a user.
        May raise an exception if the user is not able to sell the stock share.

        Usage::

            >>> db_handler.sell_stock(evans_hills, adobe, 3)

        :param user: The object of the user that should sell the stock
        :param stock: The object of the stock that should be sold
        :param amount: The amount of stock shares to sell.
        """

        print("===== SELL STOCK =====")
        print("Arguments:")
        print(f"User: {user}, stock: {stock}, amount: {amount}")

        if user == None:
            raise Exception("Invalid parameters: User is None!")

        if stock == None:
            raise Exception("Invalid parameters: Stock is None!")

        if amount == None:
            raise Exception("Invalid parameters: Amount is None!")

        if amount < 1:
            raise Exception("Invalid parameters: Amount is smaller than 1!")

        share = StockShare.query.filter(StockShare.stock == stock, StockShare.user == user).first()
        
        if share != None:
            available_stocks = share.amount
            print(f"Available stocks: {available_stocks}")

            if amount <= available_stocks:
                print("User can sell stock")

                share.amount = share.amount - amount

                print(f"Reduced share amount to {share.amount}")

                stock_sell_worth = stock.current_value * amount
                print(f"Current worth of the stocks to sell is {stock_sell_worth}")

                user.capital.balance = user.capital.balance + stock_sell_worth
                print(f"Increased user balance to {user.capital.balance}")

                transaction = Transaction(
                    stock = stock, 
                    user = user, 
                    amount = amount,
                    value = stock.current_value * amount,
                    user_balance = user.capital.balance,
                    type = "sell"
                )

                db.session.add(transaction)

                db.session.commit()

            else:
                raise Exception(f"You do not own enough {stock.company_name} stock!")

            print("Selling process completed")

        else:
            raise Exception(f"You do not own any {stock.company_name} stock!")

    def get_current_share_worth(self, stock_share):
        """Calculate the worth of a stock share
       
        :param stock_share: The stock share to calculate the worth of.
        :rtype: A float indicating the current total worth. 0 if the share does not exist.
        """

        
        if stock_share != None:
            return stock_share.amount * stock_share.stock.current_value
        
        return 0

    def get_users_stocks(self, user):
        """Get a collection with data about stocks owned by a user,
        Example:
        [
            {
                "company_name": "Adobe Inc.",
                "wkn": "871981",
                "value": 467.615,
                "stock_change_rate": 1.45,
                "ownedAmount": 21
            },
            ...
        ]
       
        :param user: A user object
        :rtype: A collection of dictionaries with stocks data
        """

        return_list = []

        shares = user.stock_shares

        # Iterate over all stock shares
        for share in shares:
            stock = share.stock

            if share.amount > 0:
                return_list.append({
                    "company_name": stock.company_name,
                    "wkn": stock.wkn,
                    "value": stock.current_value,
                    "stock_change_rate": stock.current_change_rate,
                    "ownedAmount": share.amount
                })
            
        return return_list
        
    def get_user_history(self, user):
        """Get a collection with data about the transaction history of a user.
        Example:
        [
            { 
                "date": 2020-11-17 18:12:43.574377,
                "company_name": "Adobe Inc",
                "type": "buy",
                "value": 4674.38,
                "balance": 5325.62,
            },
            ...
        ]
       
        :param user: A user object
        :rtype: A collection of dictionaries with transaction data
        """

        return_list = []

        transactions = Transaction.query.filter(Transaction.user == user).all()

        for transaction in transactions:
            return_list.append({
                "date": transaction.timestamp,
                "company_name": transaction.stock.company_name,
                "type": transaction.type,
                "value": transaction.value,
                "balance": transaction.user_balance
            })

        return return_list

    def reset_user(self, user):
        """Reset all data of a user
       
        :param user: A user object
        """
        print(f"Start capital is {Config.START_CAPITAL}")

        user.capital.balance = Config.START_CAPITAL

        StockShare.query.filter(StockShare.user == user).delete()
        Transaction.query.filter(Transaction.user == user).delete()
        db.session.commit()

    def get_user_stock_asset_worth(self, user):
        """Get the total worth of a user's stock assets.
       
        :param user: A user object
        :rtype: A float indicating the total worth.
        """
        user_shares = user.stock_shares.all()
        sum = 0

        for current_share in user_shares:
            sum += self.get_current_share_worth(current_share)

        return sum

    def get_user_balance(self, user):
        """Get the current balance of equity of a user."""
        return user.capital.balance

    def get_user_yield(self, user):
        """Get the current yield of equity of a user. Yield is the profit divided by the starting capital.
        """

        return (self.get_user_profit(user) / Config.START_CAPITAL) * 100
        

    def get_user_key_figures(self, user):

        equity = self.get_user_balance(user)
        assets = self.get_user_stock_asset_worth(user)
        profit = equity + assets - Config.START_CAPITAL
        current_yield = (equity / Config.START_CAPITAL) * 100
        total_assets = equity + assets

        returnValue = {
            "total_assets": total_assets,
            "equity": equity, 
            "assets": assets, 
            "profit": profit, 
            "current_yield": current_yield
        }
        print(returnValue)

        return returnValue