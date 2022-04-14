import requests
import base64
import json
import datetime
import okexApi.okex.Trade_api as Trade
import secrets


api = secrets.api()
secret = secrets.secret()
password = secrets.password()
flag = "1"  #demo (1), real(0)


tradeAPI = Trade.TradeAPI(api, secret, password, False, flag)

place_order = tradeAPI.place_order(instId="BTC-USDT", tdMode='cross', side='buy',ordType='limit', sz='0.005', px='2000.00')
get_position = tradeAPI.get

print(place_order)
print("\n")



    