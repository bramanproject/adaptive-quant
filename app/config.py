# config.py

from dataclasses import dataclass


@dataclass
class StrategyConfig:
    # ===== Trend =====
    EMA_FAST = 20
    EMA_MID = 50
    EMA_SLOW = 200

    RSI_PERIOD = 14
    ADX_PERIOD = 14

    # ===== Confidence =====
    MIN_CONFIDENCE = 80

    # ===== Risk =====
    MAX_RISK_PER_TRADE = 0.015      # 1.5%
    MIN_RR = 3.0                    # Risk/Reward

    # ===== Holding =====
    MIN_HOLD_DAYS = 3
    MAX_HOLD_DAYS = 14

    # ===== Portfolio =====
    MAX_POSITIONS = 10
    MAX_POSITION_SIZE = 0.10

    # ===== Filters =====
    USE_NEWS = True
    USE_INSIDERS = True
    USE_VOLUME = True
    USE_SECTOR = True
    USE_MARKET_FILTER = True

    # ===== Backtest =====
    INITIAL_CAPITAL = 10000
