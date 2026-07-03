# data/market_data.py

import requests
import pandas as pd


class MarketData:

    BASE = "https://stooq.com/q/d/l/"


    def load(self, ticker):

        symbol = ticker.lower() + ".us"

        url = f"{self.BASE}?s={symbol}&i=d"

        df = pd.read_csv(url)

        df["Date"] = pd.to_datetime(df["Date"])

        df = df.sort_values("Date")

        df.reset_index(drop=True, inplace=True)

        return df
