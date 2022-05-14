import re
from urllib import response
import requests
import okexApi.okex.Trade_api as Trade
import secrets
import time

api = secrets.api()
secret = secrets.secret()
password = secrets.password()
flag = "1"  #demo (1), real(0)


tradeAPI = Trade.TradeAPI(api, secret, password, False, flag)

instrument = "BTC-USDT-SWAP"

import timeit
start = timeit.default_timer()

# get_inst_price = requests.get(f"http://www.okex.com/api/v5/market/ticker?instId={instrument}")
# respon_lp = get_inst_price.json()["data"][0]["last"]

# print(respon_lp)


class Manifest:
    def __init__(self,api, secret, password, flag) :
        self.tradeAPI = Trade.TradeAPI(api, secret, password, False, flag)

    def pos_long(self, instrument, Secure_TP, StopLoss):
        place_pos = self.tradeAPI.place_order(instId=instrument, tdMode="isolated", posSide="long", side="buy", ordType='market', sz=1 )
        place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="sell", posSide="long", ordType="oco", sz="1", tpTriggerPx = Secure_TP, tpOrdPx = "-1", slTriggerPx = StopLoss, slOrdPx = "-1")
        return {"place_pos":place_pos,"place_algo_order":place_algo_order}
        
    def pos_short(self, instrument, Secure_TP, StopLoss):
        place_pos = self.tradeAPI.place_order(instId=instrument, tdMode="isolated", posSide="short", side="sell", ordType='market', sz=1 )
        place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="buy", posSide="short", ordType="oco", sz="1", tpTriggerPx = Secure_TP, tpOrdPx = "-1", slTriggerPx = StopLoss, slOrdPx = "-1")
        return {"place_pos":place_pos,"place_algo_order":place_algo_order}

make_trade = Manifest(api,secret,password,flag)

def send_pos(side, size,secure_tp,stop_loss):

    if side == "long":
        open_long_pos = make_trade.pos_long("BTC-USDT-SWAP", secure_tp, stop_loss)
        return open_long_pos
    elif side == "short":
        open_short_pos = make_trade.pos_short("BTC-USDT-SWAP", secure_tp, stop_loss)
        return open_short_pos
