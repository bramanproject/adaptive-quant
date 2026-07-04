# core/strategy.py

from core.indicators import (
    ema,
    rsi,
    atr,
    volume_ratio,
)

from core.scoring import ScoringEngine
from core.confidence import ConfidenceEngine
from core.risk import RiskEngine
from core.self_check import SelfCheck
from core.decision import DecisionEngine

from utils.helpers import (
    ema_alignment,
    bearish_alignment,
)


class AdaptiveQuantStrategy:

    def __init__(self, config):

        self.cfg = config

        self.scoring = ScoringEngine()

        self.confidence = ConfidenceEngine()

        self.risk = RiskEngine(config)

        self.self_check = SelfCheck(config)

        self.decision = DecisionEngine(config)

    def analyze(self, ticker, df):

        df = df.copy()

        df["EMA20"] = ema(
            df["Close"],
            self.cfg.EMA_FAST
        )

        df["EMA50"] = ema(
            df["Close"],
            self.cfg.EMA_MID
        )

        df["EMA200"] = ema(
            df["Close"],
            self.cfg.EMA_SLOW
        )

        df["RSI"] = rsi(
            df["Close"],
            self.cfg.RSI_PERIOD
        )

        df["ATR"] = atr(df)

        df["VOL_RATIO"] = volume_ratio(
            df["Volume"]
        )

        last = df.iloc[-1]

        bullish = ema_alignment(last)

        bearish = bearish_alignment(last)

        signal = "NO TRADE"

        if bullish:
            signal = "LONG"

        elif bearish:
            signal = "SHORT"

        trend_score = self.scoring.trend(
            bullish,
            bearish
        )

        momentum_score = self.scoring.momentum(
            last["RSI"]
        )

        volume_score = self.scoring.volume(
            last["VOL_RATIO"]
        )

        volatility_score = self.scoring.volatility(
            last["ATR"] / last["Close"]
        )

        market_score = self.scoring.market(True)

        sector_score = self.scoring.sector(True)

        news_score = self.scoring.news(True)

        insider_score = self.scoring.insider(True)

        confidence = self.confidence.calculate({

            "trend": trend_score,

            "momentum": momentum_score,

            "volume": volume_score,

            "volatility": volatility_score,

            "market": market_score,

            "sector": sector_score,

            "news": news_score,

            "insider": insider_score,

        })

        risk = self.risk.calculate(

            last["Close"],

            last["ATR"]

        )

        self_check = self.self_check.evaluate(

            df,

            signal

        )

        decision = self.decision.decide(

            signal,

            confidence,

            risk,

            self_check

        )

        return {

            "ticker": ticker,

            "signal": decision.action,

            "approved": decision.approved,

            "confidence": confidence.total,

            "score_breakdown": confidence.breakdown,

            "self_check": self_check.reasons,

            "stop_loss": risk.stop_loss,

            "take_profit": risk.take_profit,

            "risk_reward": risk.risk_reward,

            "decision": decision.reason

        }
