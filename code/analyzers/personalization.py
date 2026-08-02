from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class PersonalizationAnalyzer:
    """
    Estimates whether the user is likely to value an interruption.
    Higher score means the user is more likely to appreciate being notified.
    """

    def analyze(self, context: MessageContext) -> AnalyzerResult:

        user = context.user

        if user is None:
            return AnalyzerResult(
                score=0.5,
                reason="User profile unavailable",
                evidence=[],
            )

        opened = int(user.get("messages_opened_30d", 0))
        replied = int(user.get("messages_replied_30d", 0))
        dismissed = int(user.get("notifications_dismissed_30d", 0))
        reported = int(user.get("messages_reported_30d", 0))

        score = 0.5
        reasons = []

        if opened > 20:
            score += 0.15
            reasons.append("Frequently opens messages")

        if replied > 10:
            score += 0.20
            reasons.append("Frequently replies")

        if dismissed > 15:
            score -= 0.15
            reasons.append("Frequently dismisses notifications")

        if reported > 5:
            score -= 0.10
            reasons.append("Frequently reports messages")

        for membership in context.business_history:
            if membership.get("allows_promotions") == "True":
                score += 0.05
                reasons.append("Allows business promotions")

            if membership.get("promotions_opted_out_at"):
                score -= 0.10
                reasons.append("Previously opted out of promotions")

        score = max(0.0, min(score, 1.0))

        if not reasons:
            reasons.append("Neutral user preference")

        return AnalyzerResult(
            score=score,
            reason="; ".join(reasons),
            evidence=[],
        )