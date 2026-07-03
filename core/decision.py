# core/decision.py

from dataclasses import dataclass
from core.self_check import SelfCheckResult
from core.risk import RiskResult
from core.confidence import ConfidenceResult


@dataclass
class DecisionResult:

    action: str

    approved: bool

    confidence: int

    reason: str


class DecisionEngine:

    def __init__(self, config):

        self.cfg = config

    def decide(
        self,
        signal: str,
        confidence: ConfidenceResult,
        risk: RiskResult,
        self_check: SelfCheckResult,
    ):

        if signal == "NO TRADE":

            return DecisionResult(
                action="NO TRADE",
                approved=False,
                confidence=confidence.total,
                reason="No valid signal",
            )

        if confidence.total < self.cfg.MIN_CONFIDENCE:

            return DecisionResult(
                action="NO TRADE",
                approved=False,
                confidence=confidence.total,
                reason="Confidence below threshold",
            )

        if not risk.allowed:

            return DecisionResult(
                action="NO TRADE",
                approved=False,
                confidence=confidence.total,
                reason="Risk/Reward unacceptable",
            )

        if not self_check.approved:

            return DecisionResult(
                action="NO TRADE",
                approved=False,
                confidence=confidence.total,
                reason="Rejected by Self Check",
            )

        return DecisionResult(
            action=signal,
            approved=True,
            confidence=confidence.total,
            reason="Approved",
        )
