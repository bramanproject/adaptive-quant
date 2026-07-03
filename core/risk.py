# core/risk.py

from dataclasses import dataclass


@dataclass
class RiskResult:

    stop_loss: float

    take_profit: float

    risk_reward: float

    allowed: bool


class RiskEngine:

    def __init__(self, config):

        self.cfg = config

    def calculate(self, price, atr):

        stop = price - max(price * self.cfg.MAX_RISK_PER_TRADE, atr)

        risk = price - stop

        take = price + risk * self.cfg.MIN_RR

        rr = (take - price) / risk

        return RiskResult(

            stop_loss=round(stop, 2),

            take_profit=round(take, 2),

            risk_reward=round(rr, 2),

            allowed=rr >= self.cfg.MIN_RR

        )
