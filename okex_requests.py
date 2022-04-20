from pydoc import resolve
from textwrap import indent
from turtle import pos
from urllib import response
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

instrument = "BTC-USDT-SWAP"

import timeit
start = timeit.default_timer()

get_inst_price = requests.get("http://www.okex.com/api/v5/market/ticker?instId="+instrument)
respon_lp = get_inst_price.json()["data"][0]["last"]

print(respon_lp)
print("\n")
lp_int_tp = float(respon_lp) + 80
lp_int_sl = float(respon_lp) - 80

place_pos = tradeAPI.place_order(instId=instrument, tdMode='isolated',posSide="long" ,side='buy',ordType='market', sz=1)
print(place_pos)

# get_pos_list = tradeAPI.get_orders(instrument,place_pos["data"][0]["ordId"])
# print(get_pos_list)

place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="sell",posSide="long", ordType="oco", sz="1" , tpTriggerPx = lp_int_tp  ,tpOrdPx = "-1", slTriggerPx = lp_int_sl  ,slOrdPx = "-1")
print(place_algo_order)

stop = timeit.default_timer()

print('Time: ', stop - start)

