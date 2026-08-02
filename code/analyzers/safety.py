from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class SafetyAnalyzer:
    """
    Detects spam, scams and phishing-like messages.
    Returns a risk score between 0 and 1.
    """

    SCAM_KEYWORDS = {
        "otp",
        "pin",
        "password",
        "bank",
        "verify",
        "verification",
        "click",
        "winner",
        "won",
        "gift",
        "claim",
        "urgent",
        "limited",
        "prize",
    }

    def analyze(self, context: MessageContext) -> AnalyzerResult:

        text = (
            context.message.get("message_text", "")
            .lower()
            .strip()
        )

        score = 0.0
        reasons = []

        # Keyword based heuristic
        matched = [
            word
            for word in self.SCAM_KEYWORDS
            if word in text
        ]

        if matched:
            score += min(0.7, len(matched) * 0.1)
            reasons.append(
                "Suspicious keywords: " + ", ".join(matched)
            )

        # Highly forwarded messages
        forwarded = int(
            context.message.get(
                "forwarded_count",
                0,
            )
        )

        if forwarded >= 5:
            score += 0.2
            reasons.append(
                "Frequently forwarded message"
            )

        # Previously reported sender/business
        reports = sum(
            1
            for event in context.events
            if event.get("message_reported") == "True"
        )

        if reports > 0:
            score += 0.2
            reasons.append(
                "Similar messages were reported"
            )

        score = min(score, 1.0)

        if not reasons:
            reasons.append("No obvious safety concerns")

        return AnalyzerResult(
            score=score,
            reason="; ".join(reasons),
            evidence=[],
        )