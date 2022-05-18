from pyrogram import Client
import configparser
import re
from okex_requests import send_pos

chat_id = "@mehraniacalgo"

config = configparser.ConfigParser()
config.read("config.ini")


api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

app = Client(chat_id, api_id=api_id, api_hash=api_hash)

print("Waiting")
@app.on_raw_update()
async def raw(client, update, users, chats):
    try:
        message = update.message.message
        test_char =  "💹 Trading Setup:"
        if test_char in message:
            price_dict = dict()
            if "🎱 Side: LONG" in message:
                price_dict["side"]="long"
            elif "🎱 Side: SHORT" in message:
                price_dict["side"]="short"
            split_message=message.partition(test_char)
            remove_percent = re.sub("\((.*?)\)", '', split_message[2])
            remove_percent = remove_percent.strip()
            split_info = remove_percent.split('\n')
            split_info = [i.replace("$","") for i in split_info]
            
            for item in split_info:
                item = item.strip()
                temp = item.split(":")
                price_dict[temp[0]] = temp[1].strip()
            print(price_dict)
            
            make_position = send_pos(price_dict["side"], "1", price_dict["Secure TP"], price_dict["SL"])
            print(f"result: {make_position}")
        else:
            print("Ops !")

    except AttributeError as e:
        # print(f"Some Error !!!: {e}")
        pass
app.run() 