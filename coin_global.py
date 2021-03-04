from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

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
  data1 = json.dumps(result,sort_keys=True,indent=1)
  print("Rank      Name           (Symbol)        Date        price")
  for cryptoc in result['data']:
      rank=cryptoc['id']
      names=cryptoc['name']
      symbol=cryptoc['symbol']
      datea=cryptoc['date_added']
      price=cryptoc['quote']['USD']['price']
    
      print(str(rank)+"  :  "+str(names)+"   :   ("+str(symbol)+")   :   "+str(datea)+"   :   "+str(price))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)