# core/confidence.py

from dataclasses import dataclass
from typing import Dict


@dataclass
class ConfidenceResult:
    total: int
    breakdown: Dict[str, int]


class ConfidenceEngine:

    def __init__(self):

        self.weights = {
            "trend": 25,
            "momentum": 15,
            "volume": 10,
            "volatility": 10,
            "market": 10,
            "sector": 10,
            "news": 10,
            "insider": 10
        }

    def calculate(self, data: Dict):

        score = 0
        breakdown = {}

        for key, weight in self.weights.items():

            value = data.get(key, 0)

            part = round(weight * value)

            breakdown[key] = part

            score += part

        score = max(0, min(100, score))

        return ConfidenceResult(
            total=score,
            breakdown=breakdown
        )
