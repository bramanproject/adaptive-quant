# app/main.py

from telegram.bot import AdaptiveBot

TOKEN = "YOUR_BOT_TOKEN"


if __name__ == "__main__":

    bot = AdaptiveBot(TOKEN)

    bot.run()
