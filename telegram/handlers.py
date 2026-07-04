# telegram/handlers.py

from telegram import Update

from telegram.ext import ContextTypes

from data.market_data import MarketData

from app.config import StrategyConfig

from core.strategy import AdaptiveQuantStrategy


market = MarketData()

cfg = StrategyConfig()

strategy = AdaptiveQuantStrategy(cfg)


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "Adaptive Quant Ready"

    )


async def analyze(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:

        await update.message.reply_text(

            "Example: /send AAPL"

        )

        return

    ticker = context.args[0].upper()

    df = market.load(ticker)

    result = strategy.analyze(
        ticker,
        df
    )

    text = f"""
Ticker: {ticker}

Signal: {result.signal}

Confidence: {result.confidence}%

Stop: {result.stop_loss}

Target: {result.take_profit}

Reasons:

"""

    for r in result.reasons:

        text += f"✅ {r}\n"

    if result.warnings:

        text += "\nWarnings:\n"

        for w in result.warnings:

            text += f"⚠ {w}\n"

    await update.message.reply_text(text)
