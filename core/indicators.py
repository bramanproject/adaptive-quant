import pandas as pd


def ema(series: pd.Series, period: int):
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14):
    delta = series.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


def atr(df: pd.DataFrame, period: int = 14):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(period).mean()


def volume_ratio(volume: pd.Series, period: int = 20):
    return volume / volume.rolling(period).mean()
