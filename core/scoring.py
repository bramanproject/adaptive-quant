# core/scoring.py

class ScoringEngine:

    def trend(self, bullish: bool, bearish: bool):

        if bullish:
            return 1.0

        if bearish:
            return 1.0

        return 0.0

    def momentum(self, rsi):

        if 45 <= rsi <= 65:
            return 1.0

        if 35 <= rsi <= 70:
            return 0.7

        return 0.3

    def volume(self, ratio):

        if ratio >= 2:
            return 1.0

        if ratio >= 1.3:
            return 0.8

        if ratio >= 1:
            return 0.6

        return 0.2

    def volatility(self, atr_percent):

        if atr_percent < 0.03:
            return 1.0

        if atr_percent < 0.05:
            return 0.8

        if atr_percent < 0.07:
            return 0.5

        return 0.2

    def market(self, trend_ok):

        return 1.0 if trend_ok else 0.3

    def sector(self, strong):

        return 1.0 if strong else 0.4

    def news(self, positive):

        return 1.0 if positive else 0.5

    def insider(self, positive):

        return 1.0 if positive else 0.3
