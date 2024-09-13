import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
from win10toast import ToastNotifier
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '10',
    'convert': 'USD'

}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'c9655173-1a69-4300-a3ae-ce9260ed7b6c',
}

session = Session()
session.headers.update(headers)
def fetch_data():
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

def notify_user(symbol,current_price):
    message = f"Price Alert! crypto{symbol} is now {current_price} "
    print(message)
    #windows notification
    my_notification.show_toast("Alert", message)

#coins = data['data']
#printing symbolsv and the price of the coins
#for x in coins:
    #print(x['symbol'],x['quote']['USD']['price'])


    #a csv file to store the data
def csv_file(coins):
  filename = ('cryptocurrencies_prices.csv')

  rows= []

  for coin in coins:
      symbol = coin.get('symbol', )
      price = coin.get('quote', {}).get('USD', {}).get('price', 'N/A')
      timestamp = datetime.now().strftime('%Y -%m-%d %H:%M:%S')
      rows.append({'Timestamp': timestamp, 'Symbol': symbol, 'Price':price})

  df = pd.DataFrame(rows)

  df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)


def main():
    global my_notification
    my_notification = ToastNotifier()


    while True:
        data = fetch_data()
        if data:
            coins = data.get('data',[])
            for coin in coins:
                symbol = coin.get('symbol',)
                price = coin.get('quote',{}).get('USD',{}).get('price','N/A')
                print(f"{symbol} {price} ")

                notify_user(symbol,price)
                csv_file(coins)
        timestamp = datetime.now().strftime('%Y -%m-%d %H:%M:%S')
            #print the time the data was fetched
        print(f"time fetched: {timestamp}")
        time.sleep(15)

#def notify_user(symbol,current_price):
    #print(f"Price Alert! crypto{symbol} is now {current_price} ")
#my_notification = ToastNotifier()
#my_notification.show_toast("Alert", "New Prices Alert")
#time.sleep(15)

if __name__ == "__main__":
    main()