# core/portfolio.py

from dataclasses import dataclass


@dataclass
class Position:

    ticker: str

    sector: str

    side: str

    weight: float


class PortfolioEngine:

    def __init__(self, config):

        self.cfg = config

        self.positions = []

    def add(self, position: Position):

        if len(self.positions) >= self.cfg.MAX_POSITIONS:
            return False

        exposure = sum(p.weight for p in self.positions)

        if exposure + position.weight > 1.0:
            return False

        sector_count = sum(
            1
            for p in self.positions
            if p.sector == position.sector
        )

        if sector_count >= 3:
            return False

        self.positions.append(position)

        return True

    def remove(self, ticker):

        self.positions = [
            p for p in self.positions
            if p.ticker != ticker
        ]

    def exists(self, ticker):

        return any(
            p.ticker == ticker
            for p in self.positions
        )

    def summary(self):

        return self.positions
