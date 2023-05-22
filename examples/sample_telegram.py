from tokenfinderbot.tokenfinderbot import TokenBot

# bot instance
bot = TokenBot()

# get bot settings
settings = bot.get_settings()

# change bot telegram settings
settings.telegram.notify = True
settings.telegram.bot_token = "YOUR TELEGRAM BOT TOKEN" # your telegram bot token
settings.telegram.chat_id = "xxxxxxxxxx" # chat id for chat, group or channel which the bot is a memeber of

# set new settings
bot.set_settings(settings)

# run with new settings
bot.run()