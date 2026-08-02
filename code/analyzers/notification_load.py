from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class NotificationLoadAnalyzer:
    """
    Estimates whether the user is already receiving
    too many notifications.
    """

    def analyze(self, context: MessageContext) -> AnalyzerResult:

        summaries = context.notification_summary

        if not summaries:
            return AnalyzerResult(
                score=0.5,
                reason="No notification history",
                evidence=[],
            )

        sent = 0
        dismissed = 0

        for row in summaries:
            sent += int(row.get("notifications_sent", 0))
            dismissed += int(row.get("notifications_dismissed", 0))

        score = 1.0
        reasons = []

        if sent > 100:
            score -= 0.30
            reasons.append("High notification volume")

        if dismissed > 50:
            score -= 0.30
            reasons.append("High dismissal rate")

        score = max(0.0, min(score, 1.0))

        if not reasons:
            reasons.append("Normal notification load")

        return AnalyzerResult(
            score=score,
            reason="; ".join(reasons),
            evidence=[],
        )