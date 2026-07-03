# self_check.py

from dataclasses import dataclass
from typing import List


@dataclass
class SelfCheckResult:
    approved: bool
    penalty: int
    reasons: List[str]


class SelfCheck:

    def __init__(self, config):
        self.cfg = config

    def evaluate(self, df, signal: str) -> SelfCheckResult:

        last = df.iloc[-1]

        penalty = 0
        reasons = []

        # ---------------------------------
        # Если сделки нет — проверка не нужна
        # ---------------------------------

        if signal == "NO TRADE":
            return SelfCheckResult(
                approved=False,
                penalty=100,
                reasons=["No signal"]
            )

        # ---------------------------------
        # Volume
        # ---------------------------------

        if last["VOL_RATIO"] < 1.0:
            penalty += 10
            reasons.append("Volume below average")

        # ---------------------------------
        # RSI
        # ---------------------------------

        if signal == "LONG":

            if last["RSI"] > 75:
                penalty += 20
                reasons.append("RSI too high")

            if last["Close"] < last["EMA20"]:
                penalty += 20
                reasons.append("Price below EMA20")

        if signal == "SHORT":

            if last["RSI"] < 25:
                penalty += 20
                reasons.append("RSI too low")

            if last["Close"] > last["EMA20"]:
                penalty += 20
                reasons.append("Price above EMA20")

        # ---------------------------------
        # ATR
        # ---------------------------------

        atr_percent = last["ATR"] / last["Close"]

        if atr_percent > 0.07:
            penalty += 15
            reasons.append("ATR too high")

        # ---------------------------------
        # EMA Alignment
        # ---------------------------------

        ema_gap = abs(last["EMA20"] - last["EMA50"]) / last["Close"]

        if ema_gap < 0.003:
            penalty += 10
            reasons.append("Weak EMA separation")

        # ---------------------------------
        # Candle Size
        # ---------------------------------

        candle = abs(last["Close"] - last["Open"]) / last["Close"]

        if candle > 0.08:
            penalty += 10
            reasons.append("Abnormally large candle")

        # ---------------------------------
        # Volume Spike
        # ---------------------------------

        if last["VOL_RATIO"] > 5:
            penalty += 10
            reasons.append("Possible news spike")

        # ---------------------------------
        # Confidence Filter
        # ---------------------------------

        approved = penalty < 30

        if approved:
            reasons.append("Self Check passed")

        else:
            reasons.append("Trade rejected")

        return SelfCheckResult(
            approved=approved,
            penalty=penalty,
            reasons=reasons
        )
