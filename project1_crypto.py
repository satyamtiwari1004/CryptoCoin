import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore,Back,Style,init
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
    def getkey(self,value):
      list1=list(self.values())
      key1= list1.index(value)
      key2=list(self.keys())
      return key2[key1]
  
# Main Function 
url_pairs = my_dictionary() 
  

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'25',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'b98ac4cb-8efa-4994-81e6-ef59cd3b4205',
}

session = Session()
session.headers.update(headers)
try:
  response = session.get(url, params=parameters)
  result=response.json()
  for crypto in result['data']:
      rank=crypto['id']
      symbol1=crypto['symbol']
      price=crypto['quote']['USD']['price']
      url_pairs.add(rank,symbol1)
  print()
  print("My Portfolio")
  print()

  portfolio_value=0.
  last_update=0
  table=PrettyTable(['Asset','Amount Owned',parameters['convert']+' Value','Price','1h','24h','7d'])
  with open("portfolio_text") as inp:
      for line in inp:
          ticker,amount=line.split()
          ticker=ticker.upper()
          
          rank1=url_pairs.getkey(ticker)
          parameters1 = {
              'start':str(rank1),
              'limit':'1',
              'convert':'USD'
              }
          
          session1 = Session()
          session1.headers.update(headers)
          response1=session1.get(url,params=parameters1)
          result1=response1.json()
          crypto1=result1['data'][0]
          rank=crypto1['id']
          name=crypto1['name']
          symbol=crypto1['symbol']
          last_updated = crypto1['last_updated']
          symbol = crypto1['symbol']
          quotes = crypto1['quote']['USD']
          hour_change = float(quotes['percent_change_1h'])
          day_change = float(quotes['percent_change_24h'])
          week_change = float(quotes['percent_change_7d'])
          price = quotes['price']
          value = float(price) * float(amount)
          init()
          if hour_change > 0:
              hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
          else:
              hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

          if day_change > 0:
              day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
          else:
              day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

          if week_change > 0:
              week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
          else:
              week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

          portfolio_value += value

          value_string = '{:,}'.format(round(value,2))

          table.add_row([name + ' (' + symbol + ')',
                        amount,
                        '$' + value_string,
                        '$' + str(round(price,5)),
                        str(hour_change),
                        str(day_change),
                        str(week_change)])

      print(table)
      print()

      portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
      #last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

      print('Total Portfolio Value: ' + Back.GREEN + '$' + portfolio_value_string + Style.RESET_ALL)
      print()
      print('API Results Last Updated on ' + last_updated)
  print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)