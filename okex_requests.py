import okexApi.okex.Trade_api as Trade
import sys
# import okx.Trade_api as Trade
import secrets

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

def tagMaker(Secure_TP,Max_tp):
    if len(Secure_TP) == 7:
        Secure_TP = f"{Secure_TP}0" 
    elif len(Secure_TP) < 7:
        Secure_TP = f"{Secure_TP}.00"
    scTP = Secure_TP.replace(".","x")


    if len(Max_tp) == 7:
        Max_tp = f"{Max_tp}0"
    elif len(Max_tp) < 7:
        Max_tp = f"{Max_tp}.00" 
    mTP = Max_tp.replace(".","x")

    tag = f"{scTP}{mTP}"
    return tag


class Manifest_oco:
    print("log 1")
    def __init__(self,api, secret, password, flag) :
        self.tradeAPI = Trade.TradeAPI(api, secret, password, False, flag)

    def pos_long(self, instrument, Secure_TP, StopLoss, Max_tp):

        tag = tagMaker(Secure_TP,Max_tp)
        print(tag)

        place_pos = self.tradeAPI.place_order(instId=instrument, tdMode="isolated", posSide="long", side="buy", ordType='market', sz=3 )
        place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="sell", posSide="long", ordType="conditional", sz="3", slTriggerPx = StopLoss, slOrdPx = "-1", tag=tag)
        return {"place_pos":place_pos,"place_algo_order":place_algo_order}
        
    def pos_short(self, instrument, Secure_TP, StopLoss, Max_tp):

        tag = tagMaker(Secure_TP,Max_tp)
        print(tag)

        place_pos = self.tradeAPI.place_order(instId=instrument, tdMode="isolated", posSide="short", side="sell", ordType='market', sz=3 )
        place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="buy", posSide="short", ordType="conditional", sz="3", slTriggerPx = StopLoss, slOrdPx = "-1", tag=tag)
        return {"place_pos":place_pos,"place_algo_order":place_algo_order}

make_oco_trade = Manifest_oco(api,secret,password,flag)

def send_oco_pos(side, size,secure_tp,stop_loss,max_tp):

    if side == "long":
        open_long_pos = make_oco_trade.pos_long("BTC-USDT-SWAP", secure_tp, stop_loss, max_tp)
        return open_long_pos
    elif side == "short":
        open_short_pos = make_oco_trade.pos_short("BTC-USDT-SWAP", secure_tp, stop_loss, max_tp)
        return open_short_pos
