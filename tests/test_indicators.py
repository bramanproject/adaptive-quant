import pandas as pd

from core.indicators import ema
from core.indicators import rsi


def test_ema():

    s = pd.Series([1,2,3,4,5,6])

    assert len(ema(s,3)) == 6


def test_rsi():

    s = pd.Series(range(50))

    assert len(rsi(s)) == 50
