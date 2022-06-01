
import time
from urllib import response
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
    response_code = int(get_algo_pending["code"])
    if response_code == 0:
        return get_algo_pending["data"]
    else: 
        return get_algo_pending


def Trailing_calc(algo_order,last_px):
    
    output_dict = dict()
    try:
        secure_TP = float(algo_order["tag"][:8].replace("x","."))
        Max_tp = float(algo_order["tag"][8:].replace("x","."))

        mxTP_scTP = ((Max_tp - secure_TP)*40)/100
        safe_level_float = Max_tp - mxTP_scTP
        safe_level = "{:.2f}".format(safe_level_float)


        posSide = algo_order["posSide"]
        # compare is the market price is in safe level for trailing the stop loss
        if posSide == "long": # Long side checking

            margin = ((last_px - safe_level_float)/last_px) * 100
            margin = "{:.2f}".format(margin)

            if last_px >= safe_level_float:
                slTriggerPx = secure_TP
                output_dict["slTriggerPx"] = slTriggerPx
                msg = ""      
            else: 
                msg = "No changes"      


        else: # Short side checking

            margin = (((last_px - safe_level_float)/last_px) * -100) # -100 is for make understand able percent value is short mode
            margin = "{:.2f}".format(margin)            
            if last_px <= safe_level_float:
                slTriggerPx = secure_TP
                output_dict["slTriggerPx"] = slTriggerPx
                msg = ""       
            else: 
                msg = "No changes"      

        output_dict["Safe-level"] = safe_level
        output_dict["Safelvl-margin"] = margin
        output_dict["msg"] = msg


    except ValueError:
        output_dict["msg"] = "Order tag is empty"

    return output_dict


def Place_new_stopLoss(New_slTriggerPx,algo_order,): # Place new algo order for trail a stoploss and cancel old stoploss
    place_algo_order = tradeAPI.place_algo_order(instId=instrument, tdMode="isolated", side="buy", posSide="short", ordType="conditional", sz=algo_order["sz"], slTriggerPx=New_slTriggerPx, slOrdPx = "-1", tag=algo_order["tag"])
    cancel_algo_order = tradeAPI.cancel_algo_order([{"instId":instrument, 'algoId': algo_order["algoId"]}])
    return {"place_algo_order":place_algo_order,"cancel_algo_order":cancel_algo_order}
 
while True:
    start = timer()
    main_json = dict()
    ticker_px = float(Get_ticker_price(instrument))
    algo_order_list = Get_algo_order_list()

    if type(algo_order_list) is list: 

        for algo_ord_itm in algo_order_list:
            trail_calc = Trailing_calc(algo_ord_itm,ticker_px)
            main_json["ticker_px"] = ticker_px
            main_json["posSide"] = algo_ord_itm["posSide"]
            main_json["algoId"] = algo_ord_itm["algoId"]
            main_json["tag"] = algo_ord_itm["tag"]
            main_json["O-slTriggerPx"] = algo_ord_itm["slTriggerPx"]
            main_json["trail_result"] = trail_calc
            print(main_json)
    else:
        print(algo_order_list)


    end = timer()
    print(timedelta(seconds=end-start))
    time.sleep(1)
    print("\n")

