from analyzers.base import AnalyzerResult
from context_builder import MessageContext


class GroupAnalyzer:
    """
    Evaluates group importance for the user.
    """

    def analyze(
        self,
        context: MessageContext,
    ) -> AnalyzerResult:

        score = 0.5
        reasons = []

        group = context.group

        if not group:
            return AnalyzerResult(
                score=score,
                reason="No group context",
                evidence=[],
            )

        group_type = group.get(
            "group_type",
            "",
        )

        if group_type in [
            "family",
            "work",
            "education",
        ]:
            score += 0.2
            reasons.append(
                "Important group category"
            )

        members = int(
            group.get(
                "member_count",
                0,
            )
        )

        if members > 100:
            score -= 0.1
            reasons.append(
                "Large group noise"
            )

        messages = int(
            group.get(
                "messages_30d",
                0,
            )
        )

        if messages > 50:
            score -= 0.1
            reasons.append(
                "High activity group"
            )

        score = max(
            0.0,
            min(score, 1.0),
        )

        return AnalyzerResult(
            score=score,
            reason=(
                "; ".join(reasons)
                if reasons
                else "No group signals"
            ),
            evidence=[],
        )