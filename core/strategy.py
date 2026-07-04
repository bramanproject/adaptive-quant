import pandas as pd


def generate_signal(df: pd.DataFrame) -> dict:
    """
    STRATEGY LAYER
    """

    if df is None or df.empty:
        return {
            "signal": "HOLD",
            "reason": "empty_data",
            "confidence": 0.0
        }

    last_close = df["close"].iloc[-1]
    mean_price = df["close"].rolling(window=20).mean().iloc[-1]

    if last_close > mean_price:
        return {
            "signal": "BUY",
            "reason": "price_above_20ma",
            "confidence": 0.55
        }

    else:
        return {
            "signal": "HOLD",
            "reason": "below_20ma",
            "confidence": 0.40
        }
