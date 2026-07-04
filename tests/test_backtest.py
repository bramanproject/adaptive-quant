from backtest.metrics import Metrics


def test_metrics():

    m = Metrics()

    result = m.calculate([])

    assert result == {}
