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