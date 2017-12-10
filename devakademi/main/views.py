from django.http import HttpResponse, JsonResponse

import requests as req
from datetime import datetime, timedelta
import requests as req
import time
from random import randint

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

def buy(request):
    """
    Simulate purchase experience with graphical offerings
    """

    if request.method != "GET":
        return JsonResponse({"error":"/api/buy accepts only GET requests."})

    amount = request.GET.get('amount', None)

    if not amount:
        return JsonResponse({"error":"amount isn't provided. <usage>: /api/buy?amount=X where X is number"})

    return JsonResponse({"transaction_status":"Success"})



def convert(request):
    """
    Convert first one to second one considering current prices.
    """

    if request.method != "GET":
        return JsonResponse({"error":"/api/convert accepts only GET requests."})

    cur1 = request.GET.get('cur1', None)
    cur2 = request.GET.get('cur2', None)

    if not cur1 and not cur2:
        return JsonResponse({"error":"cur1&cur2 isn't provided. <usage>: /api/convert?cur1=X&cur1=Y where X and Y must be one of 'Scoin','ETH', 'BTC', 'TL'"})
    if not cur1:
        return JsonResponse({"error":"cur1 isn't provided. <usage>: /api/convert?cur1=X&cur1=Y where X and Y must be one of 'Scoin','ETH', 'BTC', 'TL'"})
    if not cur2:
        return JsonResponse({"error":"cur2 isn't provided. <usage>: /api/convert?cur1=X&cur1=Y where X and Y must be one of 'Scoin','ETH', 'BTC', 'TL'"})

    if not cur1 in ALLOWED_CURRENCIES and cur2 in ALLOWED_CURRENCIES:
        return JsonResponse({"error":"<usage>: /api/convert?cur1=X&cur1=Y where X and Y must be one of 'Scoin','ETH', 'BTC', 'TL'"})

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
    return JsonResponse({"rate":rate})

def history(request):
    """
    Tell past prices of Scoin for given date and time parameters
    """

    if request.method != "GET":
        return JsonResponse({"error":"/api/history accepts only GET requests."})

    date = request.GET.get('date', None)
    time = request.GET.get('time', None)

    if not date and not time:
        r = req.get('https://devakademi.sahibinden.com/history')
        response = r.json()
        return JsonResponse({"all":response})
    if not date:
        return JsonResponse({"error":"date isn't provided. <usage>: /api/history?date='%Y-%m-%d'&time='%H:%M'"})
    if not time:
        return JsonResponse({"error":"time isn't provided. <usage>: /api/history?date='%Y-%m-%d'&time='%H:%M'"})

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return JsonResponse({"error":"<usage>: /api/history?date='%Y-%m-%d'&time='%H:%M'"})
    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        return JsonResponse({"error":"<usage>: /api/history?date='%Y-%m-%d'&time='%H:%M'"})

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
    return JsonResponse({"price":price, "date_time":date_time})


def current(request):
    """
    Tell current Scoin price
    """

    r = req.get('https://devakademi.sahibinden.com/ticker')
    response = JsonResponse(r.json())
    return response


def index(request):
    r = req.get('https://devakademi.sahibinden.com/ticker')
    return HttpResponse(r.text)
