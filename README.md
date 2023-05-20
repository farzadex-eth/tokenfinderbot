# Token Pool Bot
TokenPoolBot is a simple bot for scanning new ERC-20 token pools created and filtering them based on the time created, liquidity and market cap. 
On each run it shows potential good token pools based on the filters.

_**Disclaimer: These markets are volatile and this bot just filters the new pools. If you want to take action on the output of this code, you have to check each pool by yourself and do your own research**_

## How to use
Install the package
```
pip install -i https://test.pypi.org/simple/ tokenfinderbot
```

Basic usage _(default settings)_
```python
from tokenfinderbot.tokenfinderbot import TokenBot

# bot instance
bot = TokenBot()

# run with default settings
bot.run()
```

Advanced usage _(edit settings)_: See [Settings](#settings) Section
```python
from tokenfinderbot.tokenfinderbot import TokenBot

# bot instance
bot = TokenBot()

# get bot settings
settings = bot.get_settings()

# change bot settings
settings.time_filter.hour = 6 # time filter hour edit
settings.liq_mc_filter.min_liq = 1000 # liquidity/market cap filter edit for min. liquidity
settings.db_name = "test" # change json db filename

# set new settings
bot.set_settings(settings)

# run with new settings
bot.run()
```

## Settings
Bot settings:

- **DB Name** _(settings.db_name)_: Name of the json file used as database. This project makes use of [tinydb](https://pypi.org/project/tinydb/) for database. **(default: "db")**

- **Time Filter** _(settings.time_filter)_: Time filter is used to accept only the pools that have been created less than x hours and y minutes ago. This filter setting includes:
  - **Hours** _(settings.time_filter.hours)_: Hours **(default: 12)**
  - **Minutes** _(settings.time_filter.minutes)_: Minutes **(default: 0)**

- **Liquidity/Market Cap Filter** _(settings.liq_mc_filter)_: Filter based on liquidity and market cap which includes three settings:
  - **MarketCap/Liquidity Ratio** _(settings.liq_mc_filter.mc_liq_ratio)_: The minimum accepted ratio of marketcap/liquidity for the pool to be accepted. for example, 2 means the market cap must be at least 2 times the liquidity. **(default: 1.5)**
  - **Min. Market Cap** _(settings.liq_mc_filter.min_mc)_: The minimum accepted marketcap in USD **(default: 100000)**
  - **Min. Liquidity** _(settings.liq_mc_filter.min_liq)_: The minimum accepted liquidity in USD **(default: 1000)**

- **Update Interval** _(settings.update_interval)_: Time interval between each update of the database and calling APIs. Its unit is minutes **(default: 15)**