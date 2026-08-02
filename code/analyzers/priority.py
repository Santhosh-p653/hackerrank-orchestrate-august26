from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class PriorityAnalyzer:
    """
    Estimates how urgent a message is.
    """

    URGENT_KEYWORDS = {
        "emergency",
        "urgent",
        "asap",
        "immediately",
        "today",
        "now",
        "hospital",
        "accident",
        "meeting",
        "payment",
        "deadline",
        "exam",
        "interview",
    }

    def analyze(self, context: MessageContext) -> AnalyzerResult:

        text = (
            context.message.get("message_text", "")
            .lower()
            .strip()
        )

        score = 0.0
        reasons = []

        matched = [
            word
            for word in self.URGENT_KEYWORDS
            if word in text
        ]

        if matched:
            score += min(0.8, len(matched) * 0.15)
            reasons.append(
                "Urgent keywords: " + ", ".join(matched)
            )

        if context.message.get("conversation_type") == "group":
            group = context.group

            if group and group.get("group_type") == "school":
                score += 0.15
                reasons.append("School group")

            elif group and group.get("group_type") == "family":
                score += 0.20
                reasons.append("Family group")

        score = min(score, 1.0)

        if not reasons:
            reasons.append("No urgency detected")

        return AnalyzerResult(
            score=score,
            reason="; ".join(reasons),
            evidence=[],
        )