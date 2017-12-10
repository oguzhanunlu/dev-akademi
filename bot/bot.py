from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from datetime import datetime, timedelta
import requests as req
import logging
import time
from random import randint

BOT_TOKEN = "497378988:AAHE2cKiqsoT0APiraNrV2teWPLsGgc4DfU"
SIMULATED_PRICES = {
    "ETH" : 439,
    "BTC" : 1100,
    "TL" : 0.25
}
ALLOWED_CURRENCIES = ['Scoin','ETH', 'BTC', 'TL']

def ts2string(ts, fmt="%Y-%m-%d %H:%M"):
    dt = datetime.fromtimestamp(ts)
    return dt.strftime(fmt)

def string2ts(string, fmt="%Y-%m-%d %H:%M"):
    dt = datetime.strptime(string, fmt)
    t_tuple = dt.timetuple()
    return int(time.mktime(t_tuple))

### helpers above this line

def buy(bot, update, *args, **kwargs):
    """
    Simulate purchase experience with graphical offerings
    """
    params = list(kwargs.items())[0][1]
    if len(params) != 1:
        bot.send_message(chat_id=update.message.chat_id, text="Give me something like '/buy amount'")
        return

    bot.send_message(chat_id=update.message.chat_id, text="Please wait...")
    bot.send_message(chat_id=update.message.chat_id, text="Transaction accomplished! Look at you rich fella.")


def bot_help(bot, update):
    """
    List available commands
    """
    bot.send_message(chat_id=update.message.chat_id,
                    text="Commands:\n\n/start - make the first move\n/history date time - tell me that price!\n/convert cur1 cur2 - conversion is my profession\n/current - tell me current price\n/buy - buy some Scoins\n\n")

def convert(bot, update, *args, **kwargs):
    """
    Convert first one to second one considering current prices.
    """

    params = list(kwargs.items())[0][1]
    if len(params) != 2:
        bot.send_message(chat_id=update.message.chat_id, text="Give me something like '/convert cur1 cur2' where cur1 and cur2 are one of 'ETH', 'BTC', 'TL'")
        return

    if not params[0] in ALLOWED_CURRENCIES and params[1] in ALLOWED_CURRENCIES:
        bot.send_message(chat_id=update.message.chat_id, text="Your currencies must be one of 'Scoin', 'ETH', 'BTC', 'TL'")
        return

    cur1, cur2 = params[0], params[1]
    formatted_ts = None
    if cur1 == 'Scoin' or cur2 == 'Scoin':
        r = req.get('https://devakademi.sahibinden.com/ticker')
        response = r.json()
        timestamp = response["date"] / 1000
        price = response["value"]
        formatted_ts = ts2string(timestamp)

    if not formatted_ts:
        formatted_ts = ts2string(int(time.time()))

    if cur1 == 'Scoin':
        price1 = price
    else:
        price1 = SIMULATED_PRICES[cur1]
    if cur2 == 'Scoin':
        price2 = price
    else:
        price2 = SIMULATED_PRICES[cur2]
    rate = price1 / price2
    text = cur1 + " is " + str(rate) + " " + cur2 +" at " + formatted_ts
    bot.send_message(chat_id=update.message.chat_id, text=text)

def history(bot, update, *args, **kwargs):
    """
    Tell past prices of Scoin for given date and time parameters
    """
    params = list(kwargs.items())[0][1]

    if len(params) != 2:
        text = "Tell me something I can't refuse. To illustrate, '/history 2017-12-10 14:34'"
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return


    date = params[0]
    time = params[1]
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        text = "Please give your date in '%Y-%m-%d' format."
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return
    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        text = "Please give your time in '%H:%M' format."
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return

    date_time = ' '.join([date,time])
    timestamp = string2ts(date_time)

    r = req.get('https://devakademi.sahibinden.com/history')
    response = r.json()
    price = None
    for item in response:
        if item['date'] == timestamp:
            print("found")
            price = item['value']

    # simulate in case it isn't found, which is always since user can't give
    # second information which was used to generate timestamp in history data
    # we could look up nearest price info but I better simulate it and develop another feature for this hackathon
    if not price:
        price = 1000 + randint(0, 100)
    text = "Scoin at " + date_time + " is " + str(price) + " $"

    bot.send_message(chat_id=update.message.chat_id, text=text)

def current(bot, update):
    """
    Tell current Scoin price, sends a HTTP GET only last price expired
    """

    r = req.get('https://devakademi.sahibinden.com/ticker')
    response = r.json()
    timestamp = response["date"] / 1000
    price = response["value"]
    formatted_ts = ts2string(timestamp)
    bot.send_message(chat_id=update.message.chat_id,
                    text="1 Scoin = "+str(price)+ " $ at "+formatted_ts)

def unknown(bot, update):
    """
    Warn in case of invalid commands
    """
    bot.send_message(chat_id=update.message.chat_id,
                    text="Sorry, I didn't understand. '"+update.message.text+"' is NOT a valid command.")

def start(bot, update):
    """
    Start conversation
    """
    bot.send_message(chat_id=update.message.chat_id, text="I'm your Scoin helper, please talk to me! Type /help to see commands.")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(Filters.command, unknown)
    current_handler = CommandHandler('current', current)
    history_handler = CommandHandler('history', history, pass_args=True)
    convert_handler = CommandHandler('convert', convert, pass_args=True)
    help_handler = CommandHandler('help', bot_help)
    buy_handler = CommandHandler('buy', buy, pass_args=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(current_handler)
    dispatcher.add_handler(history_handler)
    dispatcher.add_handler(convert_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(buy_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
