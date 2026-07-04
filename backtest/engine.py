# backtest/engine.py

from dataclasses import dataclass
from typing import List

from backtest.trades import Trade
from backtest.metrics import Metrics


@dataclass
class BacktestResult:

    trades: List[Trade]

    metrics: dict


class BacktestEngine:

    def __init__(self, strategy):

        self.strategy = strategy

    def run(self, ticker, df):

        trades = []

        for i in range(250, len(df) - 15):

            history = df.iloc[: i + 1].copy()

            result = self.strategy.analyze(
                ticker,
                history
            )

            if result.signal == "NO TRADE":
                continue

            entry = history.iloc[-1]["Close"]

            exit_price = df.iloc[i + result.hold_days]["Close"]

            if result.signal == "LONG":

                pnl = (
                    exit_price - entry
                ) / entry * 100

            else:

                pnl = (
                    entry - exit_price
                ) / entry * 100

            trades.append(

                Trade(

                    ticker=ticker,

                    entry_date=str(
                        history.iloc[-1]["Date"]
                    ),

                    exit_date=str(
                        df.iloc[
                            i + result.hold_days
                        ]["Date"]
                    ),

                    side=result.signal,

                    entry=round(entry, 2),

                    exit=round(exit_price, 2),

                    pnl=round(pnl, 2),

                    confidence=result.confidence

                )

            )

        metrics = Metrics().calculate(trades)

        return BacktestResult(

            trades=trades,

            metrics=metrics

        )
