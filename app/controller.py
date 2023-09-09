from time import sleep
from config import Config
from app import dbHandler
from threading import Thread


# Call databasehandler from controller

class Controller:
    """A controller which handles the coordination of asynchronous tasks in separate threads.
    This currently only includes the crawling of stocks data.

    """

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
                
                sleep(Config.STOCK_DATA_REFRESH_INTERVAL)

        return get_data
