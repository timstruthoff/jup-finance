from app import app, db, dbHandler, controller
from app.models import User, Transaction, UserCapital, Stock, StockValue, StockShare
from time import sleep

print("Database Test")


print("======== USER DATABASE TEST ========")
kristina = dbHandler.add_user("Kristina Lichte", "kristina.lichte@hpe.com", "Kristina")
max = dbHandler.add_user("Maximilian Kahre", "maximilian.kahre@hpe.com", "Maximilian")
melina = dbHandler.add_user("Melina Petersen", "melina.petersen@hpe.com", "Melina")
sophie = dbHandler.add_user("Sophie Dudeck", "sophie.dudeck@hpe.com", "Sophie")
tim = dbHandler.add_user("Tim Struthoff", "tim.struthoff@hpe.com", "Tim")
print("======== USER DATABASE TEST END ========")
print("")


print("======== LOGIN USER ========")
print("Trying login kristina.lichte@hpe.com, Kristina")
print(f"Login result: {dbHandler.check_login_password('kristina.lichte@hpe.com', 'Kristina')}")

print("Trying login kristina.lichte@hpe.com, WrongPassword")
print(f"Login result: {dbHandler.check_login_password('kristina.lichte@hpe.com', 'WrongPassword')}")

print("Trying login wrong.email@hpe.com, Kristina")
print(f"Login result: {dbHandler.check_login_password('wrong.email@hpe.com', 'Kristina')}")

print("======== LOGIN USER END ========")
print("")

print("======== GET STOCKS ========")
stock1 = Stock.query.get(1)
stock2 = Stock.query.get(2)
stock3 = Stock.query.get(3)

print(f"stock1: {stock1}")
print(f"stock2: {stock2}")
print(f"stock3: {stock3}")

# Kristina buys 3 stocks
dbHandler.buy_stock(kristina, stock1, 3)

# She cannot buy 30000 stocks because of insufficient funds
dbHandler.buy_stock(kristina, stock1, 30000)

# Sell 3 stocks agains
dbHandler.sell_stock(kristina, stock1, 2)
dbHandler.sell_stock(kristina, stock1, 1)

# Cannot sell stock
dbHandler.sell_stock(kristina, stock1, 1)

# Cannot sell stock
dbHandler.sell_stock(kristina, stock2, 1000)


# Get Kristina's stock_shares
dbHandler.buy_stock(kristina, stock1, 3)
dbHandler.buy_stock(kristina, stock2, 1)

kristinas_shares = kristina.stock_shares.all()
print(kristinas_shares)
stockShare1 = kristinas_shares[0]
stockShare1Worth = dbHandler.get_current_share_worth(stockShare1)
print(f"StockShare worth of {stockShare1} is {stockShare1Worth}")

stockShare2 = kristinas_shares[1]
stockShare2Worth = dbHandler.get_current_share_worth(stockShare2)
print(f"StockShare worth of {stockShare2} is {stockShare2Worth}")

print(f"Kristinas stock assets are worth {dbHandler.get_user_stock_asset_worth(kristina)} in total.")

sleep(2)
controller.refreshData()

print(f"Kristinas stock assets are worth {dbHandler.get_user_stock_asset_worth(kristina)} in total.")
