from app.config import StrategyConfig

from core.strategy import AdaptiveQuantStrategy


def test_create():

    cfg = StrategyConfig()

    strategy = AdaptiveQuantStrategy(cfg)

    assert strategy is not None
