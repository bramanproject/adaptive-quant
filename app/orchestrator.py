from data.marker_data import load_market_data

from core.strategy import generate_signal
from core.self_check import challenge_signal
from core.decision import make_decision

from backtest.engine import BacktestEngine


class Orchestrator:

    def __init__(self, config):
        self.config = config
        self.backtest_engine = BacktestEngine(config)

    def run_single_step(self, symbol, timestamp):
        """
        Один полный цикл анализа:
        DATA → STRATEGY → CHALLENGE → DECISION
        """

        # 1. DATA LAYER
        data = load_market_data(symbol, timestamp)

        # 2. STRATEGY LAYER
        signal = generate_signal(data)

        # 3. CHALLENGE LAYER (критик)
        challenged_signal = challenge_signal(signal, data)

        # 4. DECISION LAYER
        decision = make_decision(challenged_signal, data)

        return decision

    def run_backtest(self, symbol, start, end):
        """
        Полный backtest через Backtest Engine
        """

        return self.backtest_engine.run(
            orchestrator=self,
            symbol=symbol,
            start=start,
            end=end
        )
