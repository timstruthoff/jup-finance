from bs4 import BeautifulSoup
import urllib.request

class StockCrawler:
    """Class responsible for crawling stock data from a website."""

    def get_stocks_website(self):
        """Get Stock Data from a website
        This function crawls data about stock prices from the webiste traderfox.de.
        It then cleans this data up and returns it in a dictionary
        """

        my_url = "https://traderfox.de/aktien/nasdaq-100-bestandteile"
        my_website = urllib.request.urlopen(my_url)
        my_soup = BeautifulSoup(my_website, features="lxml")
        my_dataset = my_soup.find_all("tr")[1:]
        stock_data = []

        for data in range(len(my_dataset)):
            # 1. name
            # 2. wkn
            # 3. value
            # 4. stock_change_rate
            # try-except for missing data

            # add break
            company_name = "Name not found"
            wkn = "wkn not found"
            value = 0
            stock_change_rate = 0
        
            try:
                raw_company_name = my_dataset[data].find("td", {"data-id":"name"}).text
                raw_wkn = my_dataset[data].find("td", {"data-id":"wkn"}).text
                raw_value = my_dataset[data].find("td", {"data-id":"value"}).text
                raw_stock_change_rate = my_dataset[data].find("td", {"data-id":"perf"}).text

                # Clean up values

                company_name = raw_company_name

                wkn = raw_wkn

                raw_value = raw_value[:-1]
                raw_value = raw_value.replace(".","")
                raw_value = raw_value.replace(",",".")
                value = float(raw_value)

                raw_stock_change_rate = raw_stock_change_rate[:-2]
                raw_stock_change_rate = raw_stock_change_rate.replace(".","")
                raw_stock_change_rate = raw_stock_change_rate.replace(",",".")
                stock_change_rate = float(raw_stock_change_rate)

            except:
                print("Stock Parsing Error_" + str(data))

            # print(f"Raw Stock Value: Name: {raw_company_name}, wkn: {rawWkn}, value: {value}, stock_change_rate: {stock_change_rate}")

            # only if successful
            stock_data.append({
                "company_name": company_name,
                "wkn": wkn,
                "value": value,
                "stock_change_rate": stock_change_rate
            })
            
        return stock_data