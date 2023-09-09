from time import sleep
from config import Config
from app.StockCrawler import StockCrawler
from app.RandomStockDataGenerator import RandomStockDataGenerator
from app import dbHandler
from threading import Thread


# Call databasehandler from controller

class Controller:
    """A controller which handles the coordination of asynchronous tasks in separate threads.
    This currently only includes the crawling of stocks data.

    """

    random_stock_data_generator = RandomStockDataGenerator()
    stock_data_crawler = StockCrawler()

    def __init__(self):
        # get_data = self.get_worker()

        # Start a new thread that is responsible for getting stocks data from the api
        # worker = Thread(target = get_data, daemon = True)
        # worker.start()
        return

    """Get a thread worker function

    :rtype: A :function
    """
    def get_worker(self):

        """Get a thread worker function

        :rtype: A :function
        """
        def get_data():

            """Get new stocks data from an api in an infinite loop."""
            while True:
                print("Getting new stocks data")

                new_stocks_result = None

                if Config.USE_RANDOMLY_GENERATED_STOCK_DATA:
                    new_stocks_result = self.random_stock_data_generator.get_stocks()
                else:
                    new_stocks_result = self.stock_data_crawler.get_stocks_website()
                print(new_stocks_result[0])

                # Loop over the results and add them into the database.
                for stockDataPoint in new_stocks_result:
                    dbHandler.add_stock_crawl_result(
                        wkn = stockDataPoint["wkn"], 
                        company_name = stockDataPoint["company_name"], 
                        value = stockDataPoint["value"], 
                        stock_change_rate = stockDataPoint["stock_change_rate"]
                    )

                sleep(Config.STOCK_DATA_REFRESH_INTERVAL)

        return get_data
