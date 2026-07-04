# backtest/runner.py

from data.market_data import MarketData
from backtest.engine import BacktestEngine
from backtest.report import Report

from core.strategy import AdaptiveQuantStrategy

from app.config import StrategyConfig


class Runner:

    def __init__(self):

        self.cfg = StrategyConfig()

        self.strategy = AdaptiveQuantStrategy(
            self.cfg
        )

        self.market = MarketData()

    def run(self, ticker):

        df = self.market.load(ticker)

        engine = BacktestEngine(
            self.strategy
        )

        result = engine.run(
            ticker,
            df
        )

        Report().save(result.metrics)

        return result
