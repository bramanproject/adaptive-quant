import requests
import pandas as pd


class MarketData:
    """
    Data provider for market prices (Stooq source).
    """

    BASE = "https://stooq.com/q/d/l/"

    def load(self, ticker: str) -> pd.DataFrame:
        """
        Load historical daily market data for a ticker.
        """

        try:
            symbol = ticker.lower() + ".us"
            url = f"{self.BASE}?s={symbol}&i=d"

            df = pd.read_csv(url)

            # standardize column names
            df.columns = [c.lower() for c in df.columns]

            # convert date
            df["date"] = pd.to_datetime(df["date"])

            # sort by time
            df = df.sort_values("date").reset_index(drop=True)

            return df

        except Exception as e:
            # чтобы backtest не падал полностью
            print(f"[MarketData ERROR] {ticker}: {e}")
            return pd.DataFrame()


def load_market_data(ticker: str, timestamp=None) -> pd.DataFrame:
    """
    SYSTEM INTERFACE (used by orchestrator)
    """

    md = MarketData()
    df = md.load(ticker)

    if df.empty:
        return df

    return df
