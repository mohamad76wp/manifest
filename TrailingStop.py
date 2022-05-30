
import time
import okx.Trade_api as Trade
import okx.Market_api as Market

import secrets

from timeit import default_timer as timer
from datetime import timedelta

api = secrets.api()
secret = secrets.secret()
password = secrets.password()
flag = "1"  #demo (1), real(0)
instrument = "BTC-USDT-SWAP"


tradeAPI = Trade.TradeAPI(api, secret, password, False, flag)
marketAPI = Market.MarketAPI(api, secret, password, False, flag)

def Get_ticker_price(instrument): # Get last price form order book
    get_market_price = marketAPI.get_ticker(instrument)
    last_px = get_market_price["data"][0]["last"]

    return last_px


def Get_algo_order_list(): # Returns a list of pending algo orders 
    get_algo_pending = tradeAPI.order_algos_list("conditional",instType="SWAP")
    algo_ord_list = get_algo_pending["data"]

    if len(algo_ord_list) != 0:
        return algo_ord_list
    else:
        return "[algo order list is empty!]"


def Trailing_calc(algo_order,last_px):
    slTriggerPx = algo_order["slTriggerPx"]
    posSide = algo_order["posSide"]
    tag = algo_order["tag"]
    secure_TP = float(algo_order["tag"][:8].replace("x","."))
    Max_tp = float(algo_order["tag"][8:].replace("x","."))

    mxTP_scTP = ((Max_tp - secure_TP)*40)/100
    safe_level = Max_tp - mxTP_scTP
    margin = ((last_px - safe_level)/last_px)*100
    margin = "{:.2f}".format(margin)
    print(f"safe_level: {safe_level}")
    print(f"tag:{posSide}--{tag}")
    print(f"margin(sfelvl): {margin}")

    # compare is the market price is in safe level for trailing the stop loss
    if posSide == "long": # Long side checking
        if last_px >= safe_level:
            slTriggerPx = secure_TP
            print("[^Tp^]")
            return f"new sl: {slTriggerPx}"

        else: 
            return "[^No changes^]"

    else: # Long side checking
        if last_px <= safe_level:
            slTriggerPx = secure_TP
            print("[<Tp>]")
            return f"new sl: {slTriggerPx}"


        else: 
            return "[<No changes>]"        

def Place_new_stopLoss(New_slTriggerPx,algo_order,): # Place new algo order for trail a stoploss and cancel old stoploss
    place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="buy", posSide="short", ordType="conditional", sz=algo_order["sz"], slTriggerPx=New_slTriggerPx, slOrdPx = "-1", tag=algo_order["tag"])
    cancel_algo_order = tradeAPI.cancel_algo_order([{"instId":instrument, 'algoId': algo_order["algoId"]}])
    return {"place_algo_order":place_algo_order,"cancel_algo_order":cancel_algo_order}
 
while True:
    start = timer()

    ticker_px = float(Get_ticker_price(instrument))
    algo_order_list = Get_algo_order_list()
    for algo_ord_itm in algo_order_list:
        print(f"ticker px :{ticker_px}")
        print(f'posSide: {algo_ord_itm["posSide"]}')
        print(f'algoId: {algo_ord_itm["algoId"]}')
        print(f'slTriggerPx: {algo_ord_itm["slTriggerPx"]}')

        trail_calc = Trailing_calc(algo_ord_itm,ticker_px)
        print(trail_calc)
        print("\n \n")
    
    end = timer()
    print(timedelta(seconds=end-start))
    time.sleep(1)
    print("\n \n")


