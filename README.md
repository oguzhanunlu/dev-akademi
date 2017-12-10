
# dev-akademi

This repository contains two projects, a RESTful api and a Telegram bot, developed during [dev.akademi](https://devakademi.sahibinden.com/).

### Prerequisities & Installation

- Make sure you have `Python 3.6.x` & `pip` installed
- Create a [virtualenv](https://virtualenv.pypa.io/en/stable/) based on `Python 3.6.x`, *[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/ ) ease virtualenv management*
- Clone repository via `git clone git@github.com:oguzhanunlu/dev-akademi.git`
- `cd dev-akademi`
- Activate your virtual environment and run `pip install -r requirements.txt`


### Running

#### RESTful API

- Assuming you are at root of repository, run `cd devakademi/`, `devakademi/` is a Django project
- To start serving API on localhost, run `python manage.py runserver`, API should be up and running on port 8000

#### API Endpoints

```
GET     /api/current                                 - Get current Scoin price
GET     /api/history?date=%Y-%m-%d&time=%H:%M        - Get historical Scoin price
GET     /api/convert?cur1=X&cur1=Y                   - Convert between currencies, supports only `Scoin`, `ETH`, `BTC`, `TL`
GET     /api/buy?amount=X                            - Buy X Scoins
```

#### Telegram Bot

- Assuming you are at root of repository, run `cd bot/`, `bot/` contains a python script
- Run `python bot.py`, it doesn't output to console but expect to see unhandled exceptions for invalid commands.
- Test chatbot while python script is running.

Bot URL : https://telegram.me/SBCoinBot 

Telegram doesn't need your phone connected to the internet. You may use desktop clients.


It was a learning experience if not a winner one. Thanks [sahibinden](https://github.com/sahibinden) !
