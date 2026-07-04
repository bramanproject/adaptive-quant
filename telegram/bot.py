# telegram/bot.py

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from telegram.handlers import (
    start,
    analyze
)


class AdaptiveBot:

    def __init__(self, token):

        self.app = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        self.app.add_handler(
            CommandHandler(
                "start",
                start
            )
        )

        self.app.add_handler(
            CommandHandler(
                "send",
                analyze
            )
        )

    def run(self):

        self.app.run_polling()
