# strategy.py

from dataclasses import dataclass
from typing import Dict, List

from core.indicators import ema, rsi, atr, volume_ratio


@dataclass
class StrategyResult:
    ticker: str
    signal: str
    confidence: float
    score: int
    reasons: List[str]
    warnings: List[str]
    stop_loss: float
    take_profit: float
    hold_days: int


class AdaptiveQuantStrategy:

    def __init__(self, config):

        self.cfg = config

    def analyze(self, ticker: str, df):

        df = df.copy()

        # -----------------------------
        # Indicators
        # -----------------------------

        df["EMA20"] = ema(df["Close"], self.cfg.EMA_FAST)
        df["EMA50"] = ema(df["Close"], self.cfg.EMA_MID)
        df["EMA200"] = ema(df["Close"], self.cfg.EMA_SLOW)

        df["RSI"] = rsi(df["Close"], self.cfg.RSI_PERIOD)

        df["ATR"] = atr(df)

        df["VOL_RATIO"] = volume_ratio(df["Volume"])

        last = df.iloc[-1]

        score = 0

        confidence = 0

        reasons = []

        warnings = []

        # -----------------------------
        # Trend
        # -----------------------------

        bullish = (
            last.Close >
            last.EMA20 >
            last.EMA50 >
            last.EMA200
        )

        bearish = (
            last.Close <
            last.EMA20 <
            last.EMA50 <
            last.EMA200
        )

        if bullish:

            score += 30
            confidence += 25
            reasons.append("Strong bullish trend")

        elif bearish:

            score -= 30
            confidence += 25
            reasons.append("Strong bearish trend")

        else:

            warnings.append("No clear trend")

        # -----------------------------
        # RSI
        # -----------------------------

        if 45 <= last.RSI <= 65:

            confidence += 15
            reasons.append("Healthy RSI")

        elif last.RSI < 30:

            confidence += 10
            reasons.append("Oversold")

        elif last.RSI > 70:

            warnings.append("Overbought")

        # -----------------------------
        # Volume
        # -----------------------------

        if last.VOL_RATIO >= 1.30:

            confidence += 15
            reasons.append("High relative volume")

        else:

            warnings.append("Weak volume")

        # -----------------------------
        # ATR
        # -----------------------------

        atr_percent = last.ATR / last.Close

        if atr_percent < 0.05:

            confidence += 10
            reasons.append("Controlled volatility")

        else:

            warnings.append("High volatility")

        # -----------------------------
        # Market Structure
        # -----------------------------

        ema_distance = abs(last.EMA20 - last.EMA50)

        if ema_distance / last.Close > 0.01:

            confidence += 10
            reasons.append("Strong EMA separation")

        else:

            warnings.append("Weak momentum")

        # -----------------------------
        # Confidence Clamp
        # -----------------------------

        confidence = min(confidence, 100)

        # -----------------------------
        # Decision
        # -----------------------------

        signal = "NO TRADE"

        if confidence >= self.cfg.MIN_CONFIDENCE:

            if bullish:

                signal = "LONG"

            elif bearish:

                signal = "SHORT"

        # -----------------------------
        # Risk
        # -----------------------------

        stop_loss = round(last.Close * (1 - self.cfg.MAX_RISK_PER_TRADE), 2)

        risk = last.Close - stop_loss

        take_profit = round(last.Close + risk * self.cfg.MIN_RR, 2)

        # -----------------------------
        # Self Check
        # -----------------------------

        if signal != "NO TRADE":

            reject = 0

            if last.VOL_RATIO < 1.0:

                reject += 1

            if last.RSI > 75:

                reject += 1

            if atr_percent > 0.07:

                reject += 1

            if ema_distance / last.Close < 0.005:

                reject += 1

            if reject >= 2:

                signal = "NO TRADE"

                warnings.append("Rejected by Self Check")

        # -----------------------------
        # Result
        # -----------------------------

        return StrategyResult(

            ticker=ticker,

            signal=signal,

            confidence=round(confidence, 1),

            score=score,

            reasons=reasons,

            warnings=warnings,

            stop_loss=stop_loss,

            take_profit=take_profit,

            hold_days=self.cfg.MAX_HOLD_DAYS

        )
